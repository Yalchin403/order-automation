from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from home.models import (
	Product,
	Category,
)

class StoreView(View):
	def get(self, request):
		product_qs = Product.objects.filter(is_available=True)
		category_qs = Category.objects.all()
		context = {
			"products": product_qs,
			"categories": category_qs,
		}
		return render(request, "store/store.html", context)