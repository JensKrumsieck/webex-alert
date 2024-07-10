from dotenv import dotenv_values
import requests
import webex
from login import login, refresh
from util import root_dir
import os

accesstoken = ""
refreshtoken = ""

# login or read tokens
if os.path.exists(root_dir + "/.secrets"):
    secrets = dotenv_values(root_dir + "/.secrets")
    refreshtoken = secrets.get("REFRESH_TOKEN")
    accesstoken = secrets.get("ACCESS_TOKEN")
else:
    print("could not find .secrets file, starting login server...")
    accesstoken, refreshtoken = login()
    with open(root_dir + "/.secrets", "w") as f:
        f.write(f"ACCESS_TOKEN={accesstoken}\n")
        f.write(f"REFRESH_TOKEN={refreshtoken}\n")

# check valid token
res = requests.get("https://webexapis.com/v1/people/me",
                   headers={"Authorization": f"Bearer {accesstoken}"})
if res.status_code == 401:
    # use refresh token
    accesstoken, refreshtoken = refresh(refreshtoken)
    with open(root_dir + "/.secrets", "w") as f:
        f.write(f"ACCESS_TOKEN={accesstoken}\n")
        f.write(f"REFRESH_TOKEN={refreshtoken}\n")

res = requests.get("https://webexapis.com/v1/people/me",
                   headers={"Authorization": f"Bearer {accesstoken}"})
if res.status_code != 200:
    print("Could not authenticate, please try again")
    os.remove(".secrets")
    exit()

print("Logged in as " + res.json()["displayName"])
emails = []
exit()
# get all emails
#emails = webex.getAllEmails(accesstoken) # uncomment to update all emails

# get emails for specific rooms
#emails = webex.getRoomUserEmails(webex.roomIds["FDM"], accesstoken) # test with different rooms, options: "FDM", "44er", "IT"

# hardcoded list of emails
emails = ["jens.krumsieck@thuenen.de"]#, "florian.hoedt@thuenen.de", "harald.vonwaldow@thuenen.de"] # testing purpose, DANGER: if this line is commented you'll add whole thünen to room!!! 

# create room if not stored already
room_id = ""

if os.path.exists(root_dir + "/.room_id"):
    with open(root_dir + "/.room_id", "r") as f:
        room_id = f.readline()

if not room_id:
    options= {"title": "[Test] IT Security Alerts", "isLocked": True, "isPublic": False, "isAnnouncementOnly": True, "description": "This Room is used to broadcast IT Security Alerts"}
    room = webex.createRoom(options, accesstoken)
    with open(root_dir + "/.room_id", "w") as f:
        f.write(room["id"])
    room_id = room["id"]

# add users to room by their Ids
user_ids = webex.getUserIds(emails, accesstoken)
print(f"Found {len(user_ids)} users")

# get users already in that room
room_users_ids = webex.getRoomUserIds(room_id, accesstoken)
print(len(room_users_ids), "users already in room")

user_ids = list(set(user_ids) - set(room_users_ids))
print(len(user_ids), "users to add")

# add remaining users to room
for user_id in user_ids:
    res = webex.addUserToRoom(user_id, room_id, accesstoken)
    if res.status_code != 200:
        print(f"Could not add user {user_id} to room - statuscode: {res.status_code}")

# (re-)grant mod rights
special_users = ["jens.krumsieck@thuenen.de", "florian.hoedt@thuenen.de", "helge.ziese@thuenen.de", "beate.oerder@thuenen.de", "thomas.firley@thuenen.de"]
special_ids = webex.getUserIds(special_users, accesstoken)

for user_id in special_ids:
    res = webex.grantModeratorRightsInRoom(user_id, room_id, accesstoken)
    if res.status_code != 200:
        print(f"Could not grant user {user_id} moderator rights - statuscode: {res.status_code}")
    else:
        print(f"Granted user {user_id} moderator rights")