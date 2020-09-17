import xml.etree.ElementTree as ET

from OrgFromEgrul.organizations.models import OrganizationEgrip
from OrgFromEgrul.organizations.serializers import OrganizationEgripCreateOrUpdateSerializer
import logging

logging.basicConfig(filename='parsing_egrip.log', format='%(asctime)s-%(levelname)s:%(message)s', level=logging.INFO)

# Словарь для хранения пути к тем элементам организации,
# которые можно прото передать item_validation без дополнительных фиксов
location_of_org_elements = {
    'ogrn': {'path': '.', 'element': 'ОГРНИП'},
    'inn': {'path': '.', 'element': 'ИННФЛ'},
    'first_name': {'path': './СвФЛ//ФИОРус', 'element': 'Имя'},
    'second_name': {'path': './СвФЛ//ФИОРус', 'element': 'Фамилия'},
    'patronymic': {'path': './СвФЛ//ФИОРус', 'element': 'Отчество'},
    'region': {'path': './СвАдрМЖ//АдресРФ', 'element': 'КодРегион'},
    'locality': {'path': './СвАдрМЖ//АдресРФ//Город', 'element': 'НаимГород'},
    'liquidation_date': {'path': './СвПрекращ//СвСтатус', 'element': 'ДатаПрекращ'},
}


# Проверка на существование элемента парсинга
def item_validation(element, item_path, attribute):
    if element.find(item_path + '[@' + attribute + ']') is not None:
        return element.find(item_path).get(attribute)
    else:
        return ''


# Создаёт или обновляет запись в организациях
def save_in_base(wrapt_org):
    if OrganizationEgrip.objects.filter(ogrn=wrapt_org['ogrn']).exists():
        existing_org = OrganizationEgrip.objects.get(ogrn=wrapt_org['ogrn'])
        serializer = OrganizationEgripCreateOrUpdateSerializer(existing_org, data=wrapt_org)
    else:
        serializer = OrganizationEgripCreateOrUpdateSerializer(data=wrapt_org)
    is_valid = serializer.is_valid()
    if is_valid:
        serializer.save()
    else:
        print(serializer.errors)


def file_parser_egrip(file_xml):
    parser = ET.XMLParser(encoding="windows-1251")
    root = ET.parse(file_xml, parser=parser)

    for child in root.iter('СвИП'):
        wrapt_organization = dict()
        for key, value in location_of_org_elements.items():
            if value['path'] == '' and value['element'] == '':
                wrapt_organization[key] = ''
            else:
                wrapt_organization[key] = item_validation(child, value['path'], value['element'])
        save_in_base(wrapt_organization)
