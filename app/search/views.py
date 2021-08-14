from datetime import datetime
import pytz
from django.conf import settings
from django.db.models.query_utils import Q
from django.views.generic import TemplateView, ListView
from rental.models import Rental
from student.models import Student
from lesson.models import Lesson


class SearchHomeView(TemplateView):
    template_name = 'search/search_home.html'


class SearchStudentAjaxView(ListView):
    template_name = 'search/search_student_res.html'
    context_object_name = 'student_search_results'
    paginate_by = 20

    def get_queryset(self):

        student_name = self.request.GET.get('name', '')
        student_mobile = self.request.GET.get('mobile', '')
        student_weight_le = self.request.GET.get('weight_le', '')
        student_weight_gt = self.request.GET.get('weight_gt', '')
        student_kite_trip = self.request.GET.get('kite_trip', False)
        student_own_car = self.request.GET.get('own_car', False)
        student_available_from = self.request.GET.get('available_from', '')
        student_available_to = self.request.GET.get('available_to', '')
        student_available_now = self.request.GET.get('student_available_now', False)

        available_from_filter = Q()
        available_to_filter = Q()

        if student_available_now == 'True':
            current_date = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
            available_from_filter = Q(arrival_date__lte=current_date)
            available_to_filter = Q(leave_date__gte=current_date)
        else:
            if student_available_from:
                available_from_filter = Q(arrival_date__lte=student_available_from)
            if student_available_to:
                available_to_filter = Q(leave_date__gte=student_available_to)

        qs = Student.objects.filter(
            Q(name__contains=student_name) | Q(surname__contains=student_name),
            Q(mobile_number__contains=student_mobile),
            Q(weight__lte=student_weight_le or 1000),
            Q(weight__gte=student_weight_gt or 0),
            Q(own_car=student_own_car) | Q(own_car=True),
            Q(kite_elsewhere=student_kite_trip) | Q(kite_elsewhere=True),
            available_from_filter,
            available_to_filter,
        ).order_by('-register_date')
        return qs


class SearchLessonAjaxView(ListView):
    template_name = 'search/search_lesson_res.html'
    context_object_name = 'lesson_search_results'
    paginate_by = 20

    def get_queryset(self):

        lesson_student = self.request.GET.get('lesson_student', None)
        lesson_instructor = self.request.GET.get('lesson_instructor', None)
        lesson_date_from = self.request.GET.get('lesson_date_from', '')
        lesson_date_to = self.request.GET.get('lesson_date_to', '')
        lesson_is_single = self.request.GET.get('lesson_is_single', False)
        lesson_is_group = self.request.GET.get('lesson_is_group', False)

        lesson_student_filter = Q()
        lesson_instructor_filter = Q()
        group_filter = Q()
        date_from = Q()
        date_to = Q()

        if lesson_student:
            student_split = lesson_student.split(' ')
            if len(student_split) > 1:
                lesson_student_filter = Q(student__name__contains=student_split[0]) | Q(
                    student__surname__contains=student_split[1]
                )
            else:
                lesson_student_filter = Q(student__name__contains=lesson_student) | Q(
                    student__surname__contains=lesson_student
                )

        if lesson_instructor:
            instructor_split = lesson_instructor.split(' ')
            if len(instructor_split) > 1:
                instr_full_name = lesson_instructor
                lesson_instructor_filter = Q(
                    instructor__name__contains=instructor_split[0]
                ) | Q(instructor__surname__contains=instructor_split[1])
            else:
                lesson_instructor_filter = Q(
                    instructor__name__contains=lesson_instructor
                ) | Q(instructor__surname__contains=lesson_instructor)

        if lesson_date_from:
            date_from = Q(start_date__gte=lesson_date_from)
        if lesson_date_to:
            date_to = Q(start_date__lte=lesson_date_to)

        if (lesson_is_single == 'True') and (lesson_is_group == 'True'):
            pass
        elif lesson_is_single == 'True':
            group_filter = Q(group_lesson=False)
        elif lesson_is_group == 'True':
            group_filter = Q(group_lesson=True)
        else:
            pass

        qs = (
            Lesson.objects.filter(
                lesson_student_filter,
                lesson_instructor_filter,
                group_filter,
                date_from,
                date_to,
            )
            .distinct()
            .order_by('-start_date')
        )

        return qs


class SearchRentalAjaxView(ListView):
    template_name = 'search/search_rental_res.html'
    context_object_name = 'rental_search_results'
    paginate_by = 20

    def get_queryset(self):

        rental_student = self.request.GET.get('rental_student', '')
        rental_start_date = self.request.GET.get('rental_start_date', '')
        rental_end_date = self.request.GET.get('rental_end_date', '')
        rental_created_date = self.request.GET.get('rental_created_date', '')
        rental_paid = self.request.GET.get('rental_paid', '')
        rental_item = self.request.GET.get('rental_item', '')

        rental_created_filter = Q()
        rental_start_filter = Q()
        rental_end_filter = Q()

        rental_paid_filter = Q()

        if rental_created_date:
            rental_created_filter = Q(created_date__date=rental_created_date)
        if rental_start_date:
            rental_start_filter = Q(start_date__date__gte=rental_start_date)
        if rental_end_date:
            rental_end_filter = Q(end_date__date__lte=rental_end_date)

        if rental_paid != '':
            rental_paid_filter = Q(paid=rental_paid)

        qs = (
            Rental.objects.filter(
                Q(student__name__contains=rental_student)
                | Q(student__surname__contains=rental_student),
                rental_created_filter,
                rental_paid_filter,
                Q(rentaldetail__item__contains=rental_item),
                rental_start_filter,
                rental_end_filter,
            )
            .distinct()
            .order_by('-created_date')
        )

        return qs
