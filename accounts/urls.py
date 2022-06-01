from django.urls import path
from accounts.views import SignInView


app_name = "accounts"
urlpatterns = [
	path('signin-signup/', SignInView.as_view(), name='signin-signup-view'),
]