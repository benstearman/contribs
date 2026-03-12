import csv
from django.core.management.base import BaseCommand
from api.models import Candidate, Party

class Command(BaseCommand):
    help = 'Imports Candidates and normalizes Party affiliations from the FEC Master file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the candidate master CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        self.stdout.write(f"Reading from {csv_file_path}...")

        with open(csv_file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',') 
            
            processed_count = 0
            
            for row in reader:
                # 1. Normalize the Party Lookup Table
                party_code = row.get('CAND_PTY_AFFILIATION', '').strip()
                party_obj = None
                
                if party_code:
                    party_obj, _ = Party.objects.get_or_create(
                        id=party_code,
                        defaults={'name': party_code}
                    )

                # 2. Safely create OR update the Candidate
                # We use CAND_ID to look them up, and update the defaults if they exist
                Candidate.objects.update_or_create(
                    CAND_ID=row['CAND_ID'].strip(),
                    defaults={
                        'CAND_NAME': row['CAND_NAME'].strip(),
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