from crontab import CronTab
from cron_util import comment

cron = CronTab(user=True)

for job in cron:
    if comment in job.comment:
        cron.remove(job)

cron.write()
print("Removed Cronjob!")

print("remaining cronjobs:")
for job in cron:
    print(job)