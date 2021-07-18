from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager
)
from django.db.models.fields import proxy
from django.db.models.manager import BaseManager

from crew.instructor.validators import validate_name

class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, type='INSTRUCTOR'):
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')
        if not name:
            raise ValueError('Name is required')
        if not surname:
            raise ValueError('Surname is required')

        user = self.model(
            email = self.normalize_email(email),
            name = name,
            surname = surname,
            type = type
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password):
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            surname = surname,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.type = User.Types.ADMIN
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    class Types(models.TextChoices):
        CLERK = 'CLERK', 'Biuro'
        INSTRUCTOR = 'INSTRUCTOR', 'Instruktor'
        MANAGER = 'MANAGER', 'Manager'
        ADMIN = 'ADMIN', 'Admin'

    objects = UserManager()

    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=30, null=False,
                            blank=False, validators=[validate_name])
    surname = models.CharField(
        max_length=30, null=False, blank=False, validators=[validate_name])
    type = models.CharField('type', max_length=50, choices=Types.choices, default=Types.INSTRUCTOR)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True


class ClerkManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CLERK)


class InstructorkManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.INSTRUCTOR)


class ManagerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.MANAGER)



class Clerk(User):
    class Meta:
        proxy = True

    objects = ClerkManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.CLERK
        return super().save(*args, **kwargs)


class Instructor(User):
    class Meta:
        proxy = True

    objects = InstructorkManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.INSTRUCTOR
        return super().save(*args, **kwargs)


class Manager(User):
    class Meta:
        proxy = True

    objects = ManagerManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.MANAGER
        return super().save(*args, **kwargs)
