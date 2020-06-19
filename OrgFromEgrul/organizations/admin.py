from django.contrib import admin

from OrgFromEgrul.organizations.models import OrganizationEgrul


@admin.register(OrganizationEgrul)
class EditionTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ogrn']
    search_fields = ["name"]
