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
    k_user_not_exist = 'userNotExist'
    k_budget_limit_id = 'budgetLimitID'
    k_modified_user_id = 'modifiedUserID'
    k_category_limit_id = 'categoryLimitID'

    k_registration_resource_path = '/registration'
    project_email = 'sharebudgetproject@gmail.com'

    default_categories = ['Home', 'Food', 'Transport', 'Sport']

    def __init__(self):
        pass

    @staticmethod
    def default_response(reponse):
        result = {Constants.k_result: reponse,
                  Constants.k_time_stamp: datetime.utcnow().isoformat()}
        return result

    @staticmethod
    def error_reponse(message):
        result = {Constants.k_message: message}
        return result
