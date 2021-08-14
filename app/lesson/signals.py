from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete, pre_save
from .models import Lesson, LessonDetail
from student.models import Student


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

    student: Student = instance.student
    new_lesson_duration = float(instance.duration)

    is_delete_signal = kwargs.get('is_delete_signal', False)

    if is_delete_signal:
        student.lesson_hours_sum -= new_lesson_duration
        update_student_pay_rate(student, student.lesson_hours_sum)

    elif instance.id is None:
        check_for_discount_grant(instance, student, new_lesson_duration)
    else:
        old_lesson_duration = LessonDetail.objects.get(id=instance.id).duration
        lesson_duration_change = new_lesson_duration - old_lesson_duration

        if lesson_duration_change == 0:
            return
        else:
            check_for_discount_grant(instance, student, lesson_duration_change)


# Purpose of this signal is to distinguish type of signal being sent -> is_delete_signal flag
@receiver(pre_delete, sender=LessonDetail)
def update_student_pay_rate_delete_signal(sender, instance, **kwargs):
    update_student_pay_rate_signal(sender, instance, is_delete_signal=True)


def check_for_discount_grant(
    lesson_detail: LessonDetail, student: Student, calculated_lesson_duration
):
    """As title says else save student model to update new hours sum"""
    hr_threshold_1 = Student._HOURS_REQUIRED_FOR_DISCOUNT.LEVEL_I
    hr_threshold_2 = Student._HOURS_REQUIRED_FOR_DISCOUNT.LEVEL_II

    old_student_hours_sum = student.lesson_hours_sum
    student.lesson_hours_sum += calculated_lesson_duration
    new_student_hours_sum = student.lesson_hours_sum

    if (hr_threshold_1 < new_student_hours_sum < hr_threshold_2) and (
        old_student_hours_sum <= hr_threshold_1
    ):
        """
        Check if student is eligible for discount LVL 1.
        """
        # update_student_pay_rate(student, new_student_hours_sum)
        set_lesson_price_and_pay_rate(
            lesson_detail,
            student,
            hr_threshold_1,
            new_student_hours_sum,
            old_student_hours_sum,
        )

    elif (new_student_hours_sum > hr_threshold_2) and (
        old_student_hours_sum <= hr_threshold_2
    ):
        """
        Check if student is eligible for discount LVL 2.
        """
        # update_student_pay_rate(student, new_student_hours_sum)
        set_lesson_price_and_pay_rate(
            lesson_detail,
            student,
            hr_threshold_2,
            new_student_hours_sum,
            old_student_hours_sum,
        )

    elif (
        new_student_hours_sum <= hr_threshold_1 and old_student_hours_sum > hr_threshold_1
    ) or (
        new_student_hours_sum <= hr_threshold_2 and old_student_hours_sum > hr_threshold_2
    ):
        """
        Condition if lesson was edited and duration shortened so that student
        is no longer eligible for discount so pay_rate and lesson price should be updated.
        """
        update_student_pay_rate(student, new_student_hours_sum)
        student.refresh_from_db(fields=['pay_rate_single', 'pay_rate_group'])

        if lesson_detail.lesson.group_lesson:
            lesson_detail.pay_rate = student.pay_rate_group
        else:
            lesson_detail.pay_rate = student.pay_rate_single

        lesson_detail.price = float(lesson_detail.duration) * int(lesson_detail.pay_rate)

    else:
        """Save new lesson_hours_sum value"""
        student.save()


# Helper function
def update_student_pay_rate(student_obj, hours_sum):

    if hours_sum <= Student._HOURS_REQUIRED_FOR_DISCOUNT.LEVEL_I:
        student_obj.pay_rate_single = Student._PAY_RATES_SINGLE.IKO_I
        student_obj.pay_rate_group = Student._PAY_RATES_GROUP.IKO_I

    elif (
        Student._HOURS_REQUIRED_FOR_DISCOUNT.LEVEL_I
        < hours_sum
        <= Student._HOURS_REQUIRED_FOR_DISCOUNT.LEVEL_II
    ):
        student_obj.pay_rate_single = Student._PAY_RATES_SINGLE.IKO_II
        student_obj.pay_rate_group = Student._PAY_RATES_GROUP.IKO_II

    elif hours_sum > Student._HOURS_REQUIRED_FOR_DISCOUNT.LEVEL_II:
        student_obj.pay_rate_single = Student._PAY_RATES_SINGLE.IKO_III
        student_obj.pay_rate_group = Student._PAY_RATES_GROUP.IKO_II

    else:
        raise AttributeError("Student pay_rate update fail")
    student_obj.save()


def set_lesson_price_and_pay_rate(
    lesson_detail: LessonDetail,
    student: Student,
    threshold,
    new_student_hours_sum,
    old_student_hours_sum,
):
    """
    Calculate lesson_detail price using two different pay_rates.
    This is happening when student reaches next discount level when completing one lesson.
    For example student had total 4 hours and after 2h lesson his total is 6 which grants him a discount.
    One fraction of lesson is calculated with different pay_rate than second fraction.
    """
    update_student_pay_rate(student, new_student_hours_sum)

    time_after_discount = new_student_hours_sum - threshold
    time_before_discount = float(lesson_detail.duration) - time_after_discount

    price_before_discount = float(time_before_discount) * int(lesson_detail.pay_rate)

    student.refresh_from_db(fields=['pay_rate_single', 'pay_rate_group'])

    if lesson_detail.lesson.group_lesson:
        lesson_detail.pay_rate = student.pay_rate_group
    else:
        lesson_detail.pay_rate = student.pay_rate_single

    price_after_discount = float(time_after_discount) * int(lesson_detail.pay_rate)
    lesson_detail.price = price_before_discount + price_after_discount
