from django.apps import AppConfig


class LessonConfig(AppConfig):
    name = 'lesson'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import lesson.signals
