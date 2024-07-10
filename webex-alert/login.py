from typing import Tuple
from dotenv import dotenv_values
import requests
import serve
from util import root_dir

token_url = "https://webexapis.com/v1/access_token"

def read_secrets() -> Tuple[str, str]:    
    config = dotenv_values(root_dir + "/.env")
    client_id = config.get("CLIENT_ID")
    client_secret = config.get("CLIENT_SECRET")
    return (client_id, client_secret)

def login() -> Tuple[str, str]:
    client_id, client_secret = read_secrets()
    scope = "spark:all%20spark:kms"
    redirect_url = "http://localhost:8080/auth"
    auth_url = f"https://webexapis.com/v1/authorize?client_id={
        client_id}&response_type=code&redirect_uri={redirect_url}&scope={scope}"

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
    response = requests.post(token_url, data=options)
    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]

    print("Login successful!")
    return (access_token, refresh_token)


def refresh(refreshToken: str) -> Tuple[str, str]:

    client_id, client_secret = read_secrets()

     # get access token and refresh token
    options = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refreshToken
    }

    response = requests.post(token_url, data=options)
    print(f"requesting refresh token received status {response.status_code}\n{response.json()["message"]}")
    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]

    print("Got new token by using refresh token")
    return (access_token, refresh_token)