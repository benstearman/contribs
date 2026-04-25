from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = '🚀 Cascading PostgreSQL Aggregation (Optimized for 4GB RAM / 12M+ rows)'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # 1. THE TURBO BUTTONS
            # synchronous_commit = off is the #1 way to speed up massive updates in Postgres
            self.stdout.write("Unlocking maximum database speed (disabling sync-commit)...")
            cursor.execute("SET synchronous_commit = off;")
            cursor.execute("SET work_mem = '512MB';") # Slightly higher, safe for 4GB
            cursor.execute("ANALYZE api_contribution;")

            # 2. Reset everything to zero first (Fast)
            self.stdout.write("Resetting all totals to 0.00...")
            cursor.execute("UPDATE api_committee SET total_contributions = 0.00;")
            cursor.execute("UPDATE api_contributor SET total_contributions = 0.00;")
            cursor.execute("UPDATE api_employer SET total_contributions = 0.00;")
            cursor.execute("UPDATE api_candidate SET total_contributions = 0.00;")

            # 3. Step 1: Update Committees & Contributors (The only pass over the 12.7M table)
            self.stdout.write("Step 1: Calculating Committee & Contributor totals from 12.7M donations...")
            
            # Update Committees
            cursor.execute('''
                CREATE TEMP TABLE tmp_cmte_sums AS 
                SELECT committee_id, SUM(amount) as total FROM api_contribution GROUP BY committee_id;
            ''')
            cursor.execute('UPDATE api_committee c SET total_contributions = t.total FROM tmp_cmte_sums t WHERE c."CMTE_ID" = t.committee_id;')
            cursor.execute("DROP TABLE tmp_cmte_sums;")

            # Update Contributors
            cursor.execute('''
                CREATE TEMP TABLE tmp_contributor_sums AS 
                SELECT contributor_id, SUM(amount) as total FROM api_contribution GROUP BY contributor_id;
            ''')
            cursor.execute('UPDATE api_contributor c SET total_contributions = t.total FROM tmp_contributor_sums t WHERE c.id = t.contributor_id;')
            cursor.execute("DROP TABLE tmp_contributor_sums;")

            # 4. Step 2: Cascading Updates (These are INSTANT because they don't touch the 12.7M table)
            self.stdout.write("Step 2: Cascading totals to Employers & Candidates (Fast mode)...")
            
            # Update Employers (Summing Contributor totals, not individual donations)
            cursor.execute('''
                CREATE TEMP TABLE tmp_emp_sums AS 
                SELECT employer_id, SUM(total_contributions) as total FROM api_contributor 
                WHERE employer_id IS NOT NULL GROUP BY employer_id;
            ''')
            cursor.execute('UPDATE api_employer e SET total_contributions = t.total FROM tmp_emp_sums t WHERE e.id = t.employer_id;')
            
            # Update Candidates (Summing Committee totals)
            cursor.execute('''
                CREATE TEMP TABLE tmp_cand_sums AS 
                SELECT "CAND_ID_id" as cand_id, SUM(total_contributions) as total FROM api_committee 
                WHERE "CAND_ID_id" IS NOT NULL GROUP BY "CAND_ID_id";
            ''')
            cursor.execute('UPDATE api_candidate cand SET total_contributions = t.total FROM tmp_cand_sums t WHERE cand."CAND_ID" = t.cand_id;')

            # 5. Step 3: Cleanup & Cache
            self.stdout.write("Step 3: Finalizing and clearing cache...")
            cursor.execute("DELETE FROM django_cache;")
            
            # Reset DB safety settings
            cursor.execute("SET synchronous_commit = on;")
            cursor.execute("SET work_mem = '4MB';")

        self.stdout.write(self.style.SUCCESS('Successfully completed cascading update! All totals are now live.'))
