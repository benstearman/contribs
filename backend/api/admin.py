from django.contrib import admin
from .models import Office, Party, Candidate, Employer, Contributor, Contribution, FECContribution, Committee

@admin.register(FECContribution)
class FECContributionAdmin(admin.ModelAdmin):
    list_display = ('NAME', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'ENTITY_TP', 'CMTE_ID')
    list_filter = ('ENTITY_TP', 'STATE', 'TRANSACTION_DT')
    search_fields = ('NAME', 'CMTE_ID', 'TRAN_ID')
    date_hierarchy = 'TRANSACTION_DT'

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('CMTE_NM', 'CMTE_ID', 'CMTE_TP', 'CMTE_ST')
    list_filter = ('CMTE_TP', 'CMTE_ST', 'CMTE_DSGN')
    search_fields = ('CMTE_NM', 'CMTE_ID', 'TRES_NM')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'office', 'party')
    list_filter = ('party', 'office')
    search_fields = ('last_name', 'first_name')

# Registering the simpler models with default views
admin.site.register(Office)
admin.site.register(Party)
admin.site.register(Employer)
admin.site.register(Contributor)
admin.site.register(Contribution)