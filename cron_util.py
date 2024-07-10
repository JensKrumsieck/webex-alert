import os

script_path = os.path.abspath("./webex-alert")
work_dir = os.path.abspath("./")
log_file = work_dir + "/webex_cron.log"
python_path = os.path.abspath(".venv/bin/python")

date_cmd = "echo '########## Log: Run at $(date) ##########' >> " + log_file
py_command = f"{python_path} {script_path}"

command = f"/bin/bash -c \"{date_cmd} && {py_command} >> {log_file} 2>&1\""
comment = "webex"