from django.db.models.query_utils import Q
from django.views.generic import TemplateView, ListView
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

        available_from_filter = Q()
        available_to_filter = Q()

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
            available_to_filter
        ).order_by('-register_date')
        return qs


class SearchLessonAjaxView(ListView):
    template_name = 'search/search_lesson_res.html'
    context_object_name = 'lesson_search_results'
    paginate_by = 20

    def get_queryset(self):

        lesson_student = self.request.GET.get('lesson_student', '')
        lesson_instructor = self.request.GET.get('lesson_instructor', '')
        lesson_date_from = self.request.GET.get('lesson_date_from', '')
        lesson_date_to = self.request.GET.get('lesson_date_to', '')
        lesson_is_single = self.request.GET.get('lesson_is_single', False)
        lesson_is_group = self.request.GET.get('lesson_is_group', False)

        date_from = Q()
        date_to = Q()
        group_filter = Q()

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

        qs = Lesson.objects.filter(
            Q(student__name__contains=lesson_student) | Q(
                student__surname__contains=lesson_student),
            Q(instructor__name__contains=lesson_instructor) | Q(
                instructor__surname__contains=lesson_instructor),
            group_filter,
            date_from,
            date_to
        ).distinct(
        ).order_by('-start_date')

        return qs

