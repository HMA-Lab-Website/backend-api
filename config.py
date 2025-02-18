import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import base64
import json

# Load environment variables from .env file
load_dotenv()

firebase_json_base64 = os.getenv("FIREBASE_CREDENTIALS_BASE64")
firebase_json_str = base64.b64decode(firebase_json_base64).decode('utf-8')
firebase_json_dict = json.loads(firebase_json_str)

# Initialize Firebase Admin SDK
# firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
cred = credentials.Certificate(firebase_json_dict) 
firebase_admin.initialize_app(cred)

db = firestore.client()
