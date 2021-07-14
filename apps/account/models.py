from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager
)
from django.db.models.fields import proxy
from django.db.models.manager import BaseManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')
        # if not full_name:
        #     raise ValueError('Name is required')

        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin

        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.type = User.Types.MANAGER
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    class Types(models.TextChoices):
        CLERK = 'CLERK', 'Biuro'
        INSTRUCTOR = 'INSTRUCTOR', 'Instruktor'
        MANAGER = 'MANAGER', 'Manager'

    objects = UserManager()

    type = models.CharField('type', max_length=50, choices=Types.choices, default=Types.INSTRUCTOR)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    # staff = models.BooleanField(default=False)
    # admin = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['full_name']

    # objects = UserManager()

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self,app_label):
    #     return True

    # @property
    # def is_staff(self):
    #     return self.staff

    # @property
    # def is_admin(self):
    #     return self.admin


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
