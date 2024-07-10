# Webex Alerts
Creates an Alert Room for Webex and adds all colleagues to it. The Room is a broadcast only room 

Upon the first run the script will ask for authentification. Click the provided link (in terminal) to login to Webex. Access and Refresh Tokens will be stored in a .secrets file. 

> **[- WARNING -]** This will add all your Colleagues to a webex room

## How to use
1. Register an [integration app](https://developer.webex.com/my-apps/new/integration) for the webex api and enter http://localhost:8080/ to Redirect URI.
Copy client id and client secret in a file called .env, like in the example:
```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

2. Install requirements
``` bash
pip install -r requirements.txt
```

3. Execute Script
``` bash
python3 webex-alert
```

4. Login with your Webex Credentials
The Script will prompt you to visit the webex website to enter your credentials, which will then result in access and refresh tokens, stored on disk locally.

## CronJobs
The script can also be executed via cron. You can simply execute the install or uninstall script to add or remove the cron job. Execution frequency can be edited in the install script. The outputs will be logged in file `webex_cron.log`.
```bash
python cron_install.py
python cron_uninstall.py
```

## Devcontainer
A VSCode Devcontainer is available for development. The Container will install all requirements in a virtual environment (venv) and start the cron service.
The virtual enviroment will be activated automatically after starting the devcontainer.