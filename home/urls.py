from django.urls import path
from home.views import (
	HomeView,
	AboutView,
	ContactView,
)

app_name = "home"
urlpatterns = [
	path('', HomeView.as_view(), name='main'),
	path('about/', AboutView.as_view(), name="about"),
	path('contact/', ContactView.as_view(), name='contact'),
]