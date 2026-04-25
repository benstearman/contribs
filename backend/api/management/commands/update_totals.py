from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = '🚀 High-Performance Incremental Aggregation (Optimized for 4GB RAM)'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # 1. Performance Tuning
            self.stdout.write("Tuning PostgreSQL for massive data movement...")
            cursor.execute("SET synchronous_commit = off;")
            cursor.execute("SET work_mem = '512MB';")
            cursor.execute("SET maintenance_work_mem = '512MB';")
            
            # Step 1: Committees
            self.stdout.write("1. Updating Committee totals (Incremental)...")
            cursor.execute('''
                CREATE TEMP TABLE tmp_cmte_sums AS 
                SELECT committee_id, SUM(amount) as total FROM api_contribution GROUP BY committee_id;
            ''')
            cursor.execute('CREATE INDEX idx_tmp_cmte ON tmp_cmte_sums(committee_id);')
            cursor.execute('''
                UPDATE api_committee c 
                SET total_contributions = t.total 
                FROM tmp_cmte_sums t 
                WHERE c."CMTE_ID" = t.committee_id AND c.total_contributions != t.total;
            ''')
            cursor.execute("DROP TABLE tmp_cmte_sums;")

            # Step 2: Contributors
            self.stdout.write("2. Updating Contributor totals (This is the big one)...")
            cursor.execute('''
                CREATE TEMP TABLE tmp_contributor_sums AS 
                SELECT contributor_id, SUM(amount) as total FROM api_contribution GROUP BY contributor_id;
            ''')
            cursor.execute('CREATE INDEX idx_tmp_contributor ON tmp_contributor_sums(contributor_id);')
            cursor.execute('''
                UPDATE api_contributor c 
                SET total_contributions = t.total 
                FROM tmp_contributor_sums t 
                WHERE c.id = t.contributor_id AND c.total_contributions != t.total;
            ''')
            cursor.execute("DROP TABLE tmp_contributor_sums;")

            # Step 3: Employers (Uses pre-calculated Contributor totals - INSTANT)
            self.stdout.write("3. Cascading totals to Employers...")
            cursor.execute('''
                CREATE TEMP TABLE tmp_emp_sums AS 
                SELECT employer_id, SUM(total_contributions) as total FROM api_contributor 
                WHERE employer_id IS NOT NULL GROUP BY employer_id;
            ''')
            cursor.execute('''
                UPDATE api_employer e 
                SET total_contributions = t.total 
                FROM tmp_emp_sums t 
                WHERE e.id = t.employer_id AND e.total_contributions != t.total;
            ''')

            # Step 4: Candidates (Uses pre-calculated Committee totals - INSTANT)
            self.stdout.write("4. Cascading totals to Candidates...")
            cursor.execute('''
                CREATE TEMP TABLE tmp_cand_sums AS 
                SELECT "CAND_ID_id" as cand_id, SUM(total_contributions) as total FROM api_committee 
                WHERE "CAND_ID_id" IS NOT NULL GROUP BY "CAND_ID_id";
            ''')
            cursor.execute('''
                UPDATE api_candidate cand 
                SET total_contributions = t.total 
                FROM tmp_cand_sums t 
                WHERE cand."CAND_ID" = t.cand_id AND cand.total_contributions != t.total;
            ''')

            # Step 5: Finalize
            self.stdout.write("5. Clearing cache...")
            from django.core.cache import cache
            cache.clear()
            
            # Reset
            cursor.execute("SET synchronous_commit = on;")

        self.stdout.write(self.style.SUCCESS('Aggregation complete! Most operations were handled incrementally.'))
