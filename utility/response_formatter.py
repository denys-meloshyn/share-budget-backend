from datetime import datetime

from sqlalchemy.orm import Query

from sqlalchemy_pagination import paginate
from utility.constants import Constants


class ResponseFormatter:
    def __init__(self):
        pass

    @staticmethod
    def format_response(query, start_page, page_size):
        pagination = None
        if type(query) is Query:
            if start_page is not None and page_size is not None:
                pagination = paginate(query, start_page, page_size)
                items = pagination.items
            else:
                items = query.all()
        else:
            if start_page is not None and page_size is not None:
                pagination = query.paginate(start_page, page_size, True)
                items = pagination.items
            else:
                items = query.all()

        time_stamp = datetime.utcnow()
        if len(items) > 0:
            time_stamp = max(item.time_stamp for item in items)

        items = [model.to_json() for model in items]

        return Constants.default_response(items, time_stamp, pagination)
