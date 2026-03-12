from django.core.management.base import BaseCommand
from api.models import Committee

class Command(BaseCommand):
    help = 'Clears all Committee data from the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting Committees (this will also cascade delete related Contributions)...")
        committee_count, _ = Committee.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {committee_count} committees.'))