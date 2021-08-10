from django.db import models
from django.urls import reverse
from .validators import (
    validate_name,
    validate_mobile,
    validate_weight,
    validate_available_from,
    validate_available_to
)
from account.models import User
# Create your models here.


class Instructor(models.Model):

    IKO_LEVELS = (
        (None, 'Brak'),
        ('Asystent', 'Asystent'),
        ('Instruktor 1', 'Instruktor 1'),
        ('Instruktor 2', 'Instruktor 2'),
        ('Insturktor 3', 'Instruktor 3'),
        ('Coach', 'Coach'),
    )

    name = models.CharField(max_length=30, null=False, blank=False, validators=[validate_name])
    surname = models.CharField(max_length=30, null=False, blank=False, validators=[validate_name])
    nickname = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=False, blank=False)
    mobile_number = models.CharField(max_length=20, null=True, blank=True, unique=True, validators=[validate_mobile])
    email_address = models.CharField(max_length=60, null=False, blank=False, unique=True)
    # WEIGHT - NOT USED CURRENTLY
    weight = models.FloatField(null=True, blank=True, validators=[validate_weight])
    available_from = models.DateField(null=True, blank=True, validators=[validate_available_from])
    available_to = models.DateField(null=True, blank=True, validators=[validate_available_to])
    iko_id = models.IntegerField(null=True, blank=True, unique=True)
    iko_level = models.CharField(max_length=30, null=True, blank=True, choices=IKO_LEVELS)
    driving_licence = models.BooleanField(null=True, default=False)
    pay_rate_single = models.IntegerField(null=True, blank=True)
    pay_rate_group = models.IntegerField(null=True, blank=True)
    english_lessons = models.BooleanField(null=True, blank=True, default=False)
    kids_lessons = models.BooleanField(null=True, blank=True, default=False)
    group_lessons = models.BooleanField(null=True, blank=True, default=False)
    daily_hour_limit = models.IntegerField(null=True, blank=True)
    tc_accepted_date = models.DateField(null=True, blank=True)
    tc_accepted_flag = models.BooleanField(null=True, default=False)
    active = models.BooleanField(blank=True, default=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    register_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return reverse("instructor:instructor-detail", kwargs={"pk": self.pk})

    def save(self, userType='INSTRUCTOR', * args, **kwargs):
        # When creating or updating instructor check if user with the same email already exists
        # If not, then create it, if User exists take it
        if self.id:
            instructor = Instructor.objects.get(id=self.id)
            instr_user = User.objects.get(id=instructor.user.id)
            instr_user.email = self.email_address
            instr_user.name = self.name
            instr_user.surname = self.surname
            instr_user.save()
        else:
            if userType == 'MANAGER':
                is_active = True
            else:
                is_active = False

            user = User.objects.create_user(
                email = User.objects.normalize_email(self.email_address),
                name = self.name,
                surname = self.surname,
                password = User.objects.make_random_password(length=30),
                # type = 'INSTRUCTOR'
                type = userType,
                is_active = is_active
            )
            self.user = user
        super().save(*args, **kwargs)
