from django.contrib import admin
from .models import Party, Candidate, Employer, Contributor, Contribution, FECContribution, Committee

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('CAND_NAME', 'CAND_ID', 'CAND_PTY_AFFILIATION', 'CAND_ELECTION_YR', 'CAND_OFFICE')
    list_filter = ('CAND_PTY_AFFILIATION', 'CAND_OFFICE', 'CAND_ELECTION_YR')
    search_fields = ('CAND_NAME', 'CAND_ID')
    autocomplete_fields = ['CAND_PTY_AFFILIATION'] # Improves performance for dropdowns

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('CMTE_NM', 'CMTE_ID', 'CMTE_TP', 'CAND_ID')
    list_filter = ('CMTE_TP', 'CMTE_ST', 'CMTE_DSGN')
    search_fields = ('CMTE_NM', 'CMTE_ID')
    raw_id_fields = ('CAND_ID',) # Better for large candidate tables

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'zip_code', 'employer')
    search_fields = ('full_name', 'zip_code')
    list_select_related = ('employer',) # Performance optimization for 8GB RAM

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('contributor', 'committee', 'amount', 'receipt_date')
    # Use raw_id_fields so the admin doesn't crash trying to load 100k+ items into a dropdown
    raw_id_fields = ('contributor', 'committee')
    # Optimizes the admin list view SQL
    list_select_related = ('contributor', 'committee')
    # Speeds up the page by not calculating the total count of millions of rows
    show_full_result_count = False

@admin.register(FECContribution)
class FECContributionAdmin(admin.ModelAdmin):
    list_display = ('NAME', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'CMTE_ID')
    list_filter = ('STATE', 'TRANSACTION_DT')
    search_fields = ('NAME', 'CMTE_ID')
    show_full_result_count = False # Faster loading for millions of rows