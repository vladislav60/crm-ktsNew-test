# config.py

# Секретный ключ для Django
SECRET_KEY = "$$==_c9vm&-h6(h2x0@urr(ya1*ywwm!@t@1u=ccr=0tcc-r6x"

# Токен Telegram-бота
TELEGRAM_BOT_TOKEN = "7362467897:AAHrluc3JLzPq7XXOGZ5V--6zUPXx4GC8fI"

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crm-kts',
        'USER': 'crmktsuser',
        'PASSWORD': 'c7VL09DcUnXGKVysq0fV!$',
        'HOST': '192.168.1.60',
        'PORT': '5432',
    },
    'asu_ekc': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'asu_ekc',
        'USER': 'asu2',
        'PASSWORD': 'c7VL09DcUnXGKVysq0fV',
        'HOST': '192.168.1.60',
        'PORT': '5432',
    },
    'third_db': {
        'ENGINE': 'mssql',
        'NAME': 'GBASE',
        'USER': 'vlad_asukts',
        'PASSWORD': 'KtsPCN@2024!$_Lol',
        'HOST': '192.168.1.17',
        'PORT': '1433',

        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}