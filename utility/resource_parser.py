from flask_restplus import inputs

from utility.constants import Constants


class ResourceParser:
    def __init__(self):
        pass

    @staticmethod
    def add_default_update_parameters(parser):
        parser.add_argument(Constants.JSON.time_stamp, type=inputs.iso8601interval, help='Time stamp date (ISO 8601)',
                            location='headers')
        parser.add_argument(Constants.JSON.user_id, type=int, help='User ID', location='headers', required=True)
        parser.add_argument('Authorization', help='Access token', location='headers', required=True)
        parser.add_argument(Constants.JSON.pagination_start, help='Start page', type=int)
        parser.add_argument(Constants.JSON.pagination_page_size, help='Pagination size page', type=int)

    @staticmethod
    def add_default_parameters(parser):
        parser.add_argument('Authorization', help='Access token', location='headers', required=True)
        parser.add_argument(Constants.JSON.internal_id, type=int, help='Internal ID', location='form')
        parser.add_argument(Constants.JSON.user_id, type=int, help='User ID', location='form', required=True)
        parser.add_argument(Constants.JSON.is_removed, type=inputs.boolean, help='Is removed', location='form')
