from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = '🚀 High-Performance PostgreSQL Aggregation for all totals'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Temporarily unlock memory for massive joins
            self.stdout.write("Unlocking PostgreSQL performance...")
            cursor.execute("SET work_mem = '1GB';")

            # 1. Update Committee Totals
            self.stdout.write("1. Updating Committee totals...")
            cursor.execute('''
                UPDATE api_committee c
                SET total_contributions = COALESCE((
                    SELECT SUM(amount) FROM api_contribution WHERE committee_id = c."CMTE_ID"
                ), 0.00);
            ''')

            # 2. Update Candidate Totals (Sums up all their committees)
            self.stdout.write("2. Updating Candidate totals...")
            cursor.execute('''
                UPDATE api_candidate cand
                SET total_contributions = COALESCE((
                    SELECT SUM(total_contributions) 
                    FROM api_committee 
                    WHERE "CAND_ID_id" = cand."CAND_ID"
                ), 0.00);
            ''')

            # 3. Update Contributor Totals
            self.stdout.write("3. Updating Contributor totals...")
            cursor.execute('''
                UPDATE api_contributor c
                SET total_contributions = COALESCE((
                    SELECT SUM(amount) FROM api_contribution WHERE contributor_id = c.id
                ), 0.00);
            ''')

            # 4. Update Employer Totals (Native SQL JOIN is 1000x faster than ORM)
            self.stdout.write("4. Updating Employer totals (This may take a moment)...")
            cursor.execute('''
                WITH employer_sums AS (
                    SELECT c.employer_id, SUM(con.amount) as calculated_total
                    FROM api_contributor c
                    JOIN api_contribution con ON con.contributor_id = c.id
                    WHERE c.employer_id IS NOT NULL
                    GROUP BY c.employer_id
                )
                UPDATE api_employer e
                SET total_contributions = s.calculated_total
                FROM employer_sums s
                WHERE e.id = s.employer_id;
            ''')

            # 5. Clear Cache
            self.stdout.write("5. Clearing API cache...")
            cursor.execute("DELETE FROM django_cache;") # Fast way to clear file/db cache
            
            # Reset memory
            cursor.execute("SET work_mem = '4MB';")

        self.stdout.write(self.style.SUCCESS('Successfully updated all totals using native PostgreSQL engine!'))
