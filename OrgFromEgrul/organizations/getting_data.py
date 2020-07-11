import os
from time import sleep

import celery
import requests

from OrgFromEgrul.organizations.models import SuccessfullyProcessedZip
from datetime import date, timedelta
import zipfile
import tempfile
import urllib3
import logging

logging.basicConfig(filename='parsing_egrul.log', format='%(asctime)s-%(levelname)s:%(message)s', level=logging.INFO)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parent_dir = os.path.dirname(os.path.abspath(os.curdir))
egrul_dir = 'https://ftp.egrul.nalog.ru/EGRUL/'
cert_dir = os.path.join(parent_dir, 'OrgFromEgrul', 'cert-key.pem')
list_processed_zip = SuccessfullyProcessedZip.objects.values_list('url_zip', flat=True)


# Добавляет ноль в начало значнеия
def zero_plus(value):
    if value < 10:
        return '0' + str(value)
    else:
        return str(value)


# Удаляет папку и все файлы в ней
def delete_folder(path):
    for file_name in os.listdir(path):
        os.remove(path + file_name)
    os.rmdir(path)


# Открытие Zip архива и сохранение в папку
def open_and_unpacking_zip(data_zip, path):
    file = tempfile.TemporaryFile()
    file.write(data_zip)
    file_zip = zipfile.ZipFile(file)
    file_zip.extractall(path[27:])
    from OrgFromEgrul.tasks import parsing_and_save
    tasks = celery.group(
        [parsing_and_save.s(xml_file=str(path[27:] + file_name)) for file_name in
         os.listdir(path[27:])])
    group_task = tasks.apply_async()
    while not group_task.ready():
        sleep(0.5)
    logging.info('Success parsing zip! ' + path[27:])
    processed = SuccessfullyProcessedZip(url_zip=path[27:-1] + '.zip')
    processed.save()
    delete_folder(path[27:])
    file.close()
    file_zip.close()


# Проверка содержимого папки и отправка на открытие
def check_file(file_path):
    file_count = 1
    miss = 0
    while miss < 3:
        zip_path = file_path + '_' + str(file_count) + '.zip'
        if zip_path[27:] not in list_processed_zip:
            response_zip = requests.get(zip_path, verify=False, cert=cert_dir)
            if response_zip.headers['Content-Type'] == 'application/download':
                logging.info(zip_path)
                print(zip_path)
                open_and_unpacking_zip(response_zip.content, file_path + '_' + str(file_count) + '/')
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
    # logfile.close()


# Функция для запуска её каждую ночь, накатывает изменения за прошедшую неделю
def select_folder_update():
    for i in range(7, 0, -1):
        temp_date = date.today() - timedelta(days=i)
        forming_and_use_date(temp_date.day, temp_date.month, temp_date.year)
