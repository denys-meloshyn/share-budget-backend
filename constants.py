class Constants:
    k_result = 'result'
    k_status = 'status'
    k_user_id = 'userID'
    k_message = 'message'
    k_is_removed = 'isRemoved'
    k_time_stamp = 'timeStamp'
    k_internal_id = 'internalID'

    def __init__(self):
        pass

    @staticmethod
    def default_response(reponse):
        result = {Constants.k_status: True,
                  Constants.k_message: '',
                  Constants.k_result: reponse}
        return result

    @staticmethod
    def error_reponse(message):
        result = {Constants.k_status: False,
                  Constants.k_message: message,
                  Constants.k_result: {}}
        return result
