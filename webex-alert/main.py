from dotenv import dotenv_values
import requests
import webex
from login import login, refresh
import os

accesstoken = ""
refreshtoken = ""

# login or read tokens
if os.path.exists(".secrets"):
    secrets = dotenv_values(".secrets")
    refreshtoken = secrets.get("REFRESH_TOKEN")
    accesstoken = secrets.get("ACCESS_TOKEN")
else:
    accesstoken, refreshtoken = login()
    with open(".secrets", "w") as f:
        f.write(f"ACCESS_TOKEN={accesstoken}\n")
        f.write(f"REFRESH_TOKEN={refreshtoken}\n")

# check valid token
res = requests.get("https://webexapis.com/v1/people/me",
                   headers={"Authorization": f"Bearer {accesstoken}"})
if res.status_code == 401:
    # use refresh token
    accesstoken, refreshtoken = refresh(refreshtoken)
    with open(".secrets", "w") as f:
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
# get all emails
# webex.getAllEmails(accesstoken) # uncomment to update all emails
#with open("emails.txt", "r") as f:
#    emails = f.readlines()

emails = ["jens.krumsieck@thuenen.de"] # testing purpose, DANGER: if this line is commented you'll add whole thünen to room!!! 

# create room if not stored already
room_id = ""

if os.path.exists(".room_id"):
    with open(".room_id", "r") as f:
        room_id = f.readline()

public_room = False # set to true for production

if not room_id:
    options= {"title": "IT Security Alerts", "isLocked": True, "isPublic": public_room, "isAnnouncementOnly": True, "description": "This Room is used to broadcast IT Security Alerts"}
    room = webex.createRoom(options, accesstoken)
    with open(".room_id", "w") as f:
        f.write(room["id"])
    room_id = room["id"]

# add users to room by their Ids
users = webex.getUserIds(emails, accesstoken)

for user in users:
    webex.addUserToRoom(user, room_id, accesstoken)