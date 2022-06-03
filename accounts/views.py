from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages


User = get_user_model()


class SignInView(View):
    def get(self, request):
        return render(request, "accounts/signin.html", {'title': 'Giriş'})

    def post(self, request):
        pass


class SignUpView(View):
    def get(self, request):
        #TODO:
        #   send title as context
        return render(request, "accounts/signup.html", {'title': 'Qeydiyyat'})


    def post(self, request):

        #TODO:
        #   Check if username is unique
        # write some js for validation and checking if user accepted terms and conditions
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        print(username, email, password1, password2)

        if username and email and password1 and password2:

            if password1 == password2:

                user_obj = User.objects.create(username=username, email=email, password=password2)
                messages.success(request, f'Account has been successfully created for you')

                return render(request, 'accounts/signin.html', {'title': 'Giriş'})

            else:
                messages.error(request, "Parollar uyğun gəlmədi!!")
                
                return render(request, 'accounts/signup.html', {'title': 'Qeydiyyat'})

        messages.error(request, "Bütün xanalar doldurulmalıdır!")
        
        return render(request, 'accounts/signup.html', {'title': 'Qeydiyyat'})

