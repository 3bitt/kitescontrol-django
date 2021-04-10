from django.db.models import F, Prefetch
from django.db.models.aggregates import Count, Sum
from django.db.models.expressions import ExpressionWrapper, Value
from django.db.models.fields import DecimalField
from django.db.models.functions.comparison import Coalesce
from django.db.models.query_utils import Q
from django.views.generic import TemplateView
from django_ajax.mixin import AJAXMixin
from instructor.instructor.models import Instructor
from lesson.models import Lesson


class PayrollHomeView(TemplateView):
    template_name = 'payroll/payroll_home.html'


class PayrollByDate(AJAXMixin, TemplateView):
    template_name = 'payroll/payroll_by_date_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        payroll_start_date = self.request.GET['dateFrom']
        payroll_end_date = self.request.GET['dateTo']

        filtered_lessons = Lesson.objects.filter(
            Q(start_date__gte=payroll_start_date,
                start_date__lte=payroll_end_date),
            Q(instructor=F('instructor'))
        )

        instructors = Instructor.objects.filter(
            Q(active=True),
            Q(lessons=F('lessons')),
            Q(lessons__start_date__gte=payroll_start_date,
              lessons__start_date__lte=payroll_end_date)
        ).prefetch_related(
            Prefetch('lessons', filtered_lessons)
        ).annotate(
            single_lessons_count=Count(
                'lessons', filter=Q(lessons__group_lesson=False)),
            single_lessons_duration=Sum(
                'lessons__duration', filter=Q(lessons__group_lesson=False)),
            group_lessons_count=Count(
                'lessons', filter=Q(lessons__group_lesson=True)),
            group_lessons_duration=Sum(
                'lessons__duration', filter=Q(lessons__group_lesson=True)),
            single_lessons_value=ExpressionWrapper(
                Coalesce(F('single_lessons_duration'), Value(0.0)
                         ) * Coalesce(F('pay_rate_single'), Value(0.0)),
                output_field=DecimalField(decimal_places=2)),
            group_lessons_value=ExpressionWrapper(
                Coalesce(F('group_lessons_duration'), Value(0.0)
                         ) * Coalesce(F('pay_rate_group'), Value(0.0)),
                output_field=DecimalField(decimal_places=2))
        ).annotate(
            payroll_sum=F('single_lessons_value') + F('group_lessons_value')
        )

        context['instructors'] = instructors

        return context
