from django.db.models import Count
from django.views.generic.edit import UpdateView
from django.db.models.query_utils import Q
from django.urls import reverse_lazy
from rental.forms import RentalCreateForm, RentalUpdateForm
from rental.models import Rental, RentalDetail
from student.models import Student
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView


class RentalCreateView(CreateView):
    template_name = 'rental/rental_create.html'
    model = Rental
    form_class = RentalCreateForm

    def form_valid(self, form):

        req_dict = self.request.POST

        start_date = req_dict['start_date']
        end_date = req_dict['end_date'] or None
        student_id = req_dict['student']
        comment = req_dict.get('comment')

        rent_item = req_dict.getlist('rent_item')
        quantity = req_dict.getlist('quantity')
        item_price = req_dict.getlist('item_price')
        description = req_dict.getlist('description')

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


class RentalDetailView(DetailView):
    template_name = 'rental/rental_detail.html'
    model = Rental
    context_object_name = 'rental'

class RentalUpdateView(UpdateView):
    template_name = 'rental/rental_edit.html'
    model = Rental
    form_class = RentalUpdateForm
    context_object_name = 'rental'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rental_id = self.get_object().id
        rental_details = RentalDetail.objects.filter(rental = rental_id)

        context['rental_details'] = rental_details
        return context

    def form_valid(self, form):

        req_dict = self.request.POST

        start_date = req_dict['start_date']
        end_date = req_dict['end_date'] or None
        student_id = req_dict['student']
        paid = True if req_dict.get('paid') else False
        comment = req_dict.get('comment')

        rent_item = req_dict.getlist('rent_item')
        quantity = req_dict.getlist('quantity')
        item_price = req_dict.getlist('item_price')
        description = req_dict.getlist('description')

        fetch_student = Student.objects.get(id=student_id)

        rent_items = [item for item in zip(rent_item, item_price, quantity, description)]

        rental = self.get_object()
        rental.start_date = start_date
        rental.end_date = end_date
        rental.student = fetch_student
        rental.paid = paid
        rental.comment = comment
        rental.save()

        RentalDetail.objects.filter(rental=rental).delete()

        for item in rent_items:
            rental_detail = RentalDetail.objects.create(
                rental = rental,
                item = item[0],
                price = item[1],
                quantity = item[2],
                description = item[3]
            )
            rental_detail.save()

        return redirect('rental:rental-detail', rental.id)


class RentalDeleteView(DeleteView):
    model = Rental
    success_url = reverse_lazy('lesson:lesson-list')


# Class used in Lesson views.py
class RentalView():
    @staticmethod
    def getRentalsListByDate(rentals_date=None): # rentals_date is usually current_date
        rentals = Rental.objects.filter(
            Q(created_date__date=rentals_date) |
            Q(start_date__date__lte=rentals_date) &
            Q(
                Q(end_date__date__gte=rentals_date) |
                Q(end_date__isnull=True)
                )
            ).order_by('-created_date')

        return rentals

    @staticmethod
    def getRentalsForSummary(rentals_due_date=None):
        rentals = Rental.objects.filter(
                Q(end_date__date=rentals_due_date)
            ).annotate(
                paid_count=Count('id',filter=Q(paid=True)),
                unpaid_count=Count('id',filter=Q(paid=False) | Q(paid__isnull=True))
        )
        # Zrobic po prostu count'a jako osobny klucz w slowniku context w widoku summary
        # do powyzszego zapytania dodac jedynie annotate i sume czasów(?) i hajsu czy cos
        return rentals