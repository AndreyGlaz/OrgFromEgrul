#!/bin/bash

# Запуск воркера Селери в фоновом режиме вместе с beat и запись логов в celery.log
celery -A OrgFromEgrul worker --detach -l info -f celery.log -B

# Запуск проекта
python manage.py runserver 0.0.0.0:8000
