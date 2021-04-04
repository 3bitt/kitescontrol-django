from datetime import timedelta, datetime
from decimal import Decimal, ROUND_HALF_EVEN
from django.db.models.aggregates import Aggregate, Sum
from django.db.models.functions import Cast
from django.db.models import Count
from django.db.models.expressions import ExpressionWrapper, F, OuterRef, Subquery, Value
from django.db.models.fields import DecimalField, DurationField, FloatField, IntegerField
from django.db.models import Prefetch
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
        end_date = req_dict.get('end_date') or None
        student_id = req_dict['student']
        paid = True if req_dict.get('paid') else False
        comment = req_dict.get('comment')

        rent_item = req_dict.getlist('rent_item')
        quantity = req_dict.getlist('quantity')
        item_price = req_dict.getlist('item_price')
        description = req_dict.getlist('description')

        fetch_student = Student.objects.get(id=student_id)

        rent_items = [item for item in zip(rent_item, item_price, quantity, description)]

        # ed = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

        rental = self.get_object()
        # print(dir(rental.end_date))
        rental.start_date = start_date
        rental.end_date = end_date
        rental.student = fetch_student
        rental.paid = paid
        rental.comment = comment
        print(rental.end_date)
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
    def getRentalsForSummary(current_date=None):

        result_dict = {}

        created_today_filter = Q(created_date__date=current_date)
        ends_today_filter = Q(end_date__date=current_date)
        paid_filter = Q(paid=True)
        unpaid_filter = Q(Q(paid=False) | Q(paid__isnull=True))

        rentals = Rental.objects.filter(
            ends_today_filter).annotate(
            rent_duration=ExpressionWrapper(
                ( (F('end_date')  - F('start_date')) * 0.000001 \
                / Value('3600', IntegerField() )),
                output_field=DecimalField(decimal_places=1)
            )
        )

        rent_subquery = rentals.filter(rentaldetail=OuterRef('id'))

        rentals_detail = RentalDetail.objects.filter(
            rental__in=rentals
        ).select_related('rental'
        ).annotate(
            rent_duration=Subquery(
                rent_subquery.values('rent_duration')
            )
        ).annotate(
            item_rent_gross_amt=ExpressionWrapper(
                F('rent_duration') * F('price') * F('quantity'),
                output_field=FloatField()
            )
        )

        rent_detail_subquery = rentals_detail.filter(rental_id=OuterRef('id')).values('item_rent_gross_amt')
        test = rent_detail_subquery.values('rental_id').annotate(total=Sum('item_rent_gross_amt')).values('total')

        rentals = rentals.prefetch_related(
            Prefetch('rentaldetail_set', rentals_detail)
        ).annotate(
            total_rent_amt=Subquery(test)
        )

        students_with_rentals =  Student.objects.filter(
            Q(rental__in=rentals)
            ).prefetch_related(
                Prefetch('rental_set', rentals)
            ).annotate(
                student_total_rent_amt=Subquery(
                    rentals.values('student_id').annotate(
                        total_amt=Sum('total_rent_amt')).values('total_amt')
                )
            ).order_by('name').distinct()

        # Aggregates used for overall summary

        rentals_counts = rentals.aggregate(
            ends_today=Count('*'),
            paid=Count('paid', filter=paid_filter),
        )
        total_rentals_value = rentals_detail.aggregate(
            sum=Sum('item_rent_gross_amt')
        )

        result_dict['count'] = rentals_counts
        result_dict['total_profit'] = total_rentals_value
        result_dict['students'] = students_with_rentals

        return result_dict