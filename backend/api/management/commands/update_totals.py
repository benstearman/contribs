from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = '🚀 Zero-Hog PostgreSQL Aggregation (Optimized for 4GB RAM)'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # 1. Safe memory limit for 4GB server
            self.stdout.write("Configuring server-friendly performance limits...")
            cursor.execute("SET work_mem = '256MB';")

            # 2. Update Committee Totals
            self.stdout.write("1. Calculating Committee totals (Batch mode)...")
            cursor.execute("UPDATE api_committee SET total_contributions = 0.00;")
            cursor.execute('''
                CREATE TEMP TABLE tmp_cmte_sums AS 
                SELECT committee_id, SUM(amount) as total 
                FROM api_contribution 
                GROUP BY committee_id;
            ''')
            cursor.execute('''
                UPDATE api_committee c 
                SET total_contributions = t.total 
                FROM tmp_cmte_sums t 
                WHERE c."CMTE_ID" = t.committee_id;
            ''')
            cursor.execute("DROP TABLE tmp_cmte_sums;")

            # 3. Update Candidate Totals (Sums up all their committees)
            self.stdout.write("2. Calculating Candidate totals...")
            cursor.execute("UPDATE api_candidate SET total_contributions = 0.00;")
            cursor.execute('''
                CREATE TEMP TABLE tmp_cand_sums AS 
                SELECT "CAND_ID_id" as cand_id, SUM(total_contributions) as total 
                FROM api_committee 
                WHERE "CAND_ID_id" IS NOT NULL
                GROUP BY "CAND_ID_id";
            ''')
            cursor.execute('''
                UPDATE api_candidate cand 
                SET total_contributions = t.total 
                FROM tmp_cand_sums t 
                WHERE cand."CAND_ID" = t.cand_id;
            ''')
            cursor.execute("DROP TABLE tmp_cand_sums;")

            # 4. Update Contributor Totals
            self.stdout.write("3. Calculating Contributor totals...")
            cursor.execute("UPDATE api_contributor SET total_contributions = 0.00;")
            cursor.execute('''
                CREATE TEMP TABLE tmp_contributor_sums AS 
                SELECT contributor_id, SUM(amount) as total 
                FROM api_contribution 
                GROUP BY contributor_id;
            ''')
            cursor.execute('''
                UPDATE api_contributor c 
                SET total_contributions = t.total 
                FROM tmp_contributor_sums t 
                WHERE c.id = t.contributor_id;
            ''')
            cursor.execute("DROP TABLE tmp_contributor_sums;")

            # 5. Update Employer Totals
            self.stdout.write("4. Calculating Employer totals...")
            cursor.execute("UPDATE api_employer SET total_contributions = 0.00;")
            cursor.execute('''
                CREATE TEMP TABLE tmp_employer_sums AS 
                SELECT c.employer_id, SUM(con.amount) as total
                FROM api_contributor c
                JOIN api_contribution con ON con.contributor_id = c.id
                WHERE c.employer_id IS NOT NULL
                GROUP BY c.employer_id;
            ''')
            cursor.execute('''
                UPDATE api_employer e 
                SET total_contributions = t.total 
                FROM tmp_employer_sums t 
                WHERE e.id = t.employer_id;
            ''')
            cursor.execute("DROP TABLE tmp_employer_sums;")

            # 6. Clear Cache
            self.stdout.write("5. Clearing API cache...")
            cursor.execute("DELETE FROM django_cache;")
            
            # Reset memory
            cursor.execute("SET work_mem = '4MB';")

        self.stdout.write(self.style.SUCCESS('Successfully updated all totals using high-speed batch processing!'))
