from django.apps import AppConfig


class DriversAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drivers_admin'

    def ready(self):
        import drivers_admin.signals
