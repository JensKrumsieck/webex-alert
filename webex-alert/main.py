import os
import logging
import coloredlogs
import webex
from util import root_dir

coloredlogs.install(level='INFO', fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("webex-alert")

logger.info("Starting Webex Alert Script")
accesstoken, refreshtoken = webex.authenticate()

emails = []
# get all emails
#emails = webex.getAllEmails(accesstoken) # uncomment to update all emails

# get emails for specific rooms
emails = webex.getRoomUserEmails(webex.roomIds["44er"], accesstoken) # test with different rooms, options: "FDM", "44er", "IT"

# hardcoded list of emails
# emails = ["jens.krumsieck@thuenen.de"]#, "florian.hoedt@thuenen.de", "harald.vonwaldow@thuenen.de"] # testing purpose, DANGER: if this line is commented you'll add whole thünen to room!!! 

# create room if not stored already
room_id = ""

if os.path.exists(root_dir + "/.room_id"):
    with open(root_dir + "/.room_id", "r") as f:
        room_id = f.readline()

if not room_id:
    options= {"title": "❗ [Test] Thünen IT Security Alerts ❗", "isLocked": True, "isPublic": False, "isAnnouncementOnly": True, "description": "This Room is used to broadcast IT Security Alerts"}
    room = webex.createRoom(options, accesstoken)
    with open(root_dir + "/.room_id", "w") as f:
        f.write(room["id"])
    room_id = room["id"]

# add users to room by their Ids
user_ids = webex.getUserIds(emails, accesstoken)
logger.info(f"Found %s users", len(user_ids))

# get users already in that room
room_users_ids = webex.getRoomUserIds(room_id, accesstoken)
logger.info("%s users already in room", len(room_users_ids))

user_ids = list(set(user_ids) - set(room_users_ids))
logger.info("%s users to add", len(user_ids))

# add remaining users to room
for user_id in user_ids:
    res = webex.addUserToRoom(user_id, room_id, accesstoken)
    if res.status_code != 200:
        logger.error(f"Could not add user {user_id} to room - statuscode: {res.status_code}")

# (re-)grant mod rights
special_users = ["jens.krumsieck@thuenen.de", "florian.hoedt@thuenen.de", "helge.ziese@thuenen.de", "beate.oerder@thuenen.de", "thomas.firley@thuenen.de"]
special_ids = webex.getUserIds(special_users, accesstoken)

for user_id in special_ids:
    res = webex.grantModeratorRightsInRoom(user_id, room_id, accesstoken)
    if res.status_code != 200:
        logger.error(f"Could not grant user {user_id} moderator rights - statuscode: {res.status_code}")
    else:
        logger.info(f"Granted user {user_id} moderator rights")