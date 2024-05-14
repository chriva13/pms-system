from django.views.generic import TemplateView,CreateView
from .models import CustomUser
from django.urls import reverse_lazy

class HomePageView(TemplateView):
    template_name = "interface/index.html"
    
    
class ObjectivesView(TemplateView):
    template_name = "interface/objectives.html"
    
class TargetsView(TemplateView):
    template_name = "interface/targets.html"

class ArchievementView(TemplateView):
    template_name = "interface/archievement.html"
    
class ReportsView(TemplateView):
    template_name = "interface/reports.html"
    
class IndicatorsView(TemplateView):
    template_name = "interface/indicators.html"
    
class RegisterView(CreateView):
    template_name = "registration/register.html"
    model = CustomUser
    success_url = reverse_lazy("register")
    fields = ["first_name", "last_name", "email", "user_type", "contact", "password",]
    
class LoginView(TemplateView):
    template_name = "registration/login.html"
    
class ForgotPasswordView(TemplateView):
    template_name = "registration/forgotPassword.html"
    

    
