import os

script_path = os.path.abspath("./webex-alert")
work_dir = os.path.abspath("./")
log_file = work_dir + "/webex_cron.log"
python_path = os.path.abspath(".venv/bin/python")

date_cmd = "date +\"%Y-%m-%d %H:%M:%S\""
start_cmd = f"echo '########## Log: Run at $({date_cmd}) ##########' >> " + log_file
py_command = f"{python_path} {script_path}"

command = f"/bin/bash -c \"{start_cmd} && {py_command} >> {log_file} 2>&1\""
comment = "webex"