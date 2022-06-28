from json import load
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
import os
from dotenv import load_dotenv
import pyotp
from django.shortcuts import get_object_or_404
from accounts.tasks import send_email


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
            context = {
                'title': 'Qeydiyyat',
            }

            return render(request, "accounts/signup.html", context)
        
        return redirect("home:main")


    def post(self, request):

        #TODO:
        # write some js for validation and checking if user accepted terms and conditions
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        is_agree = request.POST.get("agree-term")

        if username and email and password1 and password2 and is_agree == "on":
            user_qs_by_username = User.objects.filter(username=username)
            user_qs_by_email = User.objects.filter(email=email)

            if not user_qs_by_email and not user_qs_by_username:

                if password1 == password2:
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


class VerifyAccountView(View):
    def get(self, request, id, otp):
        account_obj = get_object_or_404(User, id=id)
        if not account_obj.is_active:

            activation_key = account_obj.activation_key
            totp = pyotp.TOTP(activation_key, interval=600)

            _otp = account_obj.otp
            if otp != _otp:
                return render(request, "accounts/invalid_otp.html", status=406)

            else:
                verify = totp.verify(otp)

                if verify:
                    account_obj.is_active = True
                    email_subject = "Hesabınız təsdiqləndi"
                    receiver_email = account_obj.email
                    email_content = "Saytımıza xoş gəldiniz, hesabınız uğurla təsdiqləndi!"
                    send_email.delay(email_subject, receiver_email, email_content)
                    account_obj.save()
                    
                    return render(request, "accounts/account_verified.html", status=200)    
                
                else:
                    return render(request, "accounts/otp_expired.html", status=410)

        return render(request, "accounts/account_is_already_verified.html", status=409)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:signin-view')


# TODO:
#   Send emails by getting their content from html files, also make it possible to insert dynamic variables
#   Email content html template: https://bbbootstrap.com/snippets/confirm-account-email-template-17848137