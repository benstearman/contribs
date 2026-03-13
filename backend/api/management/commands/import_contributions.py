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

        # 1. CREATE A RAW STAGING TABLE
        self.stdout.write("1. Creating raw PostgreSQL staging table...")
        with connection.cursor() as cursor:
            cursor.execute('''
                DROP TABLE IF EXISTS temp_fec_import;
                -- UNLOGGED tables are insanely fast because they don't write to crash-recovery logs
                CREATE UNLOGGED TABLE temp_fec_import (
                    CMTE_ID text, AMNDT_IND text, RPT_TP text, TRANSACTION_PGI text, 
                    IMAGE_NUM text, TRANSACTION_TP text, ENTITY_TP text, NAME text, 
                    CITY text, STATE text, ZIP_CODE text, EMPLOYER text, 
                    OCCUPATION text, TRANSACTION_DT text, TRANSACTION_AMT text, 
                    OTHER_ID text, TRAN_ID text, FILE_NUM text, MEMO_CD text, 
                    MEMO_TEXT text, SUB_ID bigint
                );
            ''')

            # 2. STREAM THE FILE DIRECTLY TO POSTGRESQL (Bypassing Python)
            self.stdout.write("2. Streaming 12.7M rows directly into PostgreSQL engine (Takes ~1-2 mins)...")
            with open(abs_path, 'r', encoding='utf-8', errors='replace') as f:
                # Using a Python f-string to inject the literal ASCII 31 unit separator character
                sql = f"""
                COPY temp_fec_import FROM STDIN WITH (
                    FORMAT csv, 
                    DELIMITER '|', 
                    QUOTE '{chr(31)}', 
                    NULL ''
                )
                """
                cursor.copy_expert(sql, f)

            # 3. EXTRACT AND SAVE EMPLOYERS (Database-native speed)
            self.stdout.write("3. Extracting and saving unique Employers...")
            cursor.execute('''
                INSERT INTO api_employer (name)
                SELECT DISTINCT trim(EMPLOYER) FROM temp_fec_import
                WHERE EMPLOYER IS NOT NULL AND trim(EMPLOYER) != ''
                ON CONFLICT (name) DO NOTHING;
            ''')

            # 4. EXTRACT AND SAVE CONTRIBUTORS (Database-native speed)
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
            self.stdout.write("5. Linking 12.7M Contributions to Committees and Contributors...")
            cursor.execute('''
                INSERT INTO api_contribution (fec_sub_id, amount, receipt_date, committee_id, contributor_id)
                SELECT 
                    t.SUB_ID,
                    CAST(NULLIF(trim(t.TRANSACTION_AMT), '') AS NUMERIC),
                    TO_DATE(NULLIF(trim(t.TRANSACTION_DT), ''), 'MMDDYYYY'),
                    t.CMTE_ID,
                    c.id
                FROM temp_fec_import t
                -- Only attach to valid Committees in our DB
                JOIN api_committee com ON com."CMTE_ID" = t.CMTE_ID
                -- Match back to the Contributor we just created
                JOIN api_contributor c ON 
                    c.full_name = COALESCE(trim(t.NAME), 'UNKNOWN') AND 
                    c.zip_code = COALESCE(SUBSTRING(trim(t.ZIP_CODE) FROM 1 FOR 9), '')
                -- Filter out corrupted FEC dates using regex
                WHERE t.TRANSACTION_DT ~ '^[0-9]{8}$' 
                ON CONFLICT (fec_sub_id) DO NOTHING;
            ''')

            # 6. CLEANUP
            self.stdout.write("6. Cleaning up staging table...")
            cursor.execute('DROP TABLE temp_fec_import;')

        self.stdout.write(self.style.SUCCESS('Successfully processed 12.7 Million Contributions at database speed!'))