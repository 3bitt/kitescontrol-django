from django.apps import AppConfig


class LessonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lesson'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import lesson.signals
