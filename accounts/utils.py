from django.core.mail import EmailMessage
from order_automation.settings import EMAIL_HOST_USER
import os


def send_email(subject, reciever_email, content):
    
    try:
        msg = EmailMessage(
            subject,
            content,
            EMAIL_HOST_USER,
            [reciever_email],
        )
        msg.content_subtype = "html"
        msg.send()

    except:
        print("Couldn't send the email")