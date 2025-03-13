from django.apps import AppConfig


class PanicButtonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'panicbutton'

    def ready(self):
        import panicbutton.signals