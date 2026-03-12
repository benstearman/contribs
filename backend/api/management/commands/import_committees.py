import csv
from django.core.management.base import BaseCommand
from api.models import Committee, Candidate

class Command(BaseCommand):
    help = 'Imports Committees from the FEC Master file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the committee master CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        self.stdout.write(f"Reading from {csv_file_path}...")

        with open(csv_file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',') 
            processed_count = 0
            
            for row in reader:
                # 1. Safely link candidate if they exist in the DB
                cand_id_str = row.get('CAND_ID', '').strip()
                candidate_obj = None
                if cand_id_str:
                    candidate_obj = Candidate.objects.filter(CAND_ID=cand_id_str).first()

                # 2. Create or Update the Committee
                Committee.objects.update_or_create(
                    CMTE_ID=row['CMTE_ID'].strip(),
                    defaults={
                        'CMTE_NM': row.get('CMTE_NM', '').strip(),
                        'TRES_NM': row.get('TRES_NM', '').strip() or None,
                        'CMTE_ST': row.get('CMTE_ST', '').strip()[:2] or None,
                        'CMTE_TP': row.get('CMTE_TP', '').strip()[:1] or None,
                        'CMTE_DSGN': row.get('CMTE_DSGN', '').strip()[:1] or None,
                        'CAND_ID': candidate_obj
                    }
                )
                
                processed_count += 1
                if processed_count % 1000 == 0:
                    self.stdout.write(f"Processed {processed_count} committees...")

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {processed_count} Committees!'))