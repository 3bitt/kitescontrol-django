from django.db import models


class UserType(models.TextChoices):
    CLERK = 'CLERK', 'Biuro'
    ADMIN = 'ADMIN', 'Admin'
    MANAGER = 'MANAGER', 'Manager'
    INSTRUCTOR = 'INSTRUCTOR', 'Instruktor'


class IkoLevel(models.TextChoices):
    NONE = None, 'Brak'
    COACH = 'Coach', 'Coach'
    ASSISTANT = 'ASSISTANT', 'Asystent'
    INSTRUCTOR_1 = 'INSTRUCTOR_1', 'Instruktor 1'
    INSTRUCTOR_2 = 'INSTRUCTOR_2', 'Instruktor 2'
    INSTRUCTOR_3 = 'INSTRUCTOR_3', 'Instruktor 3'
