from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from account import constants as account_constants
from account import managers
from account import validators as account_validators


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        validators=[
            account_validators.validate_name
        ],  # TODO - better validate_name func name
    )
    surname = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        validators=[
            account_validators.validate_name
        ],  # TODO - better validate_name func name
    )
    type = models.CharField(
        'type',
        max_length=50,
        choices=account_constants.UserType.choices,
        default=account_constants.UserType.INSTRUCTOR,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=100, unique=True)

    objects = managers.UserManager()

    def __str__(self):
        return self.emailf

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class ClerkProfile(models.Model):
    user = models.OneToOneField(
        'account.User', on_delete=models.CASCADE, related_name='profile'
    )


class InstructorProfile(models.Model):
    iko_level = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=account_constants.IkoLevel.choices,
        default=account_constants.IkoLevel.NONE,
    )
    weight = models.FloatField(
        null=True,
        blank=True,
        validators=[account_validators.validate_weight],  # TODO - should we remove weight
    )
    mobile_number = models.CharField(
        null=True,
        blank=True,
        unique=True,
        max_length=20,
        validators=[account_validators.validate_mobile],
    )
    active = models.BooleanField(blank=True, default=True)
    email_address = models.CharField(
        max_length=60, null=False, blank=False, unique=True
    )  # TODO - user has email, wtf?
    birth_date = models.DateField(null=False, blank=False)
    register_date = models.DateTimeField(auto_now_add=True)
    tc_accepted_date = models.DateField(null=True, blank=True)
    pay_rate_group = models.IntegerField(null=True, blank=True)
    pay_rate_single = models.IntegerField(null=True, blank=True)
    daily_hour_limit = models.IntegerField(null=True, blank=True)
    driving_licence = models.BooleanField(null=True, default=False)
    tc_accepted_flag = models.BooleanField(null=True, default=False)
    iko_id = models.IntegerField(null=True, blank=True, unique=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    user = models.OneToOneField(
        'account.User', on_delete=models.CASCADE, related_name='profile'
    )
    kids_lessons = models.BooleanField(null=True, blank=True, default=False)
    group_lessons = models.BooleanField(null=True, blank=True, default=False)
    english_lessons = models.BooleanField(null=True, blank=True, default=False)
    available_to = models.DateField(
        null=True, blank=True, validators=[account_validators.validate_available_to]
    )
    available_from = models.DateField(
        null=True, blank=True, validators=[account_validators.validate_available_from]
    )


class ManagerProfile(models.Model):
    user = models.OneToOneField(
        'account.User', on_delete=models.CASCADE, related_name='profile'
    )


# class Clerk(User):
#     class Meta:
#         proxy = True
#
#     objects = managers.ClerkManager()
#
#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.type = User.Types.CLERK
#         return super().save(*args, **kwargs)
#
#
# class Instructor(User):
#     class Meta:
#         proxy = True
#
#     objects = managers.InstructorkManager()
#
#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.type = User.Types.INSTRUCTOR
#         return super().save(*args, **kwargs)
#
#
# class Manager(User):
#     class Meta:
#         proxy = True
#
#     objects = managers.ManagerManager()
#
#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.type = User.Types.MANAGER
#         return super().save(*args, **kwargs)
