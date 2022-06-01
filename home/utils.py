from order_automation.settings import EMAIL_HOST_USER
import os
from django.core.mail import EmailMessage


def send_message_to_admin(name, email, subject, message):
    email_body = f"""
        <h1>{name} tərəfindən yeni mesajınız var!</h1>

        <ul>
        <li>Email: {email}</li>
        <li>Mövzu: {subject}</li>
        <li>Mesaj: {message}</li>
        <ul>
        """
    reciever_email = os.getenv('RECIEVER_EMAIL')

    msg = EmailMessage(
        f"Yeni Mesaj - Mövzu -> {subject}",
        email_body,
        EMAIL_HOST_USER,
        [reciever_email]
    )
    msg.content_subtype = "html"
    msg.send()
