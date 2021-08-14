from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.db import models

from account import constants as account_constants


class UserManager(BaseUserManager):
    DEFAULT_USER_TYPE = account_constants.UserType.INSTRUCTOR

    @staticmethod
    def _validate_type(user_type: str):
        pass  # TODO

    def create_user(self, email, name, surname, password, is_active=True, user_type=None):
        if user_type:
            self._validate_type(user_type=user_type)

        return self.model.objects.create(
            name=name,
            surname=surname,
            is_active=is_active,
            email=self.normalize_email(email),
            password=make_password(password=password),
            type=user_type or self.DEFAULT_USER_TYPE.value,
        )

    def create_superuser(self, email, name, surname, password):
        return self.model.objects.create(
            name=name,
            is_staff=True,
            is_admin=True,
            surname=surname,
            is_superuser=True,
            email=self.normalize_email(email),
            password=make_password(password=password),
            type=account_constants.UserType.ADMIN.value,
        )


class ClerkManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(type=account_constants.UserType.CLERK)
        )


class InstructorkManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(type=account_constants.UserType.INSTRUCTOR)
        )


class ManagerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(type=account_constants.UserType.MANAGER)
        )
