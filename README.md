# Webex Alerts
Creates an Alert Room for Webex and adds all colleagues to it. The Room is a broadcast only room 

Upon the first run the script will ask for authentification. Click the provided link (in terminal) to login to Webex. Access and Refresh Tokens will be stored in a .secrets file. 

> **[- WARNING -]** This will add all your Colleagues to a webex room

## How to use
### Prerequisites
To use the Webex API you need to register a new [integration app](https://developer.webex.com/my-apps/new/integration) or use the credentials of an existing one.
For the login to work you need to enter http://localhost:8080/ into the Redirect URI(s) field. After creation of the integration a client id and a client secret will be presented. Copy client id and client secret in a file called `.env`, like in the example:
```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```
If you want to use an existing room with the script, you need to get its Id. You can use the Webex API Website for that, by vistiting the [List Rooms Endpoint's documentation](https://developer.webex.com/docs/api/v1/rooms/list-rooms). Save the rooms Id in  `config.ini`.

### Configuration
The configuration will be saved in a file called `config.ini` which looks like the following:
```ini
[webex]
isannouncementonly = True
islocked = True
ispublic = False
title = ❗ [Test] IT Security Alerts ❗
room_id = ACTUAL_ROOM_ID

[moderators]
moderators = emails@separated.xy,by@comma.de
```
if options are not given they will be inferred and added afterwards, except the moderators options which will be ignored if not given.

### Usage of Script
First of all you need to install all python requirements
``` bash
pip install -r requirements.txt
```
When executing the script the first time, you will be prompted to login to Webex with your credentials, which will return an access and refresh token, which will be stored on disk locally in `.secrets`. Delete that file to login again if you have problems or want to change the user.
``` bash
python webex-alert
```
If no RoomId is given the script will create a room with given options.
The script will than call the api to get all users in your organization and add them to the room if they are not in it, yet. After this, the script will grant specified users moderation access to that room. 

## CronJobs
The script can also be executed via cron. You can simply execute the install or uninstall script to add or remove the cron job. Execution frequency can be edited in the install script. The outputs will be logged in file `webex_cron.log`.
```bash
python cron_install.py
python cron_uninstall.py
```