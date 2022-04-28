from django.shortcuts import render
from django.views import View


class OrderView(View):
	def get(self, request):
		if request.method == "GET":
			return render(request, 'orders/index.html')

	def post(self, request):
		pass