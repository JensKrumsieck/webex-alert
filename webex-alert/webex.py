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

def addUserToRoom(user_id: str, room_id: str, accesstoken: str):
    return requests.post("https://webexapis.com/v1/memberhips", headers={"Authorization": f"Bearer {accesstoken}"}, json={"roomId": room_id, "personId": user_id})