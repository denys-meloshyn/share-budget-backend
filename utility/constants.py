from datetime import datetime


class Constants:
    # JSON keys
    k_date = 'date'
    k_name = 'name'
    k_limit = 'limit'
    k_email = 'email'
    k_price = 'price'
    k_token = 'token'
    k_result = 'result'
    k_status = 'status'
    k_user_id = 'userID'
    k_message = 'message'
    k_group_id = 'groupID'
    k_password = 'password'
    k_last_name = 'lastName'
    k_date_format = '%Y-%m-%d'
    k_first_name = 'firstName'
    k_expense_id = 'expenseID'
    k_is_removed = 'isRemoved'
    k_time_stamp = 'timeStamp'
    k_internal_id = 'internalID'
    k_category_id = 'categoryID'
    k_user_group_id = 'userGroupID'
    k_creation_date = 'creationDate'
    k_user_not_exist = 'userNotExist'
    k_budget_limit_id = 'budgetLimitID'
    k_modified_user_id = 'modifiedUserID'
    k_category_limit_id = 'categoryLimitID'
    k_user_is_already_exist = 'user_is_already_exist'

    k_pagination = 'pagination'
    k_pagination_start = 'start'
    k_pagination_total = 'total'
    k_pagination_page_size = 'pageSize'

    k_registration_resource_path = '/registration'
    project_email = 'sharebudgetproject@gmail.com'

    default_page_size = 50
    default_categories = ['Home', 'Food', 'Transport', 'Sport']

    def __init__(self):
        pass

    @staticmethod
    def default_response(response, time_stamp=datetime.utcnow(), pagination=None):
        result = {Constants.k_result: response,
                  Constants.k_time_stamp: time_stamp.isoformat()}

        if pagination is not None:
            pagination_dict = {Constants.k_pagination_total: pagination.total,
                               Constants.k_pagination_start: pagination.page,
                               Constants.k_pagination_page_size: pagination.per_page}
            result[Constants.k_pagination] = pagination_dict

        return result

    @staticmethod
    def error_reponse(message):
        result = {Constants.k_message: message}
        return result
