from utils import FirebaseUtils
import os
import pytest
from rest_framework.reverse import reverse
import json

firebase_utils = FirebaseUtils(os.getenv("TEST_EMAIL"))
jwt = firebase_utils.generate_id_token()
user = firebase_utils.get_test_user()


@pytest.mark.django_db
class TestFirebaseUser:
    pytestmark = pytest.mark.django_db

    def test_user_creation_on_request(self, client):
        url = reverse("get-user")
        client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {jwt}"
        response = client.get(url)
        data = json.loads(response.content)
        assert user.uid == data["username"]
