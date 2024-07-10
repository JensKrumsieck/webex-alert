from crontab import CronTab
from __util import command, comment

cron = CronTab(user=True)

job = cron.new(command=command, comment=comment)
job.minute.every(1)

cron.write()
print("Added Cronjob!")