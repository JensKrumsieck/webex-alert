import logging
import coloredlogs
import webex
from config import Config

coloredlogs.install(level='INFO', fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("webex-alert")

logger.info("Starting Webex Alert Script")
config = Config() # config object
accesstoken, refreshtoken = webex.authenticate()

emails = []
# get all emails
#emails = webex.getAllEmails(accesstoken) # uncomment to update all emails

# get emails for specific rooms
emails = webex.getRoomUserEmails(webex.roomIds["44er"], accesstoken) # test with different rooms, options: "FDM", "44er", "IT"

# create room if not stored already
room_id = config.get_room_id()

if not room_id or room_id == "":
    options= config.get_room_options()
    room = webex.createRoom(options, accesstoken)
    room_id = room["id"]
    config.set_room_options(room)
    logger.info(f"Created room with id {room_id}")
    
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
special_users = config.get_moderators()
special_ids = webex.getUserIds(special_users, accesstoken)

for user_id in special_ids:
    res = webex.grantModeratorRightsInRoom(user_id, room_id, accesstoken)
    if res.status_code != 200:
        logger.error(f"Could not grant user {user_id} moderator rights - statuscode: {res.status_code}")
    else:
        logger.info(f"Granted user {user_id} moderator rights")