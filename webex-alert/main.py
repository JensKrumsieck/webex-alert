from dotenv import dotenv_values
import server
import requests

bearerToken = dotenv_values(".env").get("BEARER_TOKEN")

if not bearerToken: 
    app = server.app()
    app.run()
    bearerToken = app.token
    with open(".env", "a") as f:
        f.write(f"BEARER_TOKEN={bearerToken}\n")

res = requests.get("https://webexapis.com/v1/people/me", headers={"Authorization": f"Bearer {bearerToken}"})
print("logged in as " + res.json()["displayName"])

# TODO: cache id after first run
room = requests.post("https://webexapis.com/v1/rooms", headers={"Authorization": f"Bearer {bearerToken}"}, json={"title": "Test"}).json() # TODO: options for room

emails = ["jens.krumsieck@thuenen.de"]

users = []
for mail in emails:
    user = requests.get(f"https://webexapis.com/v1/people?email={mail}", headers={"Authorization": f"Bearer {bearerToken}"}).json()
    if user["items"]:
        users.append(user["items"][0]["id"])
    else:
        print(f"User with email {mail} not found")

for users in users:
    requests.post("https://webexapis.com/v1/memberhips", headers={"Authorization": f"Bearer {bearerToken}"}, json={"roomId": room["id"], "personId": user})