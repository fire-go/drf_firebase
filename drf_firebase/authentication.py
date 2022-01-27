from rest_framework import authentication, exceptions
from .settings import api_settings
from firebase_admin import auth as firebase_auth
from typing import Tuple, Dict
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
import logging
from . import __title__

log = logging.getLogger(__title__)

User = get_user_model()


class FirebaseAuthentication(authentication.TokenAuthentication):
    """
    Firebase token based authentication.
    Clients should authenticate by passing the token keyword in the "Authorization"
    HTTP header, prepended with the string "Keyword " mentionned in the environment
    variable FIREBASE_AUTH_HEADER_PREFIX which has the default value "Bearer ".
    For example:
        -Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = api_settings.FIREBASE_AUTH_HEADER_PREFIX

    def authenticate_credentials(self, token: str) -> Tuple[AnonymousUser, Dict]:
        try:
            decoded_token = self._decode_token(token)
            firebase_user = self._authenticate_token(decoded_token)
            local_user = self._get_or_create_local_user(firebase_user)
            return (local_user, decoded_token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(e)

    def _decode_token(self, token: str) -> Dict:
        """
        Attempt to verify JWT from Authorization header with Firebase and
        return the decoded token
        """
        try:
            decoded_token = firebase_auth.verify_id_token(
                token, check_revoked=api_settings.FIREBASE_CHECK_JWT_REVOKED
            )
            log.info(f"_decode_token - decoded_token: {decoded_token}")
            return decoded_token
        except Exception as e:
            log.error(f"_decode_token - Exception: {e}")
            raise Exception(e)

    def _authenticate_token(self, decoded_token: Dict) -> firebase_auth.UserRecord:
        """
        Returns firebase user if token is authenticated
        """
        try:
            uid = decoded_token.get("uid")
            log.info(f"_authenticate_token - uid: {uid}")
            firebase_user = firebase_auth.get_user(uid)
            log.info(f"_authenticate_token - firebase_user: {firebase_user}")
            if api_settings.FIREBASE_AUTH_EMAIL_VERIFICATION:
                if not firebase_user.email_verified:
                    raise Exception("Email address of this user has not been verified.")
            return firebase_user
        except Exception as e:
            log.error(f"_authenticate_token - Exception: {e}")
            raise Exception(e)

    def _get_or_create_local_user(
        self, firebase_user: firebase_auth.UserRecord
    ) -> User:
        pass
