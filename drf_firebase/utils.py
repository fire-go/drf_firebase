from firebase_admin import auth


def get_firebase_user_uid(firebase_user: auth.UserRecord) -> str:
    """
    See Official documentation: shorturl.at/irBS3
    parameters:
    -firebase_user: firebase_admin.auth.UserRecord

    return: Firebase Unique ID Aka UID
    """
    try:
        if firebase_user.uid:
            return firebase_user.uid
    except Exception as e:
        raise Exception(e)


def get_firebase_user_identifier(firebase_user: auth.UserRecord) -> str:

    try:
        return (
            firebase_user.email
            if firebase_user.email
            else firebase_user.provider_data[0].email
            if firebase_user.provider_data[0].email
            else firebase_user.phone_number
            if firebase_user.phone_number
            else firebase_user.provider_data[0].phone_number
            if firebase_user.provider_data[0].phone_number
            else Exception("Identifier not found.")
        )
    except Exception as e:
        raise Exception(e)
