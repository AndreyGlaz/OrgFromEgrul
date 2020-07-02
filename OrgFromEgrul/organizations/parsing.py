import xml.etree.ElementTree as ET
import re

from django.core.exceptions import ObjectDoesNotExist

from OrgFromEgrul.organizations.getting_data import log_in_file
from OrgFromEgrul.organizations.models import OrganizationEgrul
from OrgFromEgrul.organizations.serializers import OrganizationEgrulCreateOrUpdateSerializer

# Словарь для хранения пути к тем элементам организации,
# которые можно прото передать item_validation без дополнительных фиксов
location_of_org_elements = {
    'name': {'path': 'СвНаимЮЛ', 'element': 'НаимЮЛПолн'},
    'short_name': {'path': 'СвНаимЮЛ', 'element': 'НаимЮЛСокр'},
    'inn': {'path': '.', 'element': 'ИНН'},
    'kpp': {'path': '.', 'element': 'КПП'},
    'ogrn': {'path': 'СвОбрЮЛ', 'element': 'ОГРН'},
    'index': {'path': './СвАдресЮЛ//АдресРФ', 'element': 'Индекс'},
    'street': {'path': './СвАдресЮЛ//АдресРФ//Улица', 'element': 'НаимУлица'},
    'building': {'path': './СвАдресЮЛ//АдресРФ', 'element': 'Корпус'},
    'supervisor_name': {'path': './СведДолжнФЛ//СвФЛ', 'element': 'Имя'},
    'supervisor_surname': {'path': './СведДолжнФЛ//СвФЛ', 'element': 'Фамилия'},
    'supervisor_patronymic': {'path': './СведДолжнФЛ//СвФЛ', 'element': 'Отчество'},
    'supervisor_post': {'path': './СведДолжнФЛ//СвДолжн', 'element': 'НаимДолжн'},
    'okopf': {'path': '.', 'element': 'КодОПФ'},
    # 'region': {'path': './СвАдресЮЛ//АдресРФ', 'element': 'КодРегион'}
}

# Словарь для хранения пути к тем элементам филиала/подразделения,
# которые можно прото передать item_validation без дополнительных фиксов
location_of_subdiv_elements = {
    'index': {'path': 'АдрМНРФ', 'element': 'Индекс'},
    'street': {'path': './АдрМНРФ//Улица', 'element': 'НаимУлица'},
    'building': {'path': 'АдрМНРФ', 'element': 'Корпус'},
    # 'region': {'path': 'АдрМНРФ', 'element': 'КодРегион'}
}


# Проверка на существование элемента парсинга
def item_validation(element, item_path, attribute):
    if element.find(item_path + '[@' + attribute + ']') is not None:
        return element.find(item_path).get(attribute)
    else:
        return ''


# Берёт КПП из нужного элемента в зависимости от типа предприятия: Филиал или Представительство
def kpp_for_subdivision(element):
    if element.tag == 'СвФилиал':
        return item_validation(element, 'СвУчетНОФилиал', 'КПП')
    else:
        return item_validation(element, 'СвУчетНОПредстав', 'КПП')


# Фиксит проблему xml-документа - указание наименования города в элементе "Регион"
def location_validation(element):
    if element is not None:
        try:
            if element.find('Регион').get('ТипРегион') == 'ГОРОД':
                return item_validation(element, 'Регион', 'НаимРегион')
            else:
                return item_validation(element, 'Город', 'НаимГород')
        except AttributeError:
            return ''
    else:
        return ''


# Генерация адреса предприятия (нужен для создания наименования предпиятия)
def address_generation(wrapt_subdivision):
    delimiter = ' '
    return delimiter.join([wrapt_subdivision['locality'], wrapt_subdivision['street'], wrapt_subdivision['building']])


# Возвращает наименование предприятия в зависимости от предоставленных данных в xml
# Если названия нет в xml, то генерируется на основе родительского предприятия и адреса
def name_subdivision_validation(element, wrapt_subdivision, name_main_organization):
    if element.find('СвНаим[@НаимПолн]') is not None:
        return element.find('СвНаим').get('НаимПолн')
    else:
        type_subdivision = 'ФИЛИАЛ' if (element.tag == 'СвФилиал') else 'ПРЕДСТАВИТЕЛЬСТВО'
        delimiter = ' '
        return delimiter.join([type_subdivision, name_main_organization, address_generation(wrapt_subdivision)])


# Функция для подстановки id соответствующей записи из словаря вместо значения. Для связки таблиц.
# def finding_from_dict(value, model):
#     if value and len(value.replace(' ', '')) == 5 and model.objects.filter(code=value.replace(' ', '')).exists():
#         return model.objects.get(code=value.replace(' ', '')).pk
#     else:
#         return None

# Функция для проверки на количество символов в выгрузке (может попадаться 2. Например "49".
def okopf_validate(value):
    if value and len(value.replace(' ', '')) == 5:
        return value
    else:
        return ''


# Создаёт или обновляет запись в организациях
def save_in_base(wrapt_org, kpp_subdivision=''):
    if OrganizationEgrul.objects.filter(ogrn=wrapt_org['ogrn']).exists():
        if wrapt_org['main_company'] is not None:  # Проверка: филиал или главная компания
            if OrganizationEgrul.objects.filter(ogrn=wrapt_org['ogrn'],
                                                kpp=kpp_subdivision).exists():  # Проверка на наличие такого филиала
                existing_sub = OrganizationEgrul.objects.get(ogrn=wrapt_org['ogrn'], kpp=kpp_subdivision)
                serializer = OrganizationEgrulCreateOrUpdateSerializer(existing_sub, data=wrapt_org)
            else:
                serializer = OrganizationEgrulCreateOrUpdateSerializer(data=wrapt_org)
        else:
            existing_org = OrganizationEgrul.objects.get(ogrn=wrapt_org['ogrn'], main_company=None)
            serializer = OrganizationEgrulCreateOrUpdateSerializer(existing_org, data=wrapt_org)
    else:
        serializer = OrganizationEgrulCreateOrUpdateSerializer(data=wrapt_org)
    is_valid = serializer.is_valid()
    if is_valid:
        serializer.save()
    else:
        print(serializer.errors)


def file_parser(file_xml):
    parser = ET.XMLParser(encoding="windows-1251")
    root = ET.XML(file_xml, parser=parser)

    # array_of_organizations = list()

    for child in root.iter('СвЮЛ'):
        wrapt_organization = dict()

        for key, value in location_of_org_elements.items():
            if value['path'] == '' and value['element'] == '':
                wrapt_organization[key] = ''
            else:
                wrapt_organization[key] = item_validation(child, value['path'], value['element'])

        wrapt_organization['locality'] = location_validation(
            child.find('./СвАдресЮЛ//АдресРФ'))  # правильно находит название города
        wrapt_organization['house'] = re.sub(r'[^0-9]', '',
                                             item_validation(child, './СвАдресЮЛ//АдресРФ', 'Дом')
                                             )  # отавляет в строке только цыфры
        wrapt_organization['okopf'] = okopf_validate(wrapt_organization['okopf'])
        wrapt_organization['main_company'] = None
        save_in_base(wrapt_organization)
        # array_of_organizations.append(wrapt_organization)

        if child.find('СвПодразд'):
            for subdivision in child.find('СвПодразд'):
                wrapt_subdivision = dict()

                for key, value in location_of_subdiv_elements.items():
                    wrapt_subdivision[key] = item_validation(child, value['path'], value['element'])

                wrapt_subdivision['inn'] = wrapt_organization[
                    'inn']  # ИНН у филиала/представительства такой же как и у основной организации
                wrapt_subdivision['kpp'] = kpp_for_subdivision(subdivision)
                wrapt_subdivision['ogrn'] = wrapt_organization[
                    'ogrn']  # ОГРН у филиала/представительства такой же как и у основной организации
                wrapt_subdivision['locality'] = location_validation(
                    subdivision.find('АдрМНРФ'))  # правильно находит название города
                wrapt_subdivision['house'] = re.sub(r'[^0-9]', '', item_validation(subdivision, 'АдрМНРФ',
                                                                                   'Дом'))  # отавляет в строке
                # только цыфры
                wrapt_subdivision['name'] = name_subdivision_validation(subdivision, wrapt_subdivision,
                                                                        wrapt_organization['name'])
                try:
                    wrapt_subdivision['main_company'] = OrganizationEgrul.objects.get(
                        ogrn=wrapt_organization['ogrn'], main_company=None).pk  # Ссылка на главную компанию
                except ObjectDoesNotExist:
                    log_in_file(
                        'Ошибка! Не удалось привязать филиал к основной компании. ogrn {}; inn {}; kpp{}'.format(
                            wrapt_subdivision['ogrn'], wrapt_subdivision['inn'], wrapt_subdivision['kpp']), 'error')
                save_in_base(wrapt_subdivision, wrapt_subdivision['kpp'])
            # array_of_organizations.append(wrapt_subdivision)

# def parsing_egrul(file_zip):
#     # list_of_all_organization_ogrn = OrganizationEgrul.objects.values_list('ogrn', flat=True)
#     for file_name in file_zip.namelist():
#         file_parser(file_zip.read(file_name).decode('utf-8'))
#     print('Success!')
