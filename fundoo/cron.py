from datetime import datetime

from django_cron import CronJobBase, Schedule

from note.models import Notes


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1
    # MIN_NUM_FAILURES = 3

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'fundoo.MyCronJob'
    print("ddd")