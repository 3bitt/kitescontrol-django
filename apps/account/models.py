from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, is_active=True, is_staff=False, is_admin=False):
        if not username:
            raise ValueError('Username is required')
        if not password:
            raise ValueError('Password is required')
        # if not full_name:
        #     raise ValueError('Name is required')

        user_obj = self.model(
            username = username
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user        


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['full_name']

    objects = UserManager()
    
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active