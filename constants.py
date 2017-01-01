class Constants:
    k_token = 'token'
    k_result = 'result'
    k_status = 'status'
    k_user_id = 'userID'
    k_message = 'message'
    k_is_removed = 'isRemoved'
    k_time_stamp = 'timeStamp'
    k_internal_id = 'internalID'

    k_registration_resource_path = '/registration'
    project_email = 'sharebudgetproject@gmail.com'

    def __init__(self):
        pass

    @staticmethod
    def default_response(reponse):
        result = {Constants.k_result: reponse}
        return result

    @staticmethod
    def error_reponse(message):
        result = {Constants.k_message: message}
        return result
