from flask_restful import inputs

from utility.constants import Constants


class ResourceParser:
    def __init__(self):
        pass

    @staticmethod
    def add_default_update_parameters(parser):
        parser.add_argument(Constants.k_time_stamp, type=inputs.iso8601interval, help='Time stamp date (ISO 8601)',
                            location='headers', required=True)
        parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='headers', required=True)
        parser.add_argument(Constants.k_token, help='User token', location='headers', required=True)
        parser.add_argument(Constants.k_pagination_start, help='Start page', type=int)
        parser.add_argument(Constants.k_pagination_page_size, help='Pagination size page', type=int)

    @staticmethod
    def add_default_parameters(parser):
        parser.add_argument(Constants.k_token, help='User token', location='form', required=True)
        parser.add_argument(Constants.k_internal_id, type=int, help='Internal ID', location='form')
        parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
        parser.add_argument(Constants.k_is_removed, type=inputs.boolean, help='Is removed', location='form')
