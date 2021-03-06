from django.urls import path
from accounts.views import (
	SignUpView,
	SignInView,
	LogoutView,
	VerifyAccountView,
	ResendOTP
)


app_name = "accounts"
urlpatterns = [
	path('signup/', SignUpView.as_view(), name='signup-view'),
	path('signin/', SignInView.as_view(), name='signin-view'),
	path('logout/', LogoutView.as_view(), name='logout-view'),
	path('resend-otp/<int:user_id>/', ResendOTP.as_view(), name="resend-otp"),
	path('verify/account/<int:id>/<str:otp>/', VerifyAccountView.as_view(), name="verify-account")


]