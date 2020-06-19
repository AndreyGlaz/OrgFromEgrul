from OrgFromEgrul.organizations.parsing import file_parser

import os
from datetime import date, timedelta
import zipfile

parent_dir = os.path.dirname(os.path.abspath(os.curdir))
egrul_dir = os.path.join(parent_dir, 'OrgFromEgrul', 'EGRUL')
list_dir_egrul = os.listdir(egrul_dir)


def start_getting_data():
    # file_zip = zipfile.ZipFile('new_folder.zip', 'r')
    # parsing_egrul(file_zip)
    # Список директорий на FTP-сервере ЕГРЮЛ (названия из дат)
    select_folder()


# Добавляет ноль в начало значнеия
def zero_plus(value):
    if value < 10:
        return '0' + str(value)
    else:
        return str(value)


# Открытие Zip архива и передача в парсинг
def open_zip(zip_path):
    file_zip = zipfile.ZipFile(zip_path, 'r')
    print(file_zip)
    for file_name in file_zip.namelist():
        print(file_name, file_zip.getinfo(file_name))
        file_parser(file_zip.read(file_name).decode('windows-1251'))


# Проверка содержимого папки и отправка на открытие
def check_folder(folder_path):
    if os.path.exists(folder_path):
        list_zip = os.listdir(folder_path)
        for name_zip in list_zip:
            open_zip(os.path.join(folder_path, name_zip))
    else:
        print('Don`t exists folder ' + folder_path)


# Формирование правильного названия папок из даты и проверка на наличие такой папки
def forming_and_use_date(day, month, year):
    date_delimiter = '.'
    temp_date_str = date_delimiter.join([zero_plus(day), zero_plus(month), str(year)])
    if temp_date_str in list_dir_egrul:
        check_folder(os.path.join(egrul_dir, temp_date_str))


# Прохождение по списку дирректорий (загрузка всей базы)
def select_folder():
    date_delimiter = '.'
    for number_year in range(2016, date.today().year + 1):
        check_folder(os.path.join(egrul_dir, '01.01.' + str(number_year) + '_FULL'))
        for number_month in range(1, 13):
            for number_date in range(1, 32):
                forming_and_use_date(number_date, number_month, number_year)


# Функция для запуска её каждую ночь, накатывает изменения за прошедшую неделю
def select_folder_update():
    for i in range(7, 0, -1):
        temp_date = date.today() - timedelta(days=i)
        forming_and_use_date(temp_date.day, temp_date.month, temp_date.year)
