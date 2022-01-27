from rest_framework import authentication
from .settings import api_settings
from firebase_admin import auth as firebase_auth
from typing import Tuple, Dict
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()


class FirebaseAuthentication(authentication.TokenAuthentication):
    keyword = api_settings.FIREBASE_AUTH_HEADER_PREFIX

    def authenticate_credentials(self, token: str) -> Tuple[AnonymousUser, Dict]:
        pass

    def _decode_token(self, token: str) -> Dict:
        pass

    def _authenticate_token(self, decoded_token: Dict) -> firebase_auth.UserRecord:
        pass

    def _get_or_create_local_user(
        self, firebase_user: firebase_auth.UserRecord
    ) -> User:
        pass
