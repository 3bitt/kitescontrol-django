from django.apps import AppConfig


class InstructorConfig(AppConfig):
    name = 'instructor.instructor'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import instructor.instructor.signals

