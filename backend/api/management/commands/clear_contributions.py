from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Instantly clears all Contributions, Contributors, and Employers'

    def handle(self, *args, **kwargs):
        self.stdout.write("Instantly truncating Contributions, Contributors, and Employers...")
        
        with connection.cursor() as cursor:
            # You can string multiple tables together in one TRUNCATE command
            cursor.execute('TRUNCATE TABLE api_contribution, api_contributor, api_employer CASCADE;')
            
        self.stdout.write(self.style.SUCCESS('Successfully cleared Contributions data!'))