from allauth.account.views import SignupView, LoginView
from django.urls import reverse_lazy

class CustomSignupView(SignupView):
    template_name = 'accounts/signup.html'

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"  
