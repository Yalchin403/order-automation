import re
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Employee


class HomeView(View):
    def get(self, request):
	    return render(request, 'home/home.html')


class AboutView(View):
    def get(self, request):
        employee_qs = Employee.objects.all()
        context = {
            "employees": employee_qs,
            "title": "Haqqımızda"
        }

        return render(request, 'home/about.html', context)


class ContactView(View):
    def get(self, request):
        context = {
            "title": "Əlaqə"
        }

        return render(request, 'home/contact.html', context)