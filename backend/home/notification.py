import sendgrid
from sendgrid.helpers.mail.email import Email
from sendgrid.sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import To
from digigru.local_settings import DEFAULT_FROM_EMAIL, SENDGRID_APIKEY
import os
from sendgrid.helpers.mail import *

sg = SendGridAPIClient(api_key=SENDGRID_APIKEY)
from_email = Email(DEFAULT_FROM_EMAIL)

def send_email(subject, message, to_email):
    target = To(to_email)
    # content = Content('text/html', message)
    mail = Mail(from_email=from_email, to_emails=[target], subject=subject, plain_text_content=message)
    response = sg.client.mail.send.post(request_body=mail.get())
    print('SendGrid response:' + str(response.status_code))