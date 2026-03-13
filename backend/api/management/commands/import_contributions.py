import csv
from datetime import datetime
from functools import lru_cache
from django.core.management.base import BaseCommand
from api.models import Contribution, Contributor, Employer, Committee

class Command(BaseCommand):
    help = 'Blazing fast Contributions import using LRU caching and bulk_create'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the itcont.txt file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        self.stdout.write(f"Reading from {csv_file_path}...")

        # 1. CACHE ALL COMMITTEES (Small enough to hold entirely in RAM)
        self.stdout.write("Pre-loading valid committees into memory...")
        valid_committees = set(Committee.objects.values_list('CMTE_ID', flat=True))
        self.stdout.write(f"Loaded {len(valid_committees)} committees into RAM.")

        # 2. MEMORY-SAFE CACHES (Prevents 8GB RAM crash while stopping 90% of DB hits)
        @lru_cache(maxsize=50000)
        def get_employer_id(emp_name):
            if not emp_name:
                return None
            employer_obj, _ = Employer.objects.get_or_create(name=emp_name)
            return employer_obj.id

        @lru_cache(maxsize=200000)
        def get_contributor_id(full_name, zip_code, employer_id):
            contributor_obj, _ = Contributor.objects.get_or_create(
                full_name=full_name,
                zip_code=zip_code,
                defaults={'employer_id': employer_id}
            )
            return contributor_obj.id

        # 3. BATCH SETUP
        batch_size = 5000
        contributions_batch = []
        processed_count = 0
        skipped_count = 0

        with open(csv_file_path, newline='', encoding='utf-8', errors='replace') as file:
            fec_headers = [
                'CMTE_ID', 'AMNDT_IND', 'RPT_TP', 'TRANSACTION_PGI', 'IMAGE_NUM', 
                'TRANSACTION_TP', 'ENTITY_TP', 'NAME', 'CITY', 'STATE', 'ZIP_CODE', 
                'EMPLOYER', 'OCCUPATION', 'TRANSACTION_DT', 'TRANSACTION_AMT', 
                'OTHER_ID', 'TRAN_ID', 'FILE_NUM', 'MEMO_CD', 'MEMO_TEXT', 'SUB_ID'
            ]
            
            reader = csv.DictReader(file, fieldnames=fec_headers, delimiter='|') 
            
            for row in reader:
                # O(1) Instant memory lookup instead of hitting the DB
                cmte_id = row.get('CMTE_ID', '').strip()
                if cmte_id not in valid_committees:
                    skipped_count += 1
                    continue

                raw_date = row.get('TRANSACTION_DT', '').strip()
                receipt_date = None
                if raw_date:
                    try:
                        receipt_date = datetime.strptime(raw_date, '%m%d%Y').date()
                    except ValueError:
                        pass
                        
                if not receipt_date:
                    skipped_count += 1
                    continue 

                try:
                    amount = float(row.get('TRANSACTION_AMT', '').strip())
                except ValueError:
                    amount = 0.00
                    
                fec_sub_id = row.get('SUB_ID', '').strip()
                if not fec_sub_id:
                    skipped_count += 1
                    continue

                # Fetch IDs using the blazing fast RAM cache
                emp_name = row.get('EMPLOYER', '').strip()
                employer_id = get_employer_id(emp_name)

                full_name = row.get('NAME', '').strip() or "UNKNOWN"
                zip_code = row.get('ZIP_CODE', '').strip()[:9] 
                contributor_id = get_contributor_id(full_name, zip_code, employer_id)

                # Assemble the Contribution completely in RAM using raw foreign key IDs
                contribution = Contribution(
                    fec_sub_id=fec_sub_id,
                    contributor_id=contributor_id,
                    committee_id=cmte_id,
                    amount=amount,
                    receipt_date=receipt_date
                )
                contributions_batch.append(contribution)
                processed_count += 1

                # --- FIRE THE BATCH PAYLOAD ---
                if len(contributions_batch) >= batch_size:
                    Contribution.objects.bulk_create(
                        contributions_batch,
                        update_conflicts=True,
                        unique_fields=['fec_sub_id'],
                        update_fields=['amount', 'receipt_date']
                    )
                    self.stdout.write(f"Processed {processed_count} contributions... (Skipped {skipped_count})")
                    contributions_batch = [] 

            # --- CLEANUP: Save any leftover rows in the final partial batch ---
            if contributions_batch:
                Contribution.objects.bulk_create(
                    contributions_batch,
                    update_conflicts=True,
                    unique_fields=['fec_sub_id'],
                    update_fields=['amount', 'receipt_date']
                )

        # Print some cool stats about how many database queries the RAM cache saved!
        self.stdout.write(f"\nRAM Cache Performance:")
        self.stdout.write(f"Employers: {get_employer_id.cache_info()}")
        self.stdout.write(f"Contributors: {get_contributor_id.cache_info()}")

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully processed {processed_count} Contributions! (Skipped {skipped_count})'))