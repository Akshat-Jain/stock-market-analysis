import base64
import os
from dotenv import load_dotenv
from datetime import date
today = date.today()
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
        from_email=('tanaymodani18@gmail.com', 'Stock Market Analysis'),
        to_emails='tanaymodani18@gmail.com',
        subject='[Stocks Analysis] Strategy 1:  '+today.strftime("%B %d, %Y"),
        html_content=msg)
    try:
        sendgrid_client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(e)

