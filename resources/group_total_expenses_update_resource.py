from flask_jwt_extended import (
    jwt_required
)
from flask_restplus import Resource, reqparse

from application import api
from model.group_total_expenses import GroupTotalExpenses
from utility.constants import Constants
from utility.resource_parser import ResourceParser
from utility.response_formatter import ResponseFormatter


def get_parameters(parser):
    ResourceParser.add_default_update_parameters(parser)
    parser.add_argument(Constants.JSON.group_id,
                        type=int,
                        help='Group ID',
                        location='form')


get_parser = reqparse.RequestParser()
swagger_get_parser = api.parser()

get_parameters(get_parser)
get_parameters(swagger_get_parser)


class GroupTotalExpensesUpdateResource(Resource):
    @jwt_required()
    @api.doc(parser=swagger_get_parser)
    def get(self):
        args = get_parser.parse_args()
        group_id = args.get(Constants.JSON.group_id)

        query = GroupTotalExpenses.query.filter(group_id == group_id)

        time_stamp = args.get(Constants.JSON.time_stamp)
        if time_stamp is not None:
            time_stamp = time_stamp[0].replace(tzinfo=None)
            query = query.from_self().filter(GroupTotalExpenses.time_stamp > time_stamp)
        query = query.order_by(GroupTotalExpenses.time_stamp.asc())

        start_page = args[Constants.JSON.pagination_start]
        page_size = args[Constants.JSON.pagination_page_size]

        return ResponseFormatter.format_response(query=query, start_page=start_page, page_size=page_size)
