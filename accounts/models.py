from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
import pyotp
from dotenv import load_dotenv
import os
from .tasks import send_email
from django.db.models.signals import post_save
from django.dispatch import receiver


load_dotenv()

if settings.DEBUG:
	current_site = os.getenv("LOCAL_DOMAIN")

else:
	current_site = os.getenv("PROD_DOMAIN")



class MyAccountManager(BaseUserManager):
	def create_user(self, username, first_name, last_name, email, password):

		if not email:
			raise ValueError('User must have an email address')

		if not username:
			raise ValueError('User must have an username')

		if not password:
			raise ValueError('User must have a password')

		user = self.model(
			email=self.normalize_email(email.lower()),
			username=username,
			first_name=first_name,
			last_name=last_name,
		)

		user.set_password(password)
		user.save(using=self.db)

		return user

	def create_superuser(self, username, first_name, last_name, email, password):

		if not email:
			raise ValueError('User must have an email address')

		if not username:
			raise ValueError('User must have an username')

		if not password:
			raise ValueError('User must have a password')

		user = self.create_user(
			email=self.normalize_email(email.lower()),
			username=username,
			password=password,
			first_name=first_name,
			last_name=last_name,
		)

		user.is_active = True
		user.is_staff = True
		user.is_admin = True
		user.is_superadmin = True
		user.save(using=self.db)

		return user


class Account(AbstractBaseUser):
	first_name = models.CharField(max_length=55)
	last_name = models.CharField(max_length=55)
	username = models.CharField(max_length=55, unique=True)
	email = models.EmailField(max_length=55, unique=True)
	phone_number = models.CharField(max_length=55, unique=True, null=True, blank=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_superadmin = models.BooleanField(default=False)
	otp = models.CharField(max_length=55)
	activation_key = models.CharField(max_length=55)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

	def __str__(self) -> str:
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, add_label):
		return True

	objects = MyAccountManager()

	def generate_otp(self):
		OTP_EXPIRATION_TIME_IN_SECONDS = 600
		secret = pyotp.random_base32()        
		totp = pyotp.TOTP(secret, interval=OTP_EXPIRATION_TIME_IN_SECONDS)
		OTP = totp.now()
		self.otp = OTP
		self.activation_key = secret

	def generate_otp_link(self, id, otp):
		otp = self.otp
		rel_url = reverse("accounts:verify-account", args=(id, otp))
		absolute_url = current_site + rel_url

		return absolute_url


@receiver(post_save, sender=Account)
def print_only_after_deal_created(sender, instance, created, **kwargs):
	if created:
		print(f'New deal with pk: {instance.pk} was created.')
		instance.generate_otp()
		absolute_url = instance.generate_otp_link(instance.id, instance.otp)
		email_subject = "Hesab Təsdiqlənməsi"
		rel_content = "Hesabınızı təsdiqləmək üçün aşağıdakı linkə klik edin: \n"
		email_content = rel_content + absolute_url
		send_email.delay(email_subject, instance.email, email_content)