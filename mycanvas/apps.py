from django.apps import AppConfig


class MycanvasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mycanvas'

    def ready(self):
        import mycanvas.signals

