from django.core.management.base import BaseCommand
from api.models import Contribution, Contributor, Employer

class Command(BaseCommand):
    help = 'Clears all Contributions, Contributors, and Employers'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting Contributions...")
        cont_count, _ = Contribution.objects.all().delete()
        
        self.stdout.write("Deleting Contributors...")
        contrib_count, _ = Contributor.objects.all().delete()
        
        self.stdout.write("Deleting Employers...")
        emp_count, _ = Employer.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully deleted {cont_count} contributions, {contrib_count} contributors, and {emp_count} employers.'
        ))