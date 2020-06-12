from rest_framework import serializers

from OrgFromEgrul.organizations.models import OrganizationEgrul


class OrganizationEgrulCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationEgrul
        fields = '__all__'
