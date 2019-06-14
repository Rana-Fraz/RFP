from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    # code = 'my_app.my_cron_job'    # a unique code
    code = "rfp.my_cron_job"

    def do(self):
        # run()
        print('ALi Raza')

def run():
    print('Ali Raza')
