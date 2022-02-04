import requests
from drf_firebase.authentication import firebase_auth
import os

FIREBASE_DRF_FIREBASE_API_KEY = os.getenv("FIREBASE_DRF_FIREBASE_API_KEY")

id_token_endpoint = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={FIREBASE_DRF_FIREBASE_API_KEY}"


class FirebaseUtils:
    """
    The class TokenGenerator takes firebase app which is already initialized
    by drf_firebase_auth and uses firebase_auth object in order to get a token id.
    """

    def __init__(self, email):
        self.email = email

    def get_test_user(self) -> firebase_auth.UserRecord:
        try:
            return firebase_auth.get_user_by_email(self.email)
        except Exception as e:
            raise Exception(e)

    def create_custom_token(self) -> str:
        try:
            firebase_user = self.get_test_user()
            return firebase_auth.create_custom_token(firebase_user.uid)
        except Exception as e:
            raise Exception(e)

    def generate_id_token(self) -> str:
        try:
            url = id_token_endpoint
            data = {"token": self.create_custom_token(), "returnSecureToken": True}
            res = requests.post(url, data=data)
            res.raise_for_status()
            return res.json()["idToken"]
        except Exception as e:
            raise Exception(e)
