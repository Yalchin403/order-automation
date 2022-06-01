from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Employee
from .utils import send_message_to_admin


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

    def post(self, request):
        # Formdan gelen datalari gotur
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            if name is not None and subject is not None and email is not None and message is not None:

                send_message_to_admin(name,
                                    email,
                                    subject,
                                    message
                    )
            else:
                return HttpResponse("Datalar boş olmamalıdır!", status=500)

        except:
            return HttpResponse("Görünüşə görə front id-ləri gözlənildiyi kimi deyil!", status=500)

        return HttpResponse("Response back!", status=200)