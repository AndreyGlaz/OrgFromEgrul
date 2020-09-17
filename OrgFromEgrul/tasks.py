from .celery import app
import logging


logging.basicConfig(filename='parsing_egrul.log', format='%(asctime)s-%(levelname)s:%(message)s', level=logging.INFO)


@app.task()
def parsing_and_save(xml_file):
    from OrgFromEgrul.organizations.parsing import file_parser
    file_parser(xml_file)


@app.task()
def parsing_and_save_egrip(xml_file):
    from .organizations.parsing_egrip import file_parser_egrip
    file_parser_egrip(xml_file)

