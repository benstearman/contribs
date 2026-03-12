import csv
from django.core.management.base import BaseCommand
from api.models import Committee, Candidate

class Command(BaseCommand):
    help = 'Imports Committees from the FEC Master file (cm.txt)'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the cm.txt file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        self.stdout.write(f"Reading from {csv_file_path}...")

        with open(csv_file_path, newline='', encoding='utf-8', errors='replace') as file:
            # Official FEC headers for Committee Master
            fec_headers = [
                'CMTE_ID', 'CMTE_NM', 'TRES_NM', 'CMTE_ST1', 'CMTE_ST2', 'CMTE_CITY', 
                'CMTE_ST', 'CMTE_ZIP', 'CMTE_DSGN', 'CMTE_TP', 'CMTE_PTY_AFFILIATION', 
                'CMTE_FILING_FREQ', 'ORG_TP', 'CONNECTED_ORG_NM', 'CAND_ID'
            ]
            
            reader = csv.DictReader(file, fieldnames=fec_headers, delimiter='|') 
            processed_count = 0
            
            for row in reader:
                cand_id_str = row.get('CAND_ID', '').strip()
                candidate_obj = None
                if cand_id_str:
                    candidate_obj = Candidate.objects.filter(CAND_ID=cand_id_str).first()

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