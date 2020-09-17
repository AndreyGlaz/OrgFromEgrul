from django.core.management import BaseCommand

from OrgFromEgrul.organizations.getting_data import select_folder_update
import logging

logging.basicConfig(filename='parsing_egrul.log', format='%(asctime)s-%(levelname)s:%(message)s', level=logging.INFO)


class Command(BaseCommand):
    help = 'Ежедневное обновление базы данных ЕГРЮЛ'

    def add_arguments(self, parser):
        parser.add_argument(
            '-egrip',
            action='store_true',
            default=False,
            help='Парсинг ЕГРИП'
        )

    def handle(self, *args, **options):
        logging.info('Starting daily update base...')
        current_type = 'EGRIP' if options.get('egrip') else 'EGRUL'
        select_folder_update(current_type)
        logging.info('The base was successfully updated!')
