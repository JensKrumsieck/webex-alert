import os
from dotenv import dotenv_values
import requests
import logging
from typing import List, Tuple
from login import login, refresh
from util import root_dir, log_method

logger = logging.getLogger("webex-alert")


@log_method
def authenticate()-> Tuple[str, str]:
    # login or read tokens
    if os.path.exists(root_dir + "/.secrets"):
        secrets = dotenv_values(root_dir + "/.secrets")
        refreshtoken = secrets.get("REFRESH_TOKEN")
        accesstoken = secrets.get("ACCESS_TOKEN")
    else:
        logger.info("could not find a .secrets file\nStarting login procedure...")
        accesstoken, refreshtoken = login()
        with open(root_dir + "/.secrets", "w") as f:
            f.write(f"ACCESS_TOKEN={accesstoken}\n")
            f.write(f"REFRESH_TOKEN={refreshtoken}\n")

    # check valid token
    res = Me(accesstoken)
    retry = res.status_code != 200
    if res.status_code == 401:
        # use refresh token
        accesstoken, refreshtoken = refresh(refreshtoken)
        with open(root_dir + "/.secrets", "w") as f:
            f.write(f"ACCESS_TOKEN={accesstoken}\n")
            f.write(f"REFRESH_TOKEN={refreshtoken}\n")

    if retry:
        res = Me(accesstoken)
        if res.status_code != 200:
            logger.critical("Could not authenticate, please try again")
            os.remove(root_dir + "/.secrets")
            exit()
    
    logger.info("Logged in as " + res.json()["displayName"])
    return (accesstoken, refreshtoken)


@log_method
def Me(accesstoken: str):
    return requests.get("https://webexapis.com/v1/people/me", headers={"Authorization": f"Bearer {accesstoken}"})

@log_method
def getAllEmails(accesstoken: str):
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

@log_method
def createRoom(options, accesstoken: str):
    # creates a room
    return requests.post("https://webexapis.com/v1/rooms", headers={"Authorization": f"Bearer {accesstoken}"}, json=options).json()

@log_method
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

@log_method
def getRoomUsers(room_id: str, accesstoken: str):
    response = requests.get("https://webexapis.com/v1/memberships", headers={"Authorization": f"Bearer {accesstoken}"}, params={"roomId": room_id})
    if(response.status_code != 200):
        logger.error("could not get room users")
        return []
    return response.json()["items"]

@log_method
def getRoomUserIds(room_id: str, accestoken: str):
    users = getRoomUsers(room_id, accestoken)
    if(users == []):
        return []
    return [user["personId"] for user in users]

@log_method
def getRoomUserEmails(room_id: str, accesstoken: str):
    users = getRoomUsers(room_id, accesstoken)
    if(users == []):
        return []
    return [user["personEmail"] for user in users]           

@log_method
def addUserToRoom(user_id: str, room_id: str, accesstoken: str):
    return requests.post("https://webexapis.com/v1/memberships", headers={"Authorization": f"Bearer {accesstoken}"}, 
                         json={"roomId": room_id, "personId": user_id})

@log_method
def grantModeratorRightsInRoom(user_id: str, room_id: str, accesstoken: str):
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