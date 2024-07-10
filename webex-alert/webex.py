import requests
from typing import List

def getAllEmails(accesstoken: str):
    # get all colleagues
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                # does that include all persons?
                "r", "s", "t", "u", "v", "w", "x", "y", "z", "ä", "ö", "ü"]
    emails = []
    for letter in alphabet:
        res = requests.get(f"https://webexapis.com/v1/people?displayName={letter}&max=1000", headers={"Authorization": f"Bearer {accesstoken}"})
        if res.status_code != 200:
            print("could not get colleagues for letter " + letter)
            continue
        for person in res.json()["items"]:
            for email in person["emails"]:
                emails.append(email)

    emails = list(set(emails))  # make unique list
    print(f"Found {len(emails)} emails")
    with open("emails.txt", "w") as f:
        for email in emails:
            f.write(email + "\n")

def get44erEmails(accesstoken: str):
    roomId = "Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vYzFlMzNjMTAtZGU2NS0xMWViLThjMGYtY2ZiZWQzYmRiMDFi"
    users = getRoomUsers(roomId, accesstoken)
    return [user["personEmail"] for user in users]

def createRoom(options, accesstoken: str):
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
            print(f"User with email {mail} not found")
    return users

def getRoomUsers(room_id: str, accesstoken: str):
    response = requests.get("https://webexapis.com/v1/memberships", headers={"Authorization": f"Bearer {accesstoken}"}, params={"roomId": room_id})
    if(response.status_code != 200):
        print("could not get room users")
        return []
    return response.json()["items"]

def getRoomUserIds(room_id: str, accestoken: str):
    users = getRoomUsers(room_id, accestoken)
    if(users == []):
        return []
    return [user["personId"] for user in users]
                                                                         
def addUserToRoom(user_id: str, room_id: str, accesstoken: str):
    return requests.post("https://webexapis.com/v1/memberships", headers={"Authorization": f"Bearer {accesstoken}"}, 
                         json={"roomId": room_id, "personId": user_id})

def grantModeratorRightsInRoom(user_id: str, room_id: str, accesstoken: str):
    # get membership id
    response = requests.get("https://webexapis.com/v1/memberships", headers={"Authorization": f"Bearer {accesstoken}"}, params={"roomId": room_id, "personId": user_id})
    response_json = response.json()
    if response.status_code != 200 or not response_json["items"] or len(response_json["items"]) == 0:
        print(f"could not get membership id for {user_id} in room")
        response.status_code = 404 # manually set to 404
        return response
    membership_id = response.json()["items"][0]["id"]
    
    # grant moderator rights
    return requests.put(f"https://webexapis.com/v1/memberships/{membership_id}", headers={"Authorization": f"Bearer {accesstoken}"}, 
                        json={"isModerator": True})