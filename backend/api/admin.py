from django.contrib import admin
from django.core.management import call_command
from django.contrib import messages
from .models import Party, Candidate, Employer, Contributor, Contribution, FECContribution, Committee

# ==========================================
# IMPORT ACTIONS
# ==========================================
@admin.action(description="Run Candidate Import (requires cn.txt)")
def run_candidate_import(modeladmin, request, queryset):
    try:
        call_command('import_candidates', 'cn.txt')
        modeladmin.message_user(request, "Successfully ran Candidate import!", messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, f"Import failed: {e}", messages.ERROR)

@admin.action(description="Run Committee Import (requires cm.txt)")
def run_committee_import(modeladmin, request, queryset):
    try:
        call_command('import_committees', 'cm.txt')
        modeladmin.message_user(request, "Successfully ran Committee import!", messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, f"Import failed: {e}", messages.ERROR)

@admin.action(description="Run Contribution Import (requires itcont.txt)")
def run_contribution_import(modeladmin, request, queryset):
    try:
        call_command('import_contributions', 'itcont.txt')
        modeladmin.message_user(request, "Successfully ran Contribution import!", messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, f"Import failed: {e}", messages.ERROR)


# ==========================================
# OPTIMIZED ADMIN CLASSES
# ==========================================
@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    actions = [run_candidate_import]
    # Re-added 'total_contributions' so you can see the math you set up!
    list_display = ('CAND_NAME', 'CAND_ID', 'CAND_PTY_AFFILIATION', 'CAND_ELECTION_YR', 'CAND_OFFICE', 'total_contributions')
    list_filter = ('CAND_PTY_AFFILIATION', 'CAND_OFFICE', 'CAND_ELECTION_YR')
    search_fields = ('CAND_NAME', 'CAND_ID')
    autocomplete_fields = ['CAND_PTY_AFFILIATION'] # Improves performance for dropdowns

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    actions = [run_committee_import]
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
    list_select_related = ('employer',) # Performance optimization

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    actions = [run_contribution_import]
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