from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import DateInput

from .models import CustomUser, Objective, Indicator, Target, IndicatorValue, Achievement, DataSource, \
    DataCollectionMethod


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
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objective Code'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objective Name'}),
            'service_output': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Service'}),
        }


class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = ['objective', 'name', 'description']
        widgets = {
            'objective': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Target Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = ['name', 'description', 'target', 'type', 'frequency', 'data_source', 'data_collection_method']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Indicator Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'target': forms.Select(attrs={'class': 'form-control'}),
            'data_source': forms.Select(attrs={'class': 'form-control'}),
            'data_collection_method': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
        }


class MonthYearWidget(DateInput):
    input_type = 'month'

    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control', 'type': 'month', 'placeholder': 'Select Month and Year'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class IndicatorValueForm(forms.ModelForm):
    class Meta:
        model = IndicatorValue
        fields = ['period', 'target_value']
        widgets = {
            'period': MonthYearWidget(),
            'target_value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Target Value'}),
        }


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['indicator_value', 'target_value']
        widgets = {
            'indicator_value': forms.Select(attrs={'class': 'form-control'}),
            'target_value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Target Value'}),
        }

    indicator = forms.ModelChoiceField(
        queryset=Indicator.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'indicator-select'}),
        required=True
    )


# forms.py
class DataSourceForm(forms.ModelForm):
    class Meta:
        model = DataSource
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        }


class DataCollectionMethodForm(forms.ModelForm):
    class Meta:
        model = DataCollectionMethod
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        }


