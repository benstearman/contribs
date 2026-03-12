import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import Contribution, Contributor, Employer, Committee

class Command(BaseCommand):
    help = 'Imports Contributions from the FEC Individual Contributions file (itcont.txt)'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the itcont.txt file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        self.stdout.write(f"Reading from {csv_file_path}...")

        with open(csv_file_path, newline='', encoding='utf-8', errors='replace') as file:
            # Official FEC headers for Individual Contributions
            fec_headers = [
                'CMTE_ID', 'AMNDT_IND', 'RPT_TP', 'TRANSACTION_PGI', 'IMAGE_NUM', 
                'TRANSACTION_TP', 'ENTITY_TP', 'NAME', 'CITY', 'STATE', 'ZIP_CODE', 
                'EMPLOYER', 'OCCUPATION', 'TRANSACTION_DT', 'TRANSACTION_AMT', 
                'OTHER_ID', 'TRAN_ID', 'FILE_NUM', 'MEMO_CD', 'MEMO_TEXT', 'SUB_ID'
            ]
            
            reader = csv.DictReader(file, fieldnames=fec_headers, delimiter='|') 
            processed_count = 0
            
            for row in reader:
                cmte_id_str = row.get('CMTE_ID', '').strip()
                committee_obj = Committee.objects.filter(CMTE_ID=cmte_id_str).first()
                if not committee_obj:
                    continue
                    
                emp_name = row.get('EMPLOYER', '').strip()
                employer_obj = None
                if emp_name:
                    employer_obj, _ = Employer.objects.get_or_create(name=emp_name)

                full_name = row.get('NAME', '').strip() or "UNKNOWN"
                zip_code = row.get('ZIP_CODE', '').strip()[:9] 
                
                contributor_obj, _ = Contributor.objects.get_or_create(
                    full_name=full_name,
                    zip_code=zip_code,
                    defaults={'employer': employer_obj}
                )

                raw_date = row.get('TRANSACTION_DT', '').strip()
                receipt_date = None
                if raw_date:
                    try:
                        receipt_date = datetime.strptime(raw_date, '%m%d%Y').date()
                    except ValueError:
                        pass
                        
                if not receipt_date:
                    continue 

                try:
                    amount = float(row.get('TRANSACTION_AMT', '').strip())
                except ValueError:
                    amount = 0.00
                    
                fec_sub_id = row.get('SUB_ID', '').strip()
                if not fec_sub_id:
                    continue

                Contribution.objects.update_or_create(
                    fec_sub_id=fec_sub_id,
                    defaults={
                        'contributor': contributor_obj,
                        'committee': committee_obj,
                        'amount': amount,
                        'receipt_date': receipt_date
                    }
                )
                
                processed_count += 1
                if processed_count % 1000 == 0:
                    self.stdout.write(f"Processed {processed_count} contributions...")

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {processed_count} Contributions!'))