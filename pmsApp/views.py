from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views.generic import TemplateView,CreateView
from .models import CustomUser
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, LoginForm, ObjectiveForm
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "interface/index.html"
    login_url = "login/"
    
    
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
    # form_class = LoginForm
    # success_url = reverse_lazy("home")

    # def form_valid(self, form):
    #
    #     username = form.cleaned_data.get('email')
    #     password = form.cleaned_data.get('password')
    #     user = authenticate(email=username, password=password)
    #     if user is not None:
    #         login(self.request, user)
    #
    #         return super().form_valid(form)
    #
    #     messages.error(self.request, "Invalid username or password.")
    #     return None


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print('Valid')
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try:
                found_user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                messages.error(request, "User does not exist")
                return redirect('/login')

            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('/login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/login')


def add_objective(request):
    if request.method == "POST":
        form = ObjectiveForm(request, data=request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            name = form.cleaned_data.get('name')
            service_output = form.cleaned_data.get('service_output')

            return super().form_valid(form)
        else:
            messages.error(request, "Invalid request")
            return redirect('/login')


class ForgotPasswordView(TemplateView):
    template_name = "registration/forgotPassword.html"
    

