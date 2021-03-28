from datetime import datetime, tzinfo
from django.utils import timezone
from kitescontrol.settings import TIME_ZONE
from django.db.models.query_utils import Q
from rental.forms import RentalCreateForm
from rental.models import Rental, RentalDetail
from student.models import Student
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView


class RentalCreateView(CreateView):
    template_name = 'rental/rental_create.html'
    model = Rental
    form_class = RentalCreateForm

    def form_valid(self, form):

        dict = self.request.POST

        start_date = dict['start_date']
        end_date = dict['end_date'] or None
        student_id = dict['student']
        comment = dict.get('comment')

        rent_item = dict.getlist('rent_item')
        quantity = dict.getlist('quantity')
        item_price = dict.getlist('item_price')
        description = dict.getlist('description')

        fetch_student = Student.objects.get(id=student_id)

        rent_items = [item for item in zip(rent_item, item_price, quantity, description)]

        rental = Rental.objects.create(
            start_date = start_date,
            end_date = end_date,
            student = fetch_student,
            comment = comment
        )
        rental.save()

        for item in rent_items:
            rental_detail = RentalDetail.objects.create(
                rental = rental,
                item = item[0],
                price = item[1],
                quantity = item[2],
                description = item[3]
            )
            rental_detail.save()

        return redirect('lesson:lesson-list')
        # return super().form_valid(form)


# Class used in Lesson views.py
class RentalView():
    # rent_date = datetime.now(tz=timezone.get_current_timezone())

    @staticmethod
    def getRentalsListByDate(rentals_date=None): # rentals_date is usually current_date
        rentals = Rental.objects.filter(
            Q(created_date__date=rentals_date) |
            Q(start_date__date__lte=rentals_date) &
            Q(
                Q(end_date__date__gte=rentals_date) |
                Q(end_date__isnull=True)
                )
            )
        return rentals