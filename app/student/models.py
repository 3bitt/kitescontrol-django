from django.db import models
from django.urls import reverse
from .validators import validate_name, validate_mobile, validate_weight


class Student(models.Model):

    IKO_LEVELS = (
        (
            'Level 1 - Discovery',
            (
                ('1A', '1A'),
                ('1B', '1B'),
                ('1C', '1C'),
                ('1D', '1D'),
                ('1E', '1E'),
            ),
        ),
        (
            'Level 2 - Intermediate',
            (
                ('2F', '2F'),
                ('2G', '2G'),
                ('2H', '2H'),
                ('2I', '2I'),
            ),
        ),
        (
            'Level 3 - Independent',
            (
                ('3J', '3J'),
                ('3K', '3K'),
                ('3L', '3L'),
                ('3M', '3M'),
                ('3N', '3N'),
            ),
        ),
        (
            'Level 4 - Advanced',
            (
                ('4O', '4O'),
                ('4P', '4P'),
                ('4Q', '4Q'),
                ('4R', '4R'),
                ('4S', '4S'),
                ('4T', '4T'),
                ('4U', '4U'),
                ('4V', '4V'),
                ('4W', '4W'),
                ('4X', '4X'),
                ('4Y', '4Y'),
            ),
        ),
    )

    WETSUIT_SIZES = (
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('S-128', 'S-128'),
        ('M-140', 'M-140'),
        ('L-146', 'L-146'),
        ('XL-152', 'XL-152'),
    )
    HARNESS_SIZES = (
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    )

    class _HOURS_REQUIRED_FOR_DISCOUNT:
        LEVEL_I = 5  # qualified for pay rate IKO_II if above 5
        LEVEL_II = 10  # qualified for pay rate IKO_III if above 10

    class _PAY_RATES_SINGLE:
        IKO_I = 160
        IKO_II = 140
        IKO_III = 130

    class _PAY_RATES_GROUP:
        IKO_I = 130
        IKO_II = 120

    name = models.CharField(
        max_length=30, null=False, blank=False, validators=[validate_name]
    )

    surname = models.CharField(
        max_length=30, null=False, blank=False, validators=[validate_name]
    )

    birth_date = models.DateField(null=True, blank=False)

    mobile_number = models.CharField(
        max_length=20, null=True, blank=False, validators=[validate_mobile]
    )

    email_address = models.CharField(max_length=40, null=True, blank=True)
    weight = models.FloatField(
        null=True, blank=True, default=0, validators=[validate_weight]
    )
    arrival_date = models.DateField(null=True, blank=True)
    leave_date = models.DateField(null=True, blank=True)
    stay_location = models.CharField(max_length=40, null=True, blank=True)
    own_car = models.BooleanField(null=True, blank=True, default=False)
    kite_elsewhere = models.BooleanField(null=True, blank=True, default=False)

    wetsuit_size = models.CharField(
        max_length=6, null=True, blank=True, choices=WETSUIT_SIZES
    )

    harness_size = models.CharField(
        max_length=3, null=True, blank=True, choices=HARNESS_SIZES
    )

    iko_id = models.IntegerField(null=True, blank=True, unique=True)
    iko_level = models.CharField(max_length=30, null=True, blank=True, choices=IKO_LEVELS)
    comment = models.CharField(max_length=255, null=True, blank=True)
    pay_rate_single = models.IntegerField(null=False, blank=False)
    pay_rate_group = models.IntegerField(null=False, blank=False)
    # HOURS_SUM - updated by LessonDetail signal
    lesson_hours_sum = models.FloatField(null=True, blank=True, default=0.0)
    register_date = models.DateTimeField(auto_now_add=True)
    # https://stackoverflow.com/questions/34275588/djangorestframework-modelserializer-datetimefield-only-converting-to-current-tim

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return reverse("student:student-detail", kwargs={"pk": self.pk})
