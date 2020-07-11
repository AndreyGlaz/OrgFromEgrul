from OrgFromEgrul.organizations.getting_data import select_folder_update
from .celery import app
import logging

logging.basicConfig(filename='parsing_egrul.log', format='%(asctime)s-%(levelname)s:%(message)s', level=logging.INFO)


@app.task(ignore_result=True)
def start_update():
    logging.info('Starting update base...')
    select_folder_update()
    logging.info('The base was successfully updated!!!')


@app.task()
def parsing_and_save(xml_file):
    from OrgFromEgrul.organizations.parsing import file_parser
    file_parser(xml_file)
