from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Objective


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    email = forms.EmailField(max_length=254, help_text='Required')
    user_type = forms.CharField(max_length=30, required=True, help_text='Required')
    contact = forms.CharField(max_length=30, required=True, help_text='Required')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'user_type', 'contact', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=254, help_text='Required')

    class Meta:
        model = CustomUser
        fields = ('email',  'password')


class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = ('code',  'name', 'service_output')
