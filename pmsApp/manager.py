from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model where the email address is the unique identifier
    and has an is_admin field to allow access to the admin app
    """
    def create_admin(self, email, full_name, password=None, cellphone=None):
        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        if not full_name:
            raise ValueError(_("User must have a full name"))
        if not cellphone:
            raise ValueError(_("User must have a phone number"))

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.full_name = full_name
        user.cellphone = cellphone
        user.role = user.ADMIN
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user

    def create_customer(self, email, full_name, password=None, cellphone=None):
        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        if not full_name:
            raise ValueError(_("User must have a full name"))
        if not cellphone:
            raise ValueError(_("User must have a phone number"))

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.full_name = full_name
        user.cellphone = cellphone
        user.role = user.CUSTOMER
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.save()
        return user

    def create_employee(self, email, full_name, password=None, cellphone=None):
        if not email:
            raise ValueError(_("User must have an email"))
        if not password:
            raise ValueError(_("User must have a password"))
        if not full_name:
            raise ValueError(_("User must have a full name"))
        if not cellphone:
            raise ValueError(_("User must have a phone number"))

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = full_name
        user.set_password(password)  # change password to hash
        user.cellphone = cellphone
        user.role = user.EMPLOYEE
        user.is_admin = False
        user.is_staff = True
        user.save()
        return user

    def create_manager(self, email, full_name, password=None, cellphone=None):
        if not email:
            raise ValueError(_("User must have an email"))
        if not password:
            raise ValueError(_("User must have a password"))
        if not full_name:
            raise ValueError(_("User must have a full name"))
        if not cellphone:
            raise ValueError(_("User must have a phone number"))

        user = self.model(
            email=self.normalize_email(email)
        )
        user.full_name = full_name
        user.set_password(password)
        user.cellphone = cellphone
        user.role = user.MANAGER
        user.is_admin = False
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, email, password=None, contact=None, user_type=None):
        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        if not user_type:
            raise ValueError(_("User must have a type"))
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_admin = False
        user.contact = contact
        user.user_type = user_type
        user.is_superuser = True
        user.save()
        return user
