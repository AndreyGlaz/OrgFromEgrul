from OrgFromEgrul.organizations.getting_data import select_folder_update
from .celery import app


@app.task
def debug_task():
    select_folder_update()
    print('all okey')
