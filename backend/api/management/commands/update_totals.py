from django.core.management.base import BaseCommand
from django.db.models import Sum
from api.models import Candidate, Committee, Employer, Contributor

class Command(BaseCommand):
    help = 'Calculates and saves total_contributions for all candidates, committees, employers, and contributors'

    def handle(self, *args, **options):
        # 1. Update Committee Totals
        self.stdout.write("Calculating committee totals...")
        committees = Committee.objects.annotate(
            calculated_total=Sum('contributions__amount')
        )
        
        cmte_updated = 0
        for cmte in committees:
            new_total = cmte.calculated_total or 0.00
            if cmte.total_contributions != new_total:
                cmte.total_contributions = new_total
                cmte.save(update_fields=['total_contributions'])
                cmte_updated += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {cmte_updated} committees.'))

        # 2. Update Candidate Totals
        self.stdout.write("Calculating candidate totals...")
        candidates = Candidate.objects.annotate(
            calculated_total=Sum('committees__contributions__amount')
        )
        
        cand_updated = 0
        for candidate in candidates:
            new_total = candidate.calculated_total or 0.00
            if candidate.total_contributions != new_total:
                candidate.total_contributions = new_total
                candidate.save(update_fields=['total_contributions'])
                cand_updated += 1
                
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {cand_updated} candidates.'))

        # 3. Update Contributor Totals
        self.stdout.write("Calculating contributor totals...")
        contributors = Contributor.objects.annotate(
            calculated_total=Sum('contributions__amount')
        )
        
        cont_updated = 0
        for contributor in contributors:
            new_total = contributor.calculated_total or 0.00
            if contributor.total_contributions != new_total:
                contributor.total_contributions = new_total
                contributor.save(update_fields=['total_contributions'])
                cont_updated += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {cont_updated} contributors.'))

        # 4. Update Employer Totals
        self.stdout.write("Calculating employer totals...")
        employers = Employer.objects.annotate(
            calculated_total=Sum('contributor_set__contributions__amount')
        )
        
        emp_updated = 0
        for employer in employers:
            new_total = employer.calculated_total or 0.00
            if employer.total_contributions != new_total:
                employer.total_contributions = new_total
                employer.save(update_fields=['total_contributions'])
                emp_updated += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {emp_updated} employers.'))