from django.contrib import admin
from .models import Office, Party, Candidate, Employer, Contributor, Contribution


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
