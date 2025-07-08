import base64
from threading import Thread
import time
import requests
import keyring
from util import qrcode

api_url = "https://webexapis.com/v1"


def get_all_users():
    """
    Fetch all users from Webex API.
    """
    endpoint = f"{api_url}/people?max=1000"
           
    all_users = []
    while endpoint:
        res = requests.get(endpoint, headers=_header())
        if res.status_code != 200:
            print(f"Failed to fetch users: {res.status_code} - {res.text}")
            exit(1)
        data = res.json()
        items = data.get("items", [])
        all_users.extend(items)
        
        if res.links.get('next'):
            endpoint = res.links.get('next')["url"]
        else:
            endpoint = None
    
    return all_users


def create_room(title: str, description: str = "", moderated: bool = True):
    """
    Create a new room in Webex.
    """
    endpoint = f"{api_url}/rooms"
    payload = {
        "title": title,
        "description": description,
        "isLocked": moderated,
        "isAnnouncementOnly": moderated
    }
    res = requests.post(endpoint, headers=_header(), json=payload)
    if res.status_code != 200:
        raise Exception(
            f"Failed to create room: {res.status_code} - {res.text}")


def delete_room(room_id: str):
    """
    Delete a room by its ID.
    """
    endpoint = f"{api_url}/rooms/{room_id}"
    res = requests.delete(endpoint, headers=_header())
    if res.status_code != 204:
        raise Exception(
            f"Failed to delete room: {res.status_code} - {res.text}")


def get_room(title: str) -> dict | None:
    """
    Get a room by its title.
    """
    endpoint = f"{api_url}/rooms"
    res = requests.get(endpoint, headers=_header())
    if res.status_code != 200:
        print(f"Failed to get room: {res.status_code} - {res.text}")
        exit(1)
    return next((room for room in res.json()["items"] if room["title"] == title), None)


def get_or_create_room(title: str, description: str = "") -> dict | None:
    """
    Get a room by its title, or create it if it doesn't exist.
    """
    # with this we assert the current admin user is in the room if it exists
    room = get_room(title)
    if not room:
        create_room(title, description)
        room = get_room(title)

    if not room:
        print(f"Could not find or create the room '{title}'.")
        exit(1)

    return room


def user_is_in_room(user_id: str, room_id: str) -> bool:
    """
    Check if a user is in a specific room.
    """
    endpoint = f"{api_url}/memberships"
    params = {"roomId": room_id, "personId": user_id}
    res = requests.get(endpoint, headers=_header(), params=params)
    return res.status_code == 200 and len(res.json()["items"]) > 0


def add_user_to_room(user_id: str, room_id: str, mod: bool = False) -> bool:
    """
    Add a user to a specific room.
    """
    endpoint = f"{api_url}/memberships"
    payload = {
        "roomId": room_id,
        "personId": user_id,
        "isModerator": mod
    }
    res = requests.post(endpoint, headers=_header(), json=payload)

    # some users can not be added to rooms as moderators
    if res.status_code == 403 and mod:
        print(
            "User could not be added as moderator, added as member instead.")
    elif res.status_code != 200:
        if res.headers.get("Retry-After"):
            sleep_time = int(res.headers.get("Retry-After"))            
            print(f"Rate Limit Exceeded: Waiting {sleep_time}s")
            time.sleep(sleep_time)
            return False
        raise Exception(
            f"Failed to add user to room: {res.status_code} - {res.text}")
    return True

def auth(client_id: str, client_secret: str):
    """
    Authenticate with Webex API using OAuth2 Device Authorization Grant.
    """
    res = _me()
    if res.status_code == 401 and keyring.get_password("webex", "refresh_token"):
        _refresh_token(client_id, client_secret)
    elif res.status_code != 200 and res.status_code != 429:
        _login(client_id, client_secret)
        res = _me()
    elif res.status_code == 429:
        print("Rate limit exceeded. Please try again later.")
        exit(1)

    if res.status_code == 200:
        print(f"Logged in as \033[1m{res.json()['displayName']}\033[0m")
    else:
        print(f"Failed to log in: {res.status_code} - {res.text}")
        exit(1)


def _header():
    return {"Authorization": f"Bearer {keyring.get_password('webex', 'access_token')}"}


def _me():
    endpoint = f"{api_url}/people/me"
    return requests.get(endpoint, headers=_header())


session = {}


def _start_session(data):
    session['access_token'] = data['access_token']
    session['refresh_token'] = data['refresh_token']
    session['expires_in'] = data['expires_in']

    keyring.set_password("webex", "access_token", session['access_token'])
    keyring.set_password("webex", "refresh_token", session['refresh_token'])


def _wait_for_login(device_code: str, client_id: str, client_secret: str):
    endpoint = f"{api_url}/device/token"
    credentials = f"{client_id}:{client_secret}"
    headers = {
        "Authorization": f'Basic {base64.b64encode(credentials.encode()).decode()}'}
    payload = {
        'client_id': f'{client_id}',
        'device_code': f'{device_code}',
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
    }

    while True:
        time.sleep(2)
        res = requests.post(endpoint, headers=headers, data=payload)

        if res.status_code == 200:
            _start_session(res.json())
            break
        elif res.status_code == 400:
            print(
                f"Response Code: {res.status_code}, Message: {res.json()['errors'][0]['description']}")


def _login(client_id: str, client_secret: str):
    endpoint = f"{api_url}/device/authorize"
    payload = {
        "client_id": client_id,
        "scope": "spark:all spark:kms spark-admin:people_read",
    }
    res = requests.post(endpoint, data=payload)

    if res.status_code != 200:
        raise Exception(
            f"Failed to reach login endpoint: {res.status_code} - {res.text}")

    data = res.json()
    qrcode(data['verification_uri'])
    print(f"Visit \033[1m{data['verification_uri']}\033[0m and \nenter the code \033[1m{data['user_code']}\033[0m to authorize the application.")

    thread = Thread(target=_wait_for_login, args=(
        data['device_code'], client_id, client_secret))
    thread.start()
    # Wait for the thread to complete
    thread.join()
    return


def _refresh_token(client_id: str, client_secret: str):
    endpoint = f"{api_url}/access_token"
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": keyring.get_password("webex", "refresh_token")
    }

    res = requests.post(endpoint, headers=headers, data=payload)
    if res.status_code != 200:
        raise Exception(
            f"Failed to obtain refresh token: {res.status_code} - {res.text}")

    _start_session(res.json())
