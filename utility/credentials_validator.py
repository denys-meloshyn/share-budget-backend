from itsdangerous import BadSignature, SignatureExpired

from model.users import User
from utility.constants import Constants
from utility.token_serializer import TokenSerializer


class CredentialsValidator:
    def __init__(self):
        pass

    @staticmethod
    def is_user_credentials_valid(user_id, token):
        # Check token status
        status = TokenSerializer.verify_auth_token(token, user_id)

        # Is token expired?
        if status == SignatureExpired:
            # Yes: return error status
            return False, Constants.error_reponse('token_expired')
        # Is token not valid?
        elif status == BadSignature:
            # Yes: return error status
            return False, Constants.error_reponse('token_not_valid')

        # Try to find user with received ID
        user = User.query.filter_by(user_id=user_id).first()

        # Do we have user with received ID?
        if user is None:
            # No we haven't: return error status
            return False, Constants.error_reponse('user_does_not_exist')

        # Is received token correct?
        if user.token != token:
            # No: return error status
            return False, Constants.error_reponse('token_not_valid')

        # If everything is Ok - return person model
        return True, Constants.default_response('Ok')
