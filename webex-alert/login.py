from typing import Tuple
import requests
import serve

def login() -> Tuple[str, str]:
    # TODO: get from env
    client_id = "C0822806d1b484c90e50f08bc12022fc1c23d1cee232b4a56b4207f349c05d9f7"
    # TODO: get from env
    client_secret = "226f416d9b338da9439ced1e98ad3575c9efbb0b296f3cbc9035d4cfac16f952"
    scope = "spark:all%20spark:kms"
    redirect_url = "http://localhost:8080/auth"
    auth_url = f"https://webexapis.com/v1/authorize?client_id={
        client_id}&response_type=code&redirect_uri={redirect_url}&scope={scope}"
    login_url = "https://webexapis.com/v1/access_token"

    # get auth code by logging in
    print(f"Please Login to Webex by visiting {auth_url}")
    auth_code = serve.run()

    # get access token and refresh token
    options = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": auth_code,
        "redirect_uri": redirect_url
    }
    response = requests.post(login_url, data=options)
    access_token = response.json()["access_token"] 
    refresh_token = response.json()["refresh_token"]

    print("Login successful!")
    return (access_token, refresh_token)