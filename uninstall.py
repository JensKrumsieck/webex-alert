from crontab import CronTab
from __util import comment

cron = CronTab(user=True)

cron.remove_all()
cron.write()
print("Removed Cronjob!")

print("remaining cronjobs:")
for job in cron:
    print(job)