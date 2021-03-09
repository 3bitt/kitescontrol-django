from datetime import datetime, timedelta
from django.db.models.aggregates import Aggregate
from django.db.models.expressions import ExpressionWrapper, F
from django.db.models import Q, Sum
from django.db.models.fields import FloatField

from django.db.models.query import Prefetch, QuerySet
from lesson.models import Lesson, LessonDetail
from instructor.instructor.models import Instructor
from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.


class LessonSummaryView(ListView):
    template_name = 'lesson_summary/lesson_summary.html'
    queryset = Instructor.objects.filter(active=True)
    current_date = datetime.today()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if (self.kwargs):
            self.current_date = self.kwargs['summary_date']


        lessons_today = Lesson.objects.filter(start_date=self.current_date).order_by('start_time')
        context['instructors_with_lessons'] = self.queryset.prefetch_related(
            Prefetch('lessons', lessons_today)
        )
        lesson_detail = LessonDetail.objects.filter(
            Q(lesson__in=lessons_today))

        context['profit'] = lesson_detail.values('duration','pay_rate','lesson_id').annotate(
            lesson_cost=ExpressionWrapper(
                F('duration') * F('pay_rate'), output_field=FloatField())
                ).aggregate(total_profit=Sum('lesson_cost'))


        context['duration_sum'] = lesson_detail.aggregate(sum=(Sum('duration')))
        context['lesson_detail'] = lesson_detail
        context['single_lessons'] = lessons_today.filter(group_lesson=False).count()
        context['group_lessons'] = lessons_today.filter(group_lesson=True).count()
        context['completed_count'] = lessons_today.filter(completed=True).count()
        context['lessons_count'] = lessons_today.count()
        # context['hours'] = range(7,22)
        context['current_date'] = self.current_date
        context['current_time'] = datetime.today().hour

        context['previous_date'] = self.current_date - timedelta(days=1)
        context['next_date'] = datetime.date(self.current_date + timedelta(days=1))

        return context



