from django.contrib import admin

from OrgFromEgrul.organizations.models import OrganizationEgrul, SuccessfullyProcessedZip


@admin.register(OrganizationEgrul)
class OrganizationEgrulAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ogrn']
    search_fields = ['name', 'ogrn']


@admin.register(SuccessfullyProcessedZip)
class SuccessfullyProcessedZipAdmin(admin.ModelAdmin):
    list_display = ['id', 'url_zip', 'date']
    search_fields = ['url_zip']

