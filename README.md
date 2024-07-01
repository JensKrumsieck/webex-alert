# Webex Alerts
Creates an Alert Room for Webex and adds all colleagues to it. The Room is a broadcast only room 

Upon the first run the script will ask for authentification. Click the provided link to login to Webex. Access and Refresh Tokens will be stored in a .secrets file. 

>[!WARNING] 
>DANGER! This will add all Colleagues to a room, uncomment line 46 in main.py for testing!!!

## Steps:
 - authenticate User
 - get all emails and save them to emails.txt
 - if no room exists, the script will create one and saves its id to a .room_id file
 - the script will add all colleagues to the room

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