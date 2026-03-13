from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Instantly clears all Committee data from the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Instantly truncating Committees (and cascading to Contributions)...")
        
        with connection.cursor() as cursor:
            # TRUNCATE instantly empties the table. 
            # CASCADE tells Postgres to instantly wipe the linked Contributions too.
            cursor.execute('TRUNCATE TABLE api_committee CASCADE;')
            
        self.stdout.write(self.style.SUCCESS('Successfully cleared Committees!'))