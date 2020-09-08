from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class Shop(models.Model):
    """model for shop object"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_kwargs):
        """Creates and saves an user"""
        user = self.model(username=username, **extra_kwargs)
        user.set_password(password)

        if not username:
            raise ValueError("User must have an username")

        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        """Creates and saves a superuser"""
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""

    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_salesman = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    shop = models.ForeignKey(Shop, on_delete=None, null=True)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.name
