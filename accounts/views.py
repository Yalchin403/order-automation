from json import load
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
import os
from dotenv import load_dotenv


load_dotenv()
User = get_user_model()

if settings.DEBUG:
    domain = os.getenv("LOCAL_DOMAIN")

else:
    domain = os.getenv("PROD_DOMAIN")


class SignInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:main')
            
        return render(request, "accounts/signin.html", {'title': 'Giriş'})
        
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            next_  = request.GET.get('next')
            if next_:
                return redirect(f'{domain}{next_}')

            return redirect('home:main')
            
        else:
            messages.error(request, 'Username or password invalid')

            return render(request, 'accounts/signin.html')


class SignUpView(View):
    def get(self, request):
        if not self.request.user.is_authenticated:

        #TODO:
        #   send title as context
            return render(request, "accounts/signup.html", {'title': 'Qeydiyyat'})
        
        return redirect("home:main")


    def post(self, request):

        #TODO:
        # write some js for validation and checking if user accepted terms and conditions
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        is_agree = request.POST.get("agree-term")

        print(is_agree, type(is_agree))
        if username and email and password1 and password2 and is_agree == "on":
            user_qs_by_username = User.objects.filter(username=username)
            user_qs_by_email = User.objects.filter(email=email)

            if not user_qs_by_email and not user_qs_by_username:

                if password1 == password2:
                    print("Here")
                    user_obj = User.objects.create(username=username, email=email)
                    user_obj.set_password(password2)
                    user_obj.save()
                    messages.success(request, f'Account has been successfully created for you')

                    return render(request, 'accounts/signin.html', {'title': 'Giriş'})

                else:
                    messages.error(request, "Parollar uyğun gəlmədi!!")
                    
                    return render(request, 'accounts/signup.html', {'title': 'Qeydiyyat'})

            else:

                if user_qs_by_email:
                    messages.error(request, "Email artıq istifadə olunub!")
                
                else:
                    messages.error(request, "Istifadəçi adı artıq istifadə olunub!")

        else:
            messages.error(request, "Bütün xanalar doldurulmalıdır!")
        
        return render(request, 'accounts/signup.html', {'title': 'Qeydiyyat'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:signin-view')


#TODO:
#   otp authentication upon registration