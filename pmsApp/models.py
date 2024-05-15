from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid



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
    REQUIRED_FIELDS = ['email', 'password',]

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