import os
import dotenv
import webex

dotenv.load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

webex.login(client_id, client_secret)
webex.refresh_token(client_id, client_secret)