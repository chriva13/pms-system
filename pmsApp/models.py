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

    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    service_output = models.CharField(max_length=255)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)


class Indicator(models.Model):
    WORDS, NUMBER = 'words', 'number'
    TYPE_CHOICES = (
        (WORDS, 'Words'),
        (NUMBER, 'Number')
    )

    ANNUALLY, QUARTERLY, MONTHLY = 'Annually', 'Quarterly', 'Monthly'
    FREQUENCY_CHOICES = (
        (WORDS, 'Annually'),
        (QUARTERLY, 'Quarterly'),
        (MONTHLY, 'Monthly')
    )

    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    type = models.CharField(choices=TYPE_CHOICES, max_length=255)
    frequency = models.CharField(choices=FREQUENCY_CHOICES, max_length=255)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)


class Target(models.Model):

    name = models.CharField(max_length=255)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    year = models.CharField(max_length=255)
    indicator_target_value = models.CharField(max_length=255)

