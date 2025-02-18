import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables from .env file
load_dotenv()

# Initialize Firebase Admin SDK
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
cred = credentials.Certificate(firebase_credentials_path) 
firebase_admin.initialize_app(cred)

db = firestore.client()
