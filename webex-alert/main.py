import os
import dotenv
import webex
import keyring
import argparse

parser = argparse.ArgumentParser(description="Webex Alert CLI")
parser.add_argument("--logout", action="store_true", help="Logout from Webex")
args = parser.parse_args()

dotenv.load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

if args.logout:
    keyring.delete_password("webex", "access_token")
    keyring.delete_password("webex", "refresh_token")
    exit(0)

webex.auth(client_id, client_secret)  # type: ignore

users = webex.get_all_users()
room = webex.get_room("Thünen-Notfälle")
if not room:
    room_id = webex.create_room("Thünen-Notfälle", "Notfallmeldungen Thünen-Institut")
    room = webex.get_room("Thünen-Notfälle")
print(f"Found {len(users)} users and room: {room['title']}") # type: ignore