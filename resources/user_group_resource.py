from datetime import datetime

from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from flask_restplus import Resource, reqparse
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from application import api
from model import db
from model.group import Group
from model.user_group import UserGroup
from utility.constants import Constants
from utility.resource_parser import ResourceParser


def put_parameters(parser):
    parser.add_argument(Constants.JSON.user_group_id, type=int, help='User group ID', location='form')
    parser.add_argument(Constants.JSON.user_id, type=int, help='User ID', location='form', required=True)
    parser.add_argument(Constants.JSON.group_id, type=int, help='Group ID', location='form', required=True)

    ResourceParser.add_default_parameters(parser)


def post_parameters(parser):
    parser.add_argument(Constants.JSON.invitation_token, help='Invitation token', location='form', required=True)
    ResourceParser.add_default_parameters(parser)


class UserGroupResource(Resource):
    post_parser = api.parser()
    post_parameters(post_parser)

    @jwt_required
    @api.doc(parser=post_parser)
    def post(self):
        parser = reqparse.RequestParser()
        post_parameters(parser)
        args = parser.parse_args()
        request_user_id = get_jwt_identity()

        invitation_token = args[Constants.JSON.invitation_token]
        try:
            token_serializer = Serializer(invitation_token)
            toke_data = token_serializer.loads(invitation_token)
        except SignatureExpired:
            # Valid token, but expired
            return Constants.error_reponse('token_expired'), 401
        except BadSignature:
            # Invalid token
            return Constants.error_reponse('token_not_valid'), 401

        user_id_group_creator = toke_data[Constants.JSON.user_id]
        group_id = toke_data[Constants.JSON.group_id]

        group = Group.query.filter_by(group_id=group_id).first()
        if not group:
            return Constants.error_reponse(Constants.JSON.group_is_not_exist), 401

        if group.creator_user_id != user_id_group_creator:
            return Constants.error_reponse(Constants.JSON.permission_not_allowed), 401

        user_group = UserGroup.query.filter(
            db.and_(UserGroup.group_id == group_id, UserGroup.user_id == request_user_id)
        ).first()

        if user_group is None:
            user_group = UserGroup(input_parameters={})
            user_group.user_id = request_user_id
            user_group.group_id = group_id
            db.session.add(user_group)
        else:
            user_group.is_removed = False
            user_group.time_stamp = datetime.utcnow()

        db.session.commit()
        return Constants.default_response(user_group.to_json())

    put_parser = api.parser()
    put_parameters(put_parser)

    @jwt_required
    @api.doc(parser=put_parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()
        request_user_id = get_jwt_identity()

        user_group_id = args.get(Constants.JSON.user_group_id)
        if user_group_id is None:
            user_group = UserGroup(input_parameters=args)
            db.session.add(user_group)
            db.session.commit()

            return Constants.default_response(user_group.to_json())

        user_group = UserGroup.query.filter_by(user_group_id=user_group_id).first()
        if not user_group:
            return Constants.error_reponse('user_group_is_not_exist'), 401

        group = Group.query.filter_by(group_id=user_group.group_id).first()
        if not group:
            return Constants.error_reponse(Constants.JSON.group_is_not_exist), 401

        if group.creator_user_id != request_user_id:
            return Constants.error_reponse(Constants.JSON.permission_not_allowed), 401

        user_group.update(args)
        db.session.commit()

        return Constants.default_response(user_group.to_json())
