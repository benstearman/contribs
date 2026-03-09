from django.core.management.base import BaseCommand
from django.db.models import Sum
from api.models import Candidate

class Command(BaseCommand):
    help = 'Calculates and saves total_contributions for all candidates'

    def handle(self, *args, **options):
        self.stdout.write("Calculating totals...")
        
        # Do the heavy math here, in the background
        candidates = Candidate.objects.annotate(
            calculated_total=Sum('committees__contributions__amount')
        )
        
        updated_count = 0
        for candidate in candidates:
            # If they have no contributions, default to 0.00
            new_total = candidate.calculated_total or 0.00
            
            # Only hit the database to save if the number actually changed
            if candidate.total_contributions != new_total:
                candidate.total_contributions = new_total
                candidate.save(update_fields=['total_contributions'])
                updated_count += 1
                
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} candidates.'))