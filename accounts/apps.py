from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = 'Управление пользователем'

    def ready(self):
        import accounts.signals  # Импортируйте сигналы
