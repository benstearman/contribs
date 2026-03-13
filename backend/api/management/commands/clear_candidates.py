from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Instantly clears all Candidate and Party data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Instantly truncating Candidates and Parties...")
        
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE api_candidate, api_party CASCADE;')
            
        self.stdout.write(self.style.SUCCESS('Successfully cleared Candidates!'))