from django.core.management import BaseCommand

from OrgFromEgrul.organizations.getting_data import select_folder


class Command(BaseCommand):
    help = 'Обновление всей базы данных ЕГРЮЛ'

    def handle(self, *args, **options):
        select_folder()
