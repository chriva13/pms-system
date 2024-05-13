from django.db import models

# Create your models here.
class User(AbstractUser):
    ADMIN = 1
    USER = 2
    
    ROLE_CHOICES = ()
