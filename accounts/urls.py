from django.urls import path
from accounts.views import SignUpView, SignInView, LogoutView


app_name = "accounts"
urlpatterns = [
	path('signup/', SignUpView.as_view(), name='signup-view'),
	path('signin/', SignInView.as_view(), name='signin-view'),
	path('logout/', LogoutView.as_view(), name='logout-view'),


]