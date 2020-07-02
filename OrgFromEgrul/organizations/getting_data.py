import os
import requests
from OrgFromEgrul.organizations.parsing import file_parser
from datetime import date, timedelta
import zipfile
import tempfile
import urllib3
import logging

logging.basicConfig(format='%(asctime)d-%(levelname)s:%(message)s', level=logging.INFO,
                    filename='/home/admin/egrul_base_log/parsing_egrul.log')


def log_in_file(string, level):
    if level == 'info':
        logging.info(string)
    elif level == 'error':
        logging.error(string)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parent_dir = os.path.dirname(os.path.abspath(os.curdir))
egrul_dir = 'https://ftp.egrul.nalog.ru/EGRUL/'
cert_dir = os.path.join(parent_dir, 'OrgFromEgrul', 'cert-key.pem')


# Добавляет ноль в начало значнеия
def zero_plus(value):
    if value < 10:
        return '0' + str(value)
    else:
        return str(value)


# Открытие Zip архива и передача в парсинг
def open_zip(data_zip):
    file = tempfile.TemporaryFile()
    file.write(data_zip)
    file_zip = zipfile.ZipFile(file)
    for file_name in file_zip.namelist():
        file_parser(file_zip.read(file_name).decode('windows-1251'))


# Проверка содержимого папки и отправка на открытие
def check_file(file_path):
    file_count = 1
    miss = 0

    while miss < 3:
        response_zip = requests.get(file_path + '_' + str(file_count) + '.zip', verify=False, cert=cert_dir)
        if response_zip.headers['Content-Type'] == 'application/download':
            log_in_file(file_path, 'info')
            open_zip(response_zip.content)
        else:
            miss += 1
        file_count += 1


# Формирование правильного названия папок из даты и проверка на наличие такой папки
def forming_and_use_date(day, month, year):
    date_delimiter = '.'
    date_file_delimiter = '-'
    temp_date_str = date_delimiter.join([zero_plus(day), zero_plus(month), str(year)])
    temp_date_str_file = date_file_delimiter.join([str(year), zero_plus(month), zero_plus(day)])
    check_file(''.join([egrul_dir, temp_date_str, '/EGRUL_', temp_date_str_file]))


# Прохождение по списку дирректорий (загрузка всей базы)
def select_folder():
    for number_year in range(2018, date.today().year + 1):
        check_file(egrul_dir + '01.01.' + str(number_year) + '_FULL/EGRUL_FULL_' + str(number_year) + '-01-01')
        for number_month in range(1, 13):
            for number_date in range(1, 32):
                forming_and_use_date(number_date, number_month, number_year)


# Функция для запуска её каждую ночь, накатывает изменения за прошедшую неделю
def select_folder_update():
    for i in range(7, 0, -1):
        temp_date = date.today() - timedelta(days=i)
        forming_and_use_date(temp_date.day, temp_date.month, temp_date.year)
