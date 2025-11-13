from django.apps import AppConfig


class BootcampConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bootcamp'

    def ready(self):
        import bootcamp.signals