import os
import signal
import threading
from flask import Flask, request, redirect
import requests

client_id = "C0822806d1b484c90e50f08bc12022fc1c23d1cee232b4a56b4207f349c05d9f7" # TODO: get from env
client_secret = "226f416d9b338da9439ced1e98ad3575c9efbb0b296f3cbc9035d4cfac16f952" # TODO: get from env
scope = "spark:all spark:kms"
redirect_url = "http://localhost:8080/auth"
auth_url = f"https://webexapis.com/v1/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_url}&scope={scope}"
login_url = "https://webexapis.com/v1/access_token"

class app:
    def __init__(self):
        self.token = ""
        self.app =self.create_app()
        self.proc = None

    def create_app(self):   
        app = Flask("Webex Login")
        @app.route("/")
        def login():
            return redirect(auth_url)
        
        @app.route("/auth")
        def getToken():
            code = request.args["code"]
            if code:
                options = {
                    "grant_type": "authorization_code",
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "code": code,
                    "redirect_uri": redirect_url        
                }
                response = requests.post(login_url, data=options)
                self.token = response.json()["access_token"] 
                self.exit()
                return "logged in successfully! please close this tab."
            else:
                return "something went wrong!"
        return app

    def __runApp(self):
        self.app.run(host='localhost', port=8080)

    def run(self):
        self.proc = threading.Thread(self.__runApp())
        self.proc.start()
    
    def exit(self):
        pid = os.getpid()
        os.kill(pid, signal.SIGINT)