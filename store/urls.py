from django.urls import path
from .views import (
	StoreView,
)

app_name = "store"
urlpatterns = [
	path('', StoreView.as_view(), name='main'),
]