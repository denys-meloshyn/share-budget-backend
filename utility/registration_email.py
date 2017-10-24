from flask_mail import Message

from shared_objects import mail
from utility.constants import Constants


class SendRegistrationEmail:
    def __init__(self):
        pass

    @staticmethod
    def send_registration_email(user):
        msg = Message()
        msg.sender = Constants.project_email
        msg.subject = 'Share Budget Registration Completion Information for ' + user.first_name
        msg.recipients = [user.email]

        msg.html = '<html>'
        msg.html += '<body>'
        msg.html += '<p>Hi ' + user.first_name + '!</p>'
        msg.html += '<p>Thanks for joining Share Budget. To complete your registration, please, click the following ' \
                    'link to approve your email:</p>'
        msg.html += '<p> <a href = "'
        msg.html += 'https://sharebudget.herokuapp.com'
        msg.html += Constants.registration_resource_path
        msg.html += '?'
        msg.html += Constants.JSON.token
        msg.html += '='
        msg.html += user.registration_email_token
        msg.html += '">Complete registration</a></p>'
        msg.html += '<p>If you did not register for Share Budget, just ignore this message.</p>'
        msg.html += '<p>With any questions contact <a href="mailto:sharebudgetproject@gmail.com?Subject=Remarks' \
                    ' and offers">sharebudgetproject@gmail.com</a>.</p>'
        msg.html += '<p>Best regards, <br>Share Budget Team</p>'
        msg.html += '</body>'
        msg.html += '</html>'

        mail.send(msg)
