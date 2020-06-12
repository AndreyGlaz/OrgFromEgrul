from OrgFromEgrul.organizations.parsing import parsing_egrul
from .celery import app


@app.task
def debug_task():
    # parsing_egrul()
    print('all okey')
