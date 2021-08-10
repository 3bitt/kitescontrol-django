import random
from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from account.models import User
from crew.instructor.models import Instructor
import datetime
from lesson.models import Lesson, LessonDetail

from student.models import Student

IKO_LEVELS = [
    'Asystent',
    'Instruktor 1',
    'Instruktor 2',
    'Insturktor 3'
]

WETSUIT_SIZES = ['XS','S','M','L','XL','XXL','S-128','M-140','L-146','XL-152']
HARNESS_SIZES = ['XS','S','M','L','XL','XXL']
IKO_LEVELS_STUDENT = ['1A',
'1B','1C','1D','1E','2F','2G','2H','2I',
'3J','3K','3L','3M','3N','4O','4P','4Q',
'4R','4S','4T','4U','4V','4W','4X','4Y' ]

class Provider(faker.providers.BaseProvider):
    def iko_level(self):
        return self.random_element(IKO_LEVELS)
    def wetsuit_size(self):
        return self.random_element(WETSUIT_SIZES)
    def harness_size(self):
        return self.random_element(HARNESS_SIZES)
    def iko_level_student(self):
        return self.random_element(IKO_LEVELS_STUDENT)
    def student_iko_id(self):
        return self.random_element(elements=(None, random.randint(10000, 90000)))

    def lesson_start_hours_unique(self):
        return self.r

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # self.create_managers(3)
        # self.create_clerks(3)
        self.create_instructors(10) #CHANGE userType in instructor.models.save() to 'INSTRUCTOR'
        # self.create_students(100)
        # self.create_lessons()
        pass

    def create_managers(self, count):
        faker = Faker(['pl_PL'])
        faker.add_provider(Provider)
        for i in range(count):
            email = faker.unique.email()
            name = faker.first_name()
            surname = faker.last_name()

            User.objects.create_user(
                email=email, name=name, surname=surname, password='Password@1', type='MANAGER')

    def create_clerks(self, count):
        faker = Faker(['pl_PL'])
        faker.add_provider(Provider)
        for i in range(count):
            email = faker.unique.email()
            name = faker.first_name()
            surname = faker.last_name()

            User.objects.create_user(
                email=email, name=name, surname=surname, password='Password@1', type='CLERK')

    def create_instructors(self, count):
        faker = Faker(['pl_PL'])
        faker.add_provider(Provider)
        for i in range(count):
            email = faker.unique.email()
            name = faker.first_name()
            surname = faker.last_name()

            # user = User.objects.create_user(email=email,name=name,surname=surname,password='Password@1',type='INSTRUCTOR')

            birth_date = faker.date_between(start_date='-40y', end_date='-20y')
            mobile_number = random.randint(100000000, 999999999)
            weight = random.randint(50, 100)
            available_from = faker.date_between_dates(
                date_start=datetime.date(2021, 2, 1), date_end=datetime.date(2021, 4, 25))
            available_to = faker.date_between_dates(
                date_start=datetime.date(2021, 9, 1), date_end=datetime.date(2021, 12, 25))
            iko_level = faker.iko_level()
            bool_random = bool(random.getrandbits(1))
            pay_rate_single=random.randint(40,80)
            pay_rate_group = random.randint(50, 90)
            daily_hour_limit = random.randint(4, 18)

            Instructor.objects.create(
                name=name,
                surname=surname,
                birth_date= birth_date,
                mobile_number=mobile_number,
                email_address=email,
                weight=weight,
                available_from=available_from,
                available_to=available_to,
                iko_id=mobile_number,
                iko_level=iko_level,
                driving_licence=bool_random,
                pay_rate_single=pay_rate_single,
                pay_rate_group=pay_rate_group,
                english_lessons=bool_random,
                kids_lessons=bool_random,
                group_lessons=bool_random,
                daily_hour_limit=daily_hour_limit,
                active=True,
                # user=user
            )

    def create_students(self, count):
        faker = Faker(['pl_PL'])
        faker.add_provider(Provider)
        for i in range(count):
            email = faker.email()
            name = faker.first_name()
            surname = faker.last_name()

            birth_date = faker.date_between(start_date='-40y', end_date='-20y')
            mobile_number = random.randint(100000000, 999999999)
            weight = random.randint(50, 100)
            arrival_date = faker.date_between_dates(
                date_start=datetime.date(2021, 5, 1), date_end=datetime.date(2021, 9, 10))
            leave_date = faker.date_between_dates(
                date_start=arrival_date, date_end=datetime.date(2021, 9, 25))
            stay_location = faker.city()
            comment = faker.sentence(nb_words=5)
            bool_random = bool(random.getrandbits(1))
            pay_rate_single = random.randint(100, 150)
            pay_rate_group = random.randint(90, 130)

            student = Student.objects.create(
                name=name,
                surname=surname,
                birth_date=birth_date,
                mobile_number=mobile_number,
                email_address=email,
                weight=weight,
                arrival_date=arrival_date,
                leave_date=leave_date,
                stay_location=stay_location,
                own_car=bool_random,
                kite_elsewhere=bool_random,
                wetsuit_size=faker.wetsuit_size(),
                harness_size=faker.harness_size(),
                iko_id=faker.student_iko_id(),
                iko_level=faker.iko_level_student(),
                comment=comment,
                pay_rate_single=pay_rate_single,
                pay_rate_group=pay_rate_group
            )

    def create_lessons(self):
        faker = Faker(['pl_PL'])
        faker.add_provider(Provider)

        lesson_start_hours = [7, 9, 11, 13, 15, 17, 19]

        instructor_ids = Instructor.objects.all().values_list('id')
        students_list = Student.objects.all().values_list('id', flat=True)

        # range(5, 10)
        # range( 1,30)

        for month in range(5,6):
            for day in range(1,2):
                for instructor in instructor_ids:
                    for lesson_per_day in range(random.randint(1,7)):
                        lesson_students_list = random.choice([
                            [random.choice(students_list)],
                            [random.choice(students_list)],
                            [random.choice(students_list)],
                            [random.choice(students_list)],
                            random.choices(students_list, k=2)
                            ])

                        _unique_start_hour = random.choice(lesson_start_hours)
                        lesson_start_hours.pop(lesson_start_hours.index(_unique_start_hour))

                        start_date = datetime.date(2021,month,day)
                        start_time = datetime.time(_unique_start_hour,0,0,0)
                        group_lesson = bool((len(lesson_students_list) > 1))
                        duration = random.choice([1,1.5,2,2,2,2,2])

                        kite_brand = random.choice(['7A', '12B', '12A', '7B', '9C', '14B', '7C', '9A', '5A', '10B', '14C', '10C'])
                        board = random.choice(['Kc.7', 'Kc.12', 'Kc.8', 'Kc.5', 'Kc.2', 'Kc.4', 'Kc.10', 'Kc.11', 'Kc.2', 'Kc.1', '14C', '10C'])
                        comment = faker.sentence(nb_words=1)
                        confirmed = random.choice(
                            [True, True, True, True,False])
                        in_progress = random.choice([bool(confirmed), bool(confirmed), bool(confirmed),bool(confirmed and False )])

                        completed = random.choice(
                            [bool(not in_progress and confirmed), False, False, False])
                        paid = random.choice(
                            [bool(completed), False, False, False, False])

                        lesson = Lesson.objects.create(
                            start_date=start_date,
                            start_time=start_time,
                            group_lesson=group_lesson,
                            duration=duration,
                            paid=paid,
                            kite_brand=kite_brand,
                            board=board,
                            comment=comment,
                            in_progress=in_progress,
                            confirmed=confirmed,
                            completed=completed
                        )

                        lesson.student.set(lesson_students_list)
                        lesson.instructor.set(list(instructor))
                        lesson.save()

                        # print(lesson_students_list)

                        if (lesson.completed):
                            is_group_lesson = lesson.group_lesson

                            for student in lesson.student.all():

                                lesson_detail = LessonDetail.objects.create(
                                    lesson=lesson,
                                    student=student,
                                    duration=lesson.duration,
                                    pay_rate = student.pay_rate_group if is_group_lesson else student.pay_rate_single,
                                    price=duration * int(student.pay_rate_group if is_group_lesson else student.pay_rate_single),
                                    iko_level_achieved=faker.iko_level_student()
                                )

                    lesson_start_hours = [7, 9, 11, 13, 15, 17, 19]



