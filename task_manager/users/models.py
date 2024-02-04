from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, phone_number, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, name, phone_number, password, **other_fields)

    def create_user(self, email=None, name=None, phone_number=None, password=None, **other_fields):
        if not name:
            raise ValueError(_('You must provide a name'))
        if not phone_number:
            raise ValueError(_('You must provide a phone number'))

        email = self.normalize_email(email) if email else None
        user = self.model(email=email, name=name, phone_number=phone_number, **other_fields)
        user.set_password(password)
        user.save()
        return user


class RegisterUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=150)
    phone_number = models.IntegerField()
    start_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    spam = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    def __str__(self):
        return self.name


