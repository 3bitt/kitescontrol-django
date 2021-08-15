from django.apps import AppConfig


class InstructorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crew.instructor'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import crew.instructor.signals
