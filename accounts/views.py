from django.shortcuts import render
from django.views import View


class SignInView(View):
    def get(self, request):
        return render(request, "accounts/signin_signup.html")

    def post(self, request):
        pass


class SignUpView(View):
    def post(self, request):
        pass