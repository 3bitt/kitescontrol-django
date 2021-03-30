from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from student.models import Student


# To be extended in future

class Rental(models.Model):

    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=DO_NOTHING)
    paid = models.BooleanField(default=False, null=True, blank=True)
    paid_date = models.DateTimeField(null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'Rent item for {self.student}'

class RentalDetail(models.Model):

    class RentItem(models.TextChoices):
        WETSUIT = 'WETSUIT', 'Pianka'
        HELMET = 'HELMET', 'Kask'
        LIFE_JACKET = 'LIFE_JACKET', 'Kamizelka ratunkowa'
        HARNESS = 'HARNESS', 'Trapez'
        LEASH = 'LEASH', 'Leash'
        BOARD = 'BOARD', 'Deska'
        KITE = 'KITE', 'Kite'

        __empty__ = ('UNKNOWN')


    rental = models.ForeignKey(Rental, on_delete=CASCADE)
    item = models.CharField(max_length=12, choices=RentItem.choices)
    price = models.FloatField(null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'Rent detail for {self.rental}'

    def get_rent_item_display(self):

        return {
            'WETSUIT': 'Pianka',
            'HELMET': 'Kask',
            'LIFE_JACKET': 'Kamizelka rat.',
            'HARNESS': 'Trapez',
            'LEASH': 'Leash',
            'BOARD': 'Deska',
            'KITE': 'Kite'
        }.get(self.item, f'Błąd - nie znam takiej rzeczy jak {self.item}')