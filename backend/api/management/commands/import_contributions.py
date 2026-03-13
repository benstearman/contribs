import os
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = '100x Faster PostgreSQL Native ETL for 12.7M rows'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the itcont.txt file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file']
        abs_path = os.path.abspath(file_path)

        with connection.cursor() as cursor:
            # --- 🚀 THE TURBOCHARGER 🚀 ---
            # Temporarily give Postgres 1GB of RAM to do massive Hash Joins and Index building purely in memory
            self.stdout.write("Unlocking PostgreSQL memory limits...")
            cursor.execute("SET work_mem = '1GB';")
            cursor.execute("SET maintenance_work_mem = '1GB';")

            # 1. CREATE A RAW STAGING TABLE
            self.stdout.write("1. Creating raw PostgreSQL staging table...")
            cursor.execute('''
                DROP TABLE IF EXISTS temp_fec_import;
                CREATE UNLOGGED TABLE temp_fec_import (
                    CMTE_ID text, AMNDT_IND text, RPT_TP text, TRANSACTION_PGI text, 
                    IMAGE_NUM text, TRANSACTION_TP text, ENTITY_TP text, NAME text, 
                    CITY text, STATE text, ZIP_CODE text, EMPLOYER text, 
                    OCCUPATION text, TRANSACTION_DT text, TRANSACTION_AMT text, 
                    OTHER_ID text, TRAN_ID text, FILE_NUM text, MEMO_CD text, 
                    MEMO_TEXT text, SUB_ID bigint
                );
            ''')

            # 2. STREAM THE FILE DIRECTLY TO POSTGRESQL
            self.stdout.write("2. Streaming 12.7M rows directly into PostgreSQL engine (Takes ~1-2 mins)...")
            with open(abs_path, 'r', encoding='utf-8', errors='replace') as f:
                sql = f"""
                COPY temp_fec_import FROM STDIN WITH (
                    FORMAT csv, 
                    DELIMITER '|', 
                    QUOTE '{chr(31)}', 
                    NULL ''
                )
                """
                cursor.copy_expert(sql, f)

            # 3. EXTRACT AND SAVE EMPLOYERS
            self.stdout.write("3. Extracting and saving unique Employers...")
            cursor.execute('''
                INSERT INTO api_employer (name)
                SELECT DISTINCT trim(EMPLOYER) FROM temp_fec_import
                WHERE EMPLOYER IS NOT NULL AND trim(EMPLOYER) != ''
                ON CONFLICT (name) DO NOTHING;
            ''')

            # 4. EXTRACT AND SAVE CONTRIBUTORS
            self.stdout.write("4. Extracting and saving unique Contributors...")
            cursor.execute('''
                INSERT INTO api_contributor (full_name, zip_code, employer_id)
                SELECT DISTINCT 
                    COALESCE(trim(t.NAME), 'UNKNOWN'), 
                    COALESCE(SUBSTRING(trim(t.ZIP_CODE) FROM 1 FOR 9), ''),
                    e.id
                FROM temp_fec_import t
                LEFT JOIN api_employer e ON e.name = trim(t.EMPLOYER)
                WHERE t.NAME IS NOT NULL OR t.ZIP_CODE IS NOT NULL
                ON CONFLICT (full_name, zip_code) DO NOTHING;
            ''')

            # 5. LINK EVERYTHING TOGETHER AND SAVE CONTRIBUTIONS
            self.stdout.write("5. Linking 12.7M Contributions (Using high-memory Hash Joins)...")
            
            # Using a CTE (WITH clause) computes the string cleanup FIRST,
            # so Postgres doesn't have to recalculate strings 12.7 million times during the JOIN
            cursor.execute('''
                WITH cleaned_import AS (
                    SELECT 
                        SUB_ID,
                        CAST(NULLIF(trim(TRANSACTION_AMT), '') AS NUMERIC) as amount,
                        TO_DATE(NULLIF(trim(TRANSACTION_DT), ''), 'MMDDYYYY') as receipt_date,
                        CMTE_ID,
                        COALESCE(trim(NAME), 'UNKNOWN') as clean_name,
                        COALESCE(SUBSTRING(trim(ZIP_CODE) FROM 1 FOR 9), '') as clean_zip
                    FROM temp_fec_import
                    WHERE LENGTH(trim(TRANSACTION_DT)) = 8
                )
                INSERT INTO api_contribution (fec_sub_id, amount, receipt_date, committee_id, contributor_id)
                SELECT 
                    t.SUB_ID,
                    t.amount,
                    t.receipt_date,
                    t.CMTE_ID,
                    c.id
                FROM cleaned_import t
                JOIN api_committee com ON com."CMTE_ID" = t.CMTE_ID
                JOIN api_contributor c ON c.full_name = t.clean_name AND c.zip_code = t.clean_zip
                ON CONFLICT (fec_sub_id) DO NOTHING;
            ''')

            # 6. CLEANUP
            self.stdout.write("6. Cleaning up staging table...")
            cursor.execute('DROP TABLE temp_fec_import;')
            
            # Reset memory limits to standard defaults
            cursor.execute("SET work_mem = '4MB';")
            cursor.execute("SET maintenance_work_mem = '64MB';")

        self.stdout.write(self.style.SUCCESS('Successfully processed 12.7 Million Contributions at database speed!'))