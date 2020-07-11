from django.core.management import BaseCommand

from OrgFromEgrul.organizations.getting_data import select_folder
import logging

logging.basicConfig(filename='parsing_egrul.log', format='%(asctime)s-%(levelname)s:%(message)s',  level=logging.INFO)


class Command(BaseCommand):
    help = 'Обновление всей базы данных ЕГРЮЛ'

    def handle(self, *args, **options):
        logging.info('Starting update all base...')
        select_folder()
        logging.info('The base was successfully updated!')
