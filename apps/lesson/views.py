from rental.views import RentalView
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.db.models import Q
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from crew.instructor.models import Instructor
from student.models import Student
from .models import Lesson, LessonDetail
from datetime import datetime, timedelta
import datetime as datetimeModule
from .forms import LessonCreateForm
from django.urls import reverse_lazy
from django.core.serializers import serialize
from django.db.models import Prefetch

# LESSON STATUSES:
# 0 - CREATED
# 1 - CONFIRMED
# 2 - COMPLETED

class LessonListView(ListView):
    current_date = datetime.now()

    # current_date = date.today()
    queryset = Instructor.objects.filter(active=True)
    template_name = 'lesson/lesson_list.html'
    # context_object_name = 'instructors_all'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if (self.kwargs):
            self.current_date = self.kwargs['schedule_date']

        lessons_today = Lesson.objects.filter(start_date=self.current_date).order_by('start_time')
        context['instructors_with_lessons'] = self.queryset.prefetch_related(
            Prefetch('lessons', lessons_today)
        )

        context['hours'] = range(7,22)
        context['current_date'] = self.current_date
        context['current_time'] = datetime.today().hour

        context['previous_date'] = self.current_date - timedelta(days=1)
        context['next_date'] = datetime.date(self.current_date + timedelta(days=1))

        context['rentals_list'] = RentalView.getRentalsListByDate(self.current_date)

        return context


class LessonDetailView(DetailView):
    queryset = Lesson.objects.all()
    template_name = 'lesson/lesson_detail.html'
    context_object_name = 'lesson'


class LessonCreateView(CreateView):
    current_date = datetime.now()
    model = Lesson
    template_name = 'lesson/lesson_create.html'
    form_class = LessonCreateForm
    success_url = reverse_lazy('lesson:lesson-list')

    students_query = Student.objects.filter(
            Q(arrival_date__lte=current_date),
            Q(leave_date__gte=current_date)
        ).order_by('-register_date', '-surname')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)  # Get the form as usual
        form.fields['instructor'].queryset = Instructor.objects.filter(active=True).order_by('surname')
        form.fields['student'].queryset = self.students_query
        form.fields['duration'].initial = 2
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students_query"] = serialize('json',
            self.students_query,
            )
        return context

    def form_valid(self, form: LessonCreateForm):
        start_hour = int(self.request.POST['start_hour'])
        start_minute = int(self.request.POST['start_minute'])
        start_time = datetimeModule.time(start_hour,start_minute)
        form.instance.start_time = start_time

        if len(form.cleaned_data['student']) > 1:
            form.instance.group_lesson = True
        else:
            form.instance.group_lesson = False

        if form.cleaned_data['start_date'] != datetime.date(self.current_date):
            lesson_date = form.cleaned_data['start_date'].strftime('%d-%m-%Y')
            self.success_url = reverse_lazy('lesson:lesson-list', kwargs={'schedule_date': lesson_date})

        response = super(LessonCreateView, self).form_valid(form)

        return response

class LessonUpdateView(UpdateView):
    current_date = datetime.now()
    model = Lesson
    template_name = 'lesson/lesson_edit.html'
    form_class = LessonCreateForm
    success_url = reverse_lazy('lesson:lesson-list')

    def form_valid(self, form: LessonCreateForm):
        start_hour = int(self.request.POST['start_hour'])
        start_minute = int(self.request.POST['start_minute'])
        start_time = datetimeModule.time(start_hour,start_minute)
        form.instance.start_time = start_time

        if form.cleaned_data['start_date'] != datetime.date(self.current_date):
            lesson_date = form.cleaned_data['start_date'].strftime('%d-%m-%Y')
            self.success_url = reverse_lazy('lesson:lesson-list', kwargs={'schedule_date': lesson_date})
        response = super(LessonUpdateView, self).form_valid(form)

        # return super().form_valid(form)
        return response

    # def get_success_url(self):
    #     return reverse_lazy('lesson:lesson-list')


class LessonConfirmView(View):

    def post(self, request, **kwargs):
        lesson_id = self.kwargs['pk']
        lesson: Lesson = Lesson.objects.get(id=lesson_id)

        if (lesson.confirmed):
            lesson.confirmed = False
        elif (not lesson.confirmed):
            lesson.confirmed = True
        else:
            pass
        lesson.save()

        lesson_date = lesson.start_date.strftime('%d-%m-%Y')

        return redirect('lesson:lesson-list', lesson_date)


class LessonStartView(View):

    def post(self, request, **kwargs):
        lesson_id = self.kwargs['pk']
        lesson = Lesson.objects.get(id=lesson_id)
        if (lesson.in_progress):
            lesson.in_progress = False
            lesson.confirmed = False
        elif (not lesson.in_progress):
            lesson.in_progress = True
            lesson.confirmed = True
        else:
            lesson.in_progress = False
            lesson.confirmed = False
        lesson.save()

        lesson_date = lesson.start_date.strftime('%d-%m-%Y')

        return redirect('lesson:lesson-list', lesson_date)


# Only group lessons
class LessonSplit(View):

    def post(self, *args, **kwargs):

        req_dict = self.request.POST
        lesson_id = self.kwargs['pk']

        student_time_spent = float(req_dict['time_spent'])
        leave_stud_id =  req_dict['leaving_student_id']

        target_lesson = Lesson.objects.get(id=lesson_id)
        leaving_student = target_lesson.student.get(id=leave_stud_id)

        #
        # Update lesson which is being splitted
        #
        target_lesson.duration = student_time_spent
        target_lesson.in_progress = False
        target_lesson.completed = True
        target_lesson.comment = ' '.join(filter(None, (target_lesson.comment, f'[SYSTEM]: Lekcja została rozdzielona: {leaving_student} opuścił lekcje')))
        target_lesson.save()

        students_staying = []

        for student in target_lesson.student.all():

            student_pay_rate = student.pay_rate_group

            lesson_detail_object, created = LessonDetail.objects.update_or_create(
                lesson=target_lesson, student=student,
                defaults = {
                    'lesson': target_lesson,
                    'student': student,
                    'duration': student_time_spent,
                    'pay_rate': int(student_pay_rate),
                    'price': int(student_pay_rate) * student_time_spent,
                    'iko_level_achieved': student.iko_level
                }
            )

            if not str(student.id) == leave_stud_id:
                students_staying.append(student.id)

        #
        # Create new lesson
        #
        start_time_offset = (datetime.combine(
                target_lesson.start_date,
                target_lesson.start_time
                ) + timedelta(hours=student_time_spent)
            ).time()

        new_lesson = Lesson.objects.create(
            start_date = target_lesson.start_date,
            start_time = start_time_offset,
            group_lesson = True if len(students_staying) > 2 else False,
            duration = 1,
            paid = False,
            kite_brand = target_lesson.kite_brand,
            board = target_lesson.board,
            comment = f'[SYSTEM]: Lekcja stworzona wskutek rozdzielenia',
            confirmed = True,
            in_progress = True,
            completed = False
        )

        new_lesson.student.set(students_staying)
        new_lesson.instructor.set(list(target_lesson.instructor.values_list(flat=True)))
        new_lesson.save()

        lesson_date = target_lesson.start_date.strftime('%d-%m-%Y')

        return redirect('lesson:lesson-list', lesson_date)


class LessonCompleteView(View):

    def post(self, request, **kwargs):
        lesson_id = self.kwargs['pk']
        lesson: Lesson = Lesson.objects.get(id=lesson_id)
        request_dict = self.request.POST

        for key in request_dict:
            if key.startswith('new_iko_level'):
                student_id = key.split('_')[-1]
                for student in lesson.student.all():
                    if student.id == int(student_id):
                        student.iko_level = request_dict[key]
                        student.save()

                        if lesson.group_lesson:
                            student_pay_rate = student.pay_rate_group
                        else:
                            student_pay_rate = student.pay_rate_single

                        # student_lesson_time = float(request_dict[f'student_lesson_duration_{student_id}'])
                        student_lesson_time = float(request_dict['duration'])

                        lesson_detail_object, created = LessonDetail.objects.update_or_create(
                            lesson=lesson, student=student,
                            defaults = {
                                'lesson': lesson,
                                'student': student,
                                'duration': student_lesson_time,
                                'pay_rate': int(student_pay_rate),
                                'price': int(student_pay_rate) * student_lesson_time,
                                'iko_level_achieved': request_dict[key]
                            }
                        )

        lesson.duration = request_dict['duration']
        lesson.completed = True
        lesson.in_progress = False
        lesson.save()

        lesson_date = lesson.start_date.strftime('%d-%m-%Y')

        return redirect('lesson:lesson-list', lesson_date)


class LessonEditAfterComplete(View):
    http_method_names = ['get', 'post']
    template_name = 'lesson/lesson_edit_after_complete.html'

    def get(self, request, *args, **kwargs):

        lesson_id = self.kwargs.get('pk')
        if lesson_id:
            lesson = Lesson.objects.get(id=lesson_id)
            context = {'lesson': lesson}
            return render(request, self.template_name, context)
        return

    def post(self, request, *args, **kwargs):

        lesson_id = self.kwargs.get('pk')
        if lesson_id:
            lesson = Lesson.objects.get(id=lesson_id)
            new_duration = request.POST.get('duration')
            lesson.duration = new_duration

            detail = LessonDetail.objects.filter(lesson=lesson)
            for detail in detail:
                detail.duration = new_duration
                detail.price = float(new_duration) * int(detail.pay_rate)
                detail.save()

            lesson.save()
            lesson_date = lesson.start_date.strftime('%d-%m-%Y')
            return redirect('lesson:lesson-list', lesson_date)
        return

class LessonMarkAsPaidView(View):

    def post(self, *args, **kwargs):
        lesson_id = self.kwargs['pk']
        lesson = Lesson.objects.get(id=lesson_id)

        lesson.paid = True
        lesson.save()

        return redirect(self.request.META['HTTP_REFERER'])


class LessonDeleteView(DeleteView):
    model = Lesson
    success_url = reverse_lazy('lesson:lesson-list')


class FindScheduleRedirectView(View):
    http_method_names = ['get']
    def get(self, request):
        request_date = request.GET['schedule_date']
        request_date_clean = datetime.strptime(request_date, '%Y-%m-%d').astimezone().strftime('%d-%m-%Y')
        return redirect('lesson:lesson-list', request_date_clean)
