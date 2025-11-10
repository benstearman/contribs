from django.contrib import admin
from .models import Office, Party, Candidate, Employer, Contributor, Contribution, FECContribution


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ("office_type", "office_level")
    search_fields = ("office_type", "office_level")


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "party", "office")
    list_filter = ("party", "office")
    search_fields = ("first_name", "last_name", "party__name", "office__office_type")


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "zip_code", "employer")
    list_filter = ("employer",)
    search_fields = ("full_name", "zip_code", "employer__name")


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ("contributor", "amount", "receipt_date")
    list_filter = ("receipt_date",)
    search_fields = ("contributor__full_name",)


@admin.register(FECContribution)
class FECContributionAdmin(admin.ModelAdmin):
    list_display = (
        "NAME",
        "CMTE_ID",
        "TRANSACTION_DT",
        "TRANSACTION_AMT",
        "CITY",
        "STATE",
    )
    list_filter = (
        "STATE",
        "ENTITY_TP",
        "RPT_TP",
        "TRANSACTION_PGI",
    )
    search_fields = (
        "NAME",
        "CMTE_ID",
        "CITY",
        "EMPLOYER",
        "OCCUPATION",
        "TRAN_ID",
    )
    readonly_fields = ("SUB_ID",)
    ordering = ("-TRANSACTION_DT",)
    fieldsets = (
        ("Filer Info", {
            "fields": ("CMTE_ID", "RPT_TP", "AMNDT_IND", "TRANSACTION_PGI", "FILE_NUM")
        }),
        ("Contributor Info", {
            "fields": ("NAME", "CITY", "STATE", "ZIP_CODE", "EMPLOYER", "OCCUPATION", "ENTITY_TP")
        }),
        ("Transaction Details", {
            "fields": ("TRANSACTION_DT", "TRANSACTION_AMT", "TRANSACTION_TP", "OTHER_ID", "TRAN_ID")
        }),
        ("Memo / Metadata", {
            "fields": ("MEMO_CD", "MEMO_TEXT", "IMAGE_NUM", "SUB_ID")
        }),
    )
