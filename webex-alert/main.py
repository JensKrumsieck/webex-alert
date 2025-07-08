import json
import os
import dotenv
import webex
import keyring
import argparse

parser = argparse.ArgumentParser(description="Webex Alert CLI")
parser.add_argument("--logout", action="store_true", help="Logout from Webex")
parser.add_argument("--delete", action="store_true",
                    help="Delete Room in Webex")
args = parser.parse_args()

if args.logout:
    keyring.delete_password("webex", "access_token")
    keyring.delete_password("webex", "refresh_token")
    print("Logged out from Webex.")
    exit(0)

# load configuration
dotenv.load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

with open("config.json", mode='r') as f:
    config = json.load(f)
title = config["title"]
description = config["description"]
moderators = config["moderators"]

webex.auth(client_id, client_secret)  # type: ignore

if args.delete:
    room = webex.get_room(title)
    if room:
        webex.delete_room(room["id"])
        print(f"Room '{room['title']}' deleted.")
        exit(0)

users = webex.get_all_users()

room = webex.get_or_create_room(title, description)
if not room:
    print(f"Could not find or create the room '{title}'.")
    exit(1)

for user in users:
    if not webex.user_is_in_room(user["id"], room["id"]):
        print(user["displayName"] + " will be added to room " + room["title"] + " as " +
              ("moderator" if any(email in moderators for email in user["emails"]) else "member"))
        webex.add_user_to_room(
            user["id"], room["id"], any(email in moderators for email in user["emails"]))

print(f"All users added to room '{room['title']}'.")
