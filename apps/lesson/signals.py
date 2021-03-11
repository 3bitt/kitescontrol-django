from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save, pre_delete, pre_save
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

    if kwargs['action'] == 'pre_clear':
        print('PRE_CLEAR ACTION !!!!!! -----------')

    if kwargs['action'] == 'post_remove':
        print('PRE_REMOVE ACTION !!!!!! -----------')
        no_of_students = len(instance.student.all())
        print(no_of_students)
        if no_of_students < 2:
            instance.group_lesson = False
            instance.save()


    if kwargs['action'] == 'post_add':
        print('SIGNAL - ADD: pk_set:', kwargs['pk_set'])
        no_of_students = len(instance.student.all())

        if not instance.group_lesson and no_of_students > 1:
            instance.group_lesson = True
            instance.save()
