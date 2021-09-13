import base64
import os
from dotenv import load_dotenv
load_dotenv()
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid import SendGridAPIClient

to_emails = [
    ('tanaymodani18@gmail.com', 'Tanay'),
    ('akjn11@gmail.com', 'Akshat')
]

def send_mail(fromMail, toMail,msg):
    message = Mail(
        from_email=('tanaymodani18@gmail.com', 'Tanay'),
        to_emails=to_emails,
        subject='Stocks List',
        html_content=msg)
    try:
        sendgrid_client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

