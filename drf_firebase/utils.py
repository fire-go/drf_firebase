from firebase_admin import auth


def get_firebase_user_uid(firebase_user: auth.UserRecord) -> str:
    try:
        if firebase_user.uid:
            return firebase_user.uid
    except Exception as e:
        raise Exception(e)
