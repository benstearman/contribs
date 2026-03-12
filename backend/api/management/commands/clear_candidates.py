from django.core.management.base import BaseCommand
from api.models import Candidate, Party

class Command(BaseCommand):
    help = 'Clears all Candidate and Party data from the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting Candidates...")
        candidate_count, _ = Candidate.objects.all().delete()
        
        self.stdout.write("Deleting Parties...")
        party_count, _ = Party.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully deleted {candidate_count} candidates and {party_count} parties.'
        ))