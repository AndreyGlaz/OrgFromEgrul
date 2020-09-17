from rest_framework import serializers

from OrgFromEgrul.organizations.models import OrganizationEgrul, OrganizationEgrip


class OrganizationEgrulCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationEgrul
        fields = '__all__'


class OrganizationEgripCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationEgrip
        fields = '__all__'
