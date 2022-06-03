from django.urls import path
from accounts.views import SignUpView, SignInView


app_name = "accounts"
urlpatterns = [
	path('signup/', SignUpView.as_view(), name='signup-view'),
	path('signin/', SignInView.as_view(), name='signin-view'),

]