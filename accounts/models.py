from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.urls import reverse
# from django_rest_passwordreset.signals import reset_password_token_created
# import os
# import pathlib
# from django.contrib.sites.shortcuts import get_current_site
# from django.conf import settings


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

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

	def __str__(self) -> str:
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, add_label):
		return True

	objects = MyAccountManager()


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
	
# 	if settings.DEBUG:
# 		current_site = os.getenv("LOCAL_DOMAIN")

# 	else:
# 		current_site = os.getenv("PROD_DOMAIN")

# 	abs_url = f"{current_site}{reverse('password_reset:reset-password-request')}?token={reset_password_token.key}"
# 	subject = "Parolu Yenilə"
# 	email = reset_password_token.user.email
# 	current_path = pathlib.Path(__file__).parent.resolve()
# 	content = get_html_content(os.path.join(current_path,'templates', 'accounts', 'forgot_password.html')) + abs_url
# 	send_email(email, subject, content)