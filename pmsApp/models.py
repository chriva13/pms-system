from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from pmsApp.manager import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    USER_CHOICES = (
        ("admin", "admin"),
        ("hod", "hod"),
        ("manager", "institute_manager"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    user_type = models.CharField(max_length=30, choices=USER_CHOICES)

    # Remove the username field
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'user_type', 'contact']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Objective(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    service_output = models.CharField(max_length=255)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.code} - {self.name}'


class Target(models.Model):

    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DataSource(models.Model):
    name: str = models.CharField(max_length=255)  # not necessary to add type hint

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DataCollectionMethod(models.Model):
    name = models.CharField(max_length=255)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Indicator(models.Model):
    WORDS, NUMBER = 'words', 'number'
    ANNUALLY, QUARTERLY, MONTHLY = 'Annually', 'Quarterly', 'Monthly'

    TYPE_CHOICES = (
        (WORDS, 'Words'),
        (NUMBER, 'Number')
    )

    FREQUENCY_CHOICES = (
        (WORDS, 'Annually'),
        (QUARTERLY, 'Quarterly'),
        (MONTHLY, 'Monthly')
    )

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    target = models.ForeignKey(Target, on_delete=models.CASCADE)

    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    data_collection_method = models.ForeignKey(DataCollectionMethod, on_delete=models.CASCADE)

    type = models.CharField(choices=TYPE_CHOICES, max_length=255)
    frequency = models.CharField(choices=FREQUENCY_CHOICES, max_length=255)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class IndicatorValue(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    period = models.CharField(max_length=255)
    target_value = models.CharField(max_length=255)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.period} - Value: {self.target_value}'


class Achievement(models.Model):
    indicator_value = models.ForeignKey(IndicatorValue, on_delete=models.CASCADE)
    target_value = models.CharField(max_length=255)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

