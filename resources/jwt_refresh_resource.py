from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, create_access_token
from flask_restplus import Resource


class JWTRefreshResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        # retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method
        current_user = get_jwt_identity()
        # return a non-fresh token for the user
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token, 'user': current_user}, 200
