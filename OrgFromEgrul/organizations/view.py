from rest_framework.generics import get_object_or_404, ListAPIView

from OrgFromEgrul.organizations.models import OrganizationEgrul
from OrgFromEgrul.organizations.serializers import OrganizationEgrulCreateOrUpdateSerializer


class OrganizationEgrulView(ListAPIView):
    """"
    Возвращение организации по ИНН + ОГРН
    """
    # queryset = OrganizationEgrul.objects.filter()
    serializer_class = OrganizationEgrulCreateOrUpdateSerializer

    def get_queryset(self):
        org_inn = self.request.query_params.get('inn')
        org_ogrn = self.request.query_params.get('ogrn')
        list_obj = OrganizationEgrul.objects.filter(ogrn=org_ogrn, inn=org_inn)
        return list_obj

    #
    # def get_object(self):
    #     org_inn = self.request.query_params.get('inn')
    #     org_ogrn = self.request.query_params.get('ogrn')
    #     obj = get_object_or_404(self.queryset, inn=org_inn, ogrn=org_ogrn)
    #     return obj
    #
