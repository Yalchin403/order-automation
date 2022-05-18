from turtle import title
from django.db import models
from django.core.mail import EmailMessage
from order_automation.settings import EMAIL_HOST_USER
from dotenv import load_dotenv
import os

load_dotenv()


class Order(models.Model):
    SE = 'Sifariş Edilmeyib'
    SQ = 'Sifariş Qəbul edildi'
    XAG = 'Xarici Anbara Göndərilib'
    XA = 'Xarici Anbardadır'
    XAGO = 'Xarici Anbardan Göndərilib'
    GM = 'Gömrük Məntəqəsindədir'
    DA = 'Daxili Anbardadır'

    STATUSES = [
        ('SE', SE),
        ('SQ', SQ),
        ('XAG', XAG),
        ('XA', XA),
        ('XAGO', XAGO),
        ('GM', GM),
        ('DA', DA),
    ]

    name = models.CharField(max_length=55)
    surname = models.CharField(max_length=55)
    email = models.CharField(max_length=55)
    phone_number = models.CharField(max_length=55)
    order_url = models.TextField()
    notes = models.TextField()
    order_status = models.CharField(
        max_length=4,
        choices=STATUSES,
        default=SE,
    )

    def __str__(self):
        return f'{self.name} {self.surname} - {self.phone_number}'

    def save(self, *args, **kwargs):
        # send email

        try:
            email_body = f"""
				<h1>{self.name} {self.surname} terefinden yeni sifaris var</h1>

				<ul>
				<li>Email: {self.email}</li>
				<li>Telefon: {self.phone_number}</li>
				<li>Məhsulun Linki: {self.order_url}</li>
				<li>Əlavə qeydlər: {self.notes}</li>
				<ul>
				"""
            reciever_email = os.getenv('RECIEVER_EMAIL')

            msg = EmailMessage(
                "Yeni Sifaris",
                email_body,
                EMAIL_HOST_USER,
                [reciever_email]
            )
            msg.content_subtype = "html"
            msg.send()

        except:
            print("Couldn't send the email")

        return super().save(*args, **kwargs)
