class Constants:
    k_result = 'result'
    k_status = 'status'
    k_user_id = 'userID'
    k_is_removed = 'isRemoved'
    k_time_stamp = 'timeStamp'
    k_internal_id = 'internalID'

    def __init__(self):
        pass

    @staticmethod
    def error_message(message, status):
        result = {Constants.k_status: message,
                  Constants.k_result: []}
        return result, status
