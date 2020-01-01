from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from flask_restplus import Resource, reqparse

from application import api
from model.group import Group
from utility.constants import Constants
from utility.resource_parser import ResourceParser
from utility.token_serializer import TokenSerializer


def get_parameters(parser):
    parser.add_argument(Constants.JSON.group_id, help='Group ID', location='form', required=True)
    ResourceParser.add_default_update_parameters(parser)


class UserGroupInviteResource(Resource):
    get_parser = api.parser()
    get_parameters(get_parser)

    @jwt_required
    @api.doc(parser=get_parser)
    def get(self):
        parser = reqparse.RequestParser()
        get_parameters(parser)
        args = parser.parse_args()
        request_user_id = get_jwt_identity()

        group_id = args[Constants.JSON.group_id]
        group = Group.query.filter_by(group_id=group_id).first()
        if not group:
            return Constants.error_reponse(Constants.JSON.group_is_not_exist), 401

        if group.creator_user_id != request_user_id:
            return Constants.error_reponse(Constants.JSON.permission_not_allowed), 401

        token = TokenSerializer.generate_token(data={Constants.JSON.user_id: request_user_id,
                                                     Constants.JSON.group_id: group_id},
                                               expiration=300)
        return Constants.default_response(token)
