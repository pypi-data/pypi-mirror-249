import os

import firebase_admin
from firebase_admin import credentials, firestore


def initialize_firebase(cred_path=None):
    try:
        # Check if Firebase app is already initialized
        return firebase_admin.get_app()
    except ValueError as e:
        # Get the path to the firebase_sa.json file which is in the same directory as this script
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)


# Test the function
if __name__ == "__main__":
    initialize_firebase()
