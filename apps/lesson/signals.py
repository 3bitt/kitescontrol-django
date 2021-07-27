from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save, pre_delete, pre_save
from django.dispatch.dispatcher import Signal
from .models import Lesson, LessonDetail
from student.models import Student


# Send signal before Instructor is deleted to delete related User
# @receiver(post_save, sender=Lesson)
# def pre_save_lesson(sender, instance, **kwargs):
#     for stud in instance.student.all():
#             print("POST_SAVE:", stud)

# https://docs.djangoproject.com/en/dev/ref/signals/#m2m-changed
@receiver(m2m_changed, sender=Lesson.student.through)
def student_changed(sender, instance, **kwargs):

    if kwargs['action'] == 'post_remove':
        no_of_students = len(instance.student.all())
        if no_of_students < 2:
            instance.group_lesson = False
            instance.save()


    if kwargs['action'] == 'post_add':
        no_of_students = len(instance.student.all())

        if not instance.group_lesson and no_of_students > 1:
            instance.group_lesson = True
            instance.save()

@receiver(pre_save, sender=LessonDetail)
def update_student_pay_rate_signal(sender, instance, **kwargs):

    student = instance.student
    new_lesson_duration = float(instance.duration)

    is_delete_signal = kwargs.get('is_delete_signal', False)

    if is_delete_signal:
        student.lesson_hours_sum -= new_lesson_duration
        update_student_pay_rate(student, student.lesson_hours_sum)

    if instance.id is None:
        student.lesson_hours_sum += new_lesson_duration
        update_student_pay_rate(student, student.lesson_hours_sum)
    else:
        old_lesson_duration = LessonDetail.objects.get(id=instance.id).duration
        lesson_duration_change = new_lesson_duration - old_lesson_duration

        if lesson_duration_change == 0:
            return
        elif lesson_duration_change > 0:
            student.lesson_hours_sum += lesson_duration_change
            # update_student_pay_rate(student, student.lesson_hours_sum)
        elif lesson_duration_change < 0:
            student.lesson_hours_sum -= abs(lesson_duration_change)
            # update_student_pay_rate(student, student.lesson_hours_sum)
        else:
            raise AttributeError

        update_student_pay_rate(student, student.lesson_hours_sum)


# Helper function
def update_student_pay_rate(student_obj, hours_sum):
    if hours_sum < 5:
        student_obj.pay_rate_single = Student._PAY_RATES_SINGLE.IKO_I
        student_obj.pay_rate_group = Student._PAY_RATES_GROUP.IKO_I
    elif 5 <= hours_sum < 10:
        student_obj.pay_rate_single = Student._PAY_RATES_SINGLE.IKO_II
        student_obj.pay_rate_group = Student._PAY_RATES_GROUP.IKO_II
    elif hours_sum >= 10:
        student_obj.pay_rate_single = Student._PAY_RATES_SINGLE.IKO_III
        student_obj.pay_rate_group = Student._PAY_RATES_GROUP.IKO_II
    else:
        raise AttributeError
    student_obj.save()

# Purpose of this signal is to distinguish type of signal being sent -> is_delete_signal flag
@receiver(pre_delete, sender=LessonDetail)
def update_student_pay_rate_delete_signal(sender, instance, **kwargs):
    update_student_pay_rate_signal(sender, instance, is_delete_signal=True)


