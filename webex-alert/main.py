import os
import dotenv
import webex

dotenv.load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
webex.auth(client_id, client_secret) # type: ignore