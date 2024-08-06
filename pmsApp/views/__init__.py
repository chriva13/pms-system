from pmsApp.views.objectives import *
from pmsApp.views.targets import *
from pmsApp.views.indicators import *
from pmsApp.views.indicator_values import *
from pmsApp.views.achievements import *
from pmsApp.views.datas import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from pmsApp.forms import CustomUserCreationForm
from pmsApp.models import Objective, CustomUser, Indicator, Target, Report


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "interface/index.html"
    login_url = "login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all().count()  # Get all objectives
        context['objectives'] = Objective.objects.all().count()  # Get all objectives
        context['indicators'] = Indicator.objects.all().count()  # Get all objectives
        context['targets'] = Target.objects.all().count()  # Get all objectives
        context['achievements'] = Achievement.objects.all().count()  # Get all objectives
        return context


class ObjectivesView(TemplateView):
    template_name = "interface/objectives.html"
    login_url = "login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objectives'] = Objective.objects.all()  # Get all objectives
        return context


class TargetsView(TemplateView):
    template_name = "interface/targets.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['targets'] = Target.objects.all()  # Get all targets
        return context


def construct_percent(achievement: Achievement):
    percent = int(achievement.indicator_value.target_value) / int(achievement.target_value)
    return percent * 100


class AchievementView(TemplateView):
    template_name = "interface/archievement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        achievements = Achievement.objects.all()
        context['achievements'] = [{'indicator_value': a.indicator_value, 'target_value': a.target_value, 'id': a.id, 'percent': construct_percent(a)}
                                   for a in achievements]

        return context


class DatasView(TemplateView):
    template_name = "interface/datas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_sources'] = DataSource.objects.all()
        context['data_collection_methods'] = DataCollectionMethod.objects.all()

        return context


class ReportsView(TemplateView):
    template_name = "reports/all.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = Report.objects.all()
        return context


class IndicatorsView(TemplateView):
    template_name = "interface/indicators.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['indicators'] = Indicator.objects.all()  # Get all indicators
        return context


class IndicatorsValueView(TemplateView):
    template_name = "interface/indicator-values.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['values'] = IndicatorValue.objects.all()  # Get all indicator values
        return context


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


class ForgotPasswordView(TemplateView):
    template_name = "registration/forgotPassword.html"
