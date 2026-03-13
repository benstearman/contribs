import csv
from django.core.management.base import BaseCommand
from api.models import Candidate, Party

class Command(BaseCommand):
    help = 'Blazing fast Candidate import using bulk_create and in-memory caching'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the cn.txt file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        self.stdout.write(f"Reading from {csv_file_path}...")

        # 1. IN-MEMORY CACHING: Pre-load all parties so we NEVER query the DB for them in the loop
        party_cache = {party.id: party for party in Party.objects.all()}
        
        # 2. BATCH SETUP: We will save 5,000 candidates at a time
        batch_size = 5000
        candidates_batch = []
        processed_count = 0

        with open(csv_file_path, newline='', encoding='utf-8', errors='replace') as file:
            fec_headers = [
                'CAND_ID', 'CAND_NAME', 'CAND_PTY_AFFILIATION', 'CAND_ELECTION_YR', 
                'CAND_OFFICE_ST', 'CAND_OFFICE', 'CAND_OFFICE_DISTRICT', 'ICI_CODE', 
                'CAND_STATUS', 'CAND_PCC', 'CAND_ST1', 'CAND_ST2', 'CAND_CITY', 
                'CAND_ST', 'CAND_ZIP'
            ]
            
            reader = csv.DictReader(file, fieldnames=fec_headers, delimiter='|') 
            
            for row in reader:
                # --- FAST PARTY LOOKUP ---
                party_code = row.get('CAND_PTY_AFFILIATION', '').strip()[:3]
                party_obj = None
                
                if party_code:
                    if party_code not in party_cache:
                        # Only hit the DB if it's a brand new party we've never seen
                        new_party = Party.objects.create(id=party_code, name=party_code)
                        party_cache[party_code] = new_party
                    party_obj = party_cache[party_code]

                # --- ASSEMBLE CANDIDATE (In RAM, no DB hit) ---
                candidate = Candidate(
                    CAND_ID=row['CAND_ID'].strip(),
                    CAND_NAME=row.get('CAND_NAME', '').strip(),
                    CAND_PTY_AFFILIATION=party_obj,
                    CAND_ELECTION_YR=int(row['CAND_ELECTION_YR']) if row.get('CAND_ELECTION_YR') else None,
                    CAND_OFFICE_ST=row.get('CAND_OFFICE_ST', '').strip()[:2] or None,
                    CAND_OFFICE=row.get('CAND_OFFICE', '').strip()[:1] or None,
                    CAND_OFFICE_DISTRICT=row.get('CAND_OFFICE_DISTRICT', '').strip()[:2] or None
                )
                candidates_batch.append(candidate)
                processed_count += 1

                # --- FIRE THE BATCH PAYLOAD ---
                if len(candidates_batch) >= batch_size:
                    Candidate.objects.bulk_create(
                        candidates_batch,
                        update_conflicts=True, # Tells Postgres to safely update if ID exists
                        unique_fields=['CAND_ID'],
                        update_fields=['CAND_NAME', 'CAND_PTY_AFFILIATION', 'CAND_ELECTION_YR', 'CAND_OFFICE_ST', 'CAND_OFFICE', 'CAND_OFFICE_DISTRICT']
                    )
                    self.stdout.write(f"Processed {processed_count} candidates...")
                    candidates_batch = [] # Empty the list to start the next batch

            # --- CLEANUP: Save any leftover candidates in the final partial batch ---
            if candidates_batch:
                Candidate.objects.bulk_create(
                    candidates_batch,
                    update_conflicts=True,
                    unique_fields=['CAND_ID'],
                    update_fields=['CAND_NAME', 'CAND_PTY_AFFILIATION', 'CAND_ELECTION_YR', 'CAND_OFFICE_ST', 'CAND_OFFICE', 'CAND_OFFICE_DISTRICT']
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {processed_count} Candidates at lightspeed!'))