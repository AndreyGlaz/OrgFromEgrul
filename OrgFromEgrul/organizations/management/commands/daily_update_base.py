from django.core.management import BaseCommand

from OrgFromEgrul.organizations.getting_data import select_folder_update
import logging

logging.basicConfig(filename='parsing_egrul.log', format='%(asctime)s-%(levelname)s:%(message)s',  level=logging.INFO)


class Command(BaseCommand):
    help = 'Ежедневное обновление базы данных ЕГРЮЛ'

    def handle(self, *args, **options):
        logging.info('Starting daily update base...')
        select_folder_update()
        logging.info('The base was successfully updated!')
