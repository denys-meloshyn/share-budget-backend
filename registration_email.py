from flask_mail import Message

from constants import Constants
from shared_objects import mail


def send_registration_email(user):
    msg = Message()
    msg.sender = Constants.project_email
    msg.subject = 'Share Budget Registration Completion Information for ' + user.first_name
    msg.recipients = [user.email]

    msg.body = 'Hi ' + user.first_name + ',\n\n'
    msg.body += 'Thanks for joining Share Budget. To complete your registration, please click the link below to ' \
                'approve your email:\n\n'
    msg.body += 'https://sharebudget.herokuapp.com'
    msg.body += Constants.k_registration_resource_path
    msg.body += '?'
    msg.body += Constants.k_token
    msg.body += '='
    msg.body += user.registration_email_token + '\n\n'
    msg.body += 'If you did not register for Shared Budget, please disregard this message.\n'
    msg.body += 'Please contact ' + Constants.project_email + 'with any questions.\n\n'
    msg.body += 'Shared Budget Team'

    mail.send(msg)
