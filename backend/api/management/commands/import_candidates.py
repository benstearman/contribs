import csv
from django.core.management.base import BaseCommand
from api.models import Candidate, Party

class Command(BaseCommand):
    help = 'Imports Candidates from the FEC Master file (cn.txt)'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the cn.txt file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        self.stdout.write(f"Reading from {csv_file_path}...")

        with open(csv_file_path, newline='', encoding='utf-8', errors='replace') as file:
            # Official FEC headers for Candidate Master
            fec_headers = [
                'CAND_ID', 'CAND_NAME', 'CAND_PTY_AFFILIATION', 'CAND_ELECTION_YR', 
                'CAND_OFFICE_ST', 'CAND_OFFICE', 'CAND_OFFICE_DISTRICT', 'ICI_CODE', 
                'CAND_STATUS', 'CAND_PCC', 'CAND_ST1', 'CAND_ST2', 'CAND_CITY', 
                'CAND_ST', 'CAND_ZIP'
            ]
            
            # Read using pipes and explicit headers
            reader = csv.DictReader(file, fieldnames=fec_headers, delimiter='|') 
            processed_count = 0
            
            for row in reader:
                party_code = row.get('CAND_PTY_AFFILIATION', '').strip()
                party_obj = None
                
                if party_code:
                    party_obj, _ = Party.objects.get_or_create(
                        id=party_code[:3],
                        defaults={'name': party_code}
                    )

                Candidate.objects.update_or_create(
                    CAND_ID=row['CAND_ID'].strip(),
                    defaults={
                        'CAND_NAME': row.get('CAND_NAME', '').strip(),
                        'CAND_PTY_AFFILIATION': party_obj,
                        'CAND_ELECTION_YR': int(row['CAND_ELECTION_YR']) if row.get('CAND_ELECTION_YR') else None,
                        'CAND_OFFICE_ST': row.get('CAND_OFFICE_ST', '').strip()[:2] or None,
                        'CAND_OFFICE': row.get('CAND_OFFICE', '').strip()[:1] or None,
                        'CAND_OFFICE_DISTRICT': row.get('CAND_OFFICE_DISTRICT', '').strip()[:2] or None
                    }
                )
                
                processed_count += 1
                if processed_count % 1000 == 0:
                    self.stdout.write(f"Processed {processed_count} candidates...")

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {processed_count} Candidates!'))