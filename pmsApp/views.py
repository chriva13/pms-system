from django.views.generic import TemplateView,CreateView
from .models import CustomUser
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(TemplateView):
    template_name = "interface/index.html"
    # login_url = "login/"
    
    
class ObjectivesView(TemplateView):
    template_name = "interface/objectives.html"
    # login_url = "login/"
    
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
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        Hash the password and optionally log in the user.
        """
        user = form.save(commit=False)
        user.first_name = form.cleaned_data.get("first_name")
        user.last_name = form.cleaned_data.get("last_name")
        user.email = form.cleaned_data.get("email")
        user.user_type = form.cleaned_data.get("user_type")
        user.contact = form.cleaned_data.get("contact")
        user.save()
        
        return super().form_valid(form)
    
class LoginView(TemplateView):
    template_name = "registration/login.html"
    
class ForgotPasswordView(TemplateView):
    template_name = "registration/forgotPassword.html"
    

