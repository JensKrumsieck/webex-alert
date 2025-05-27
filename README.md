# Webex Alerts
Creates an Alert Room for Webex and adds all colleagues to it. The Room is a broadcast only room 

Upon the first run the script will ask for authentification. Click the provided link (in terminal) to login to Webex. Access and Refresh Tokens will be stored in a .secrets file. 


## How to use
### Prerequisites
To use the Webex API you need to register a new [integration app](https://developer.webex.com/my-apps/new/integration) or use the credentials of an existing one.
For the login to work you need to enter the followig into the Redirect URI(s) field.
```
https://oauth-helper-a.wbx2.com/helperservice/v1/actions/device/callback
https://oauth-helper-r.wbx2.com/helperservice/v1/actions/device/callback
https://oauth-helper-k.wbx2.com/helperservice/v1/actions/device/callback
```
Futhermore the following scopes are needed:
```
spark-admin:people_read
spark:all
```

After creation of the integration a client id and a client secret will be presented. Copy client id and client secret in a file called `.env`, like in the example, also add the desired moderators email adresses separated by spaces:
```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
MODERATORS=emails@of.your moderators@for.room split@by.spaces
```
### Usage of Script
First of all you need to install all python requirements
``` bash
pip install -r requirements.txt
```
When executing the script the first time, you will be prompted to login to Webex with your credentials, which will return an access and refresh token, which will be stored using keyring. Use `python webex-alert --logout` to reset stored credentials.
``` bash
python webex-alert
```
The script will add a room if it does not exists and will add all organization members to the room. Meanwhile it will add admin rights to all users specified.

Moderators need to have `Erweiterter Messaging-Dienst` enabled in Webex Admin Panel to be added via API. Otherwise they can be added manually.

> [!NOTE]
> For Testing you can get an *Admin Sandbox* here: https://developer.webex.com/admin/docs/developer-sandbox-guide