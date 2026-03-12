from django.contrib import admin
from django.core.management import call_command
from django.contrib import messages
from .models import Party, Candidate, Employer, Contributor, Contribution, FECContribution, Committee

# ==========================================
# 1. CANDIDATE ACTIONS
# ==========================================
@admin.action(description="[1] Clear all Candidate data")
def run_clear_candidates(modeladmin, request, queryset):
    try:
        call_command('clear_candidates')
        modeladmin.message_user(request, "Successfully cleared Candidates!", messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, f"Clear failed: {e}", messages.ERROR)

@admin.action(description="[2] Run Candidate Import (requires cn.txt)")
def run_candidate_import(modeladmin, request, queryset):
    try:
        call_command('import_candidates', 'data/cn.txt')
        modeladmin.message_user(request, "Successfully ran Candidate import!", messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, f"Import failed: {e}", messages.ERROR)

# ==========================================
# 2. COMMITTEE ACTIONS
# ==========================================
@admin.action(description="[1] Clear all Committee data")
def run_clear_committees(modeladmin, request, queryset):
    try:
        call_command('clear_committees')
        modeladmin.message_user(request, "Successfully cleared Committees!", messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, f"Clear failed: {e}", messages.ERROR)

@admin.action(description="[2] Run Committee Import (requires cm.txt)")
def run_committee_import(modeladmin, request, queryset):
    try:
        call_command('import_committees', 'data/cm.txt')
        modeladmin.message_user(request, "Successfully ran Committee import!", messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, f"Import failed: {e}", messages.ERROR)

# ==========================================
# 3. CONTRIBUTION ACTIONS
# ==========================================
@admin.action(description="[1] Clear all Contribution data")
def run_clear_contributions(modeladmin, request, queryset):
    try:
        call_command('clear_contributions')
        modeladmin.message_user(request, "Successfully cleared Contributions!", messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, f"Clear failed: {e}", messages.ERROR)

@admin.action(description="[2] Run Contribution Import (requires itcont.txt)")
def run_contribution_import(modeladmin, request, queryset):
    try:
        call_command('import_contributions', 'data/itcont.txt')
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
    # Added both clear and import actions
    actions = [run_clear_candidates, run_candidate_import]
    
    list_display = ('CAND_NAME', 'CAND_ID', 'CAND_PTY_AFFILIATION', 'CAND_ELECTION_YR', 'CAND_OFFICE', 'total_contributions')
    list_filter = ('CAND_PTY_AFFILIATION', 'CAND_OFFICE', 'CAND_ELECTION_YR')
    search_fields = ('CAND_NAME', 'CAND_ID')
    autocomplete_fields = ['CAND_PTY_AFFILIATION']

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    # Added both clear and import actions
    actions = [run_clear_committees, run_committee_import]
    
    list_display = ('CMTE_NM', 'CMTE_ID', 'CMTE_TP', 'CAND_ID')
    list_filter = ('CMTE_TP', 'CMTE_ST', 'CMTE_DSGN')
    search_fields = ('CMTE_NM', 'CMTE_ID')
    raw_id_fields = ('CAND_ID',)

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'zip_code', 'employer')
    search_fields = ('full_name', 'zip_code')
    list_select_related = ('employer',) 

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    # Added both clear and import actions
    actions = [run_clear_contributions, run_contribution_import]
    
    list_display = ('contributor', 'committee', 'amount', 'receipt_date')
    raw_id_fields = ('contributor', 'committee')
    list_select_related = ('contributor', 'committee')
    show_full_result_count = False

@admin.register(FECContribution)
class FECContributionAdmin(admin.ModelAdmin):
    list_display = ('NAME', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'CMTE_ID')
    list_filter = ('STATE', 'TRANSACTION_DT')
    search_fields = ('NAME', 'CMTE_ID')
    show_full_result_count = False