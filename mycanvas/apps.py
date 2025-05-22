from django.apps import AppConfig


class MycanvasConfig(AppConfig):
    name = 'mycanvas'

    def ready(self):
        from . import signals 
