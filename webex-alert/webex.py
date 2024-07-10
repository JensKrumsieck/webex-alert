import requests
import logging
from typing import List
from util import root_dir

logger = logging.getLogger("webex-alert:webex")

def Me(accesstoken: str):
    logger.debug("Getting current users info")
    return requests.get("https://webexapis.com/v1/people/me", headers={"Authorization": f"Bearer {accesstoken}"})

def getAllEmails(accesstoken: str):
    logger.debug("Getting all emails")
    # get all colleagues
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                # does that include all persons?
                "r", "s", "t", "u", "v", "w", "x", "y", "z", "ä", "ö", "ü"]
    emails = []
    for letter in alphabet:
        res = requests.get(f"https://webexapis.com/v1/people?displayName={letter}&max=1000", headers={"Authorization": f"Bearer {accesstoken}"})
        if res.status_code != 200:
            logger.error("could not get colleagues for letter " + letter)
            continue
        for person in res.json()["items"]:
            for email in person["emails"]:
                emails.append(email)

    emails = list(set(emails))  # make unique list
    with open(root_dir + "/emails.txt", "w") as f:
        for email in emails:
            f.write(email + "\n")  

    logger.info(f"Found {len(emails)} emails")
    return emails

roomIds = {
    "FDM": "Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vNjQ4MDViODAtMDI3Yi0xMWVkLWI1ZDgtZmJlZWY5MzE2NGZh",
    "44er": "Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vYzFlMzNjMTAtZGU2NS0xMWViLThjMGYtY2ZiZWQzYmRiMDFi",
    "IT": "Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vYjIwZjczOTAtMTQ0OC0xMWViLWE1OTctYjk2N2FkNmJiOWNm"
}

def createRoom(options, accesstoken: str):
    logger.debug(f"Creating new room with options {options}")
    # creates a room
    return requests.post("https://webexapis.com/v1/rooms", headers={"Authorization": f"Bearer {accesstoken}"}, json=options).json()

def getUserIds(emails: List[str], accesstoken: str) -> List[str]:
    # gets user Ids
    users = []
    for mail in emails:
        user = requests.get(f"https://webexapis.com/v1/people?email={mail}", headers={"Authorization": f"Bearer {accesstoken}"}).json()
        if user["items"]:
            users.append(user["items"][0]["id"])
        else:
            logger.error(f"User with email {mail} not found")
    return users

def getRoomUsers(room_id: str, accesstoken: str):
    logger.debug(f"Getting users for room {room_id}")
    response = requests.get("https://webexapis.com/v1/memberships", headers={"Authorization": f"Bearer {accesstoken}"}, params={"roomId": room_id})
    if(response.status_code != 200):
        logger.error("could not get room users")
        return []
    return response.json()["items"]

def getRoomUserIds(room_id: str, accestoken: str):
    logger.debug(f"Getting ids for users in room {room_id}")
    users = getRoomUsers(room_id, accestoken)
    if(users == []):
        return []
    return [user["personId"] for user in users]

def getRoomUserEmails(room_id: str, accesstoken: str):    
    logger.debug(f"Getting emails for users in room {room_id}")
    users = getRoomUsers(room_id, accesstoken)
    if(users == []):
        return []
    return [user["personEmail"] for user in users]           

def addUserToRoom(user_id: str, room_id: str, accesstoken: str):
    logger.debug(f"Adding user {user_id} to room {room_id}")
    return requests.post("https://webexapis.com/v1/memberships", headers={"Authorization": f"Bearer {accesstoken}"}, 
                         json={"roomId": room_id, "personId": user_id})

def grantModeratorRightsInRoom(user_id: str, room_id: str, accesstoken: str):    
    logger.debug(f"Grant moderations rights to user {user_id} in room {room_id}")
    # get membership id
    response = requests.get("https://webexapis.com/v1/memberships", headers={"Authorization": f"Bearer {accesstoken}"}, params={"roomId": room_id, "personId": user_id})
    response_json = response.json()
    if response.status_code != 200 or not response_json["items"] or len(response_json["items"]) == 0:
        logger.error(f"could not get membership id for {user_id} in room")
        response.status_code = 404 # manually set to 404
        return response
    membership_id = response.json()["items"][0]["id"]
    
    # grant moderator rights
    return requests.put(f"https://webexapis.com/v1/memberships/{membership_id}", headers={"Authorization": f"Bearer {accesstoken}"}, 
                        json={"isModerator": True})