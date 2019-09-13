> Представление общей структуры проекта

```bash
myproject
├── settings
│   ├── __init__.py
│   ├── settings.py    # основные настройки
│   ├── urls.py
│   └── wsgi.py
├── app
│   ├── walletapp
│       ├── migrations
|           └── __init__.py
│       ├── __init__.py
│       ├── admin.py            # Подключение orm моделей в django admin
│       ├── models.py           # orm модели
│       ├── serializers.py      # сериализация orm моделей
│       ├── tests.py            # unittest
│       ├── urls.py             # 
│       ├── views.py            # 
|       └── viewsets.py         # 
└──manage.py
```
```bash
Для запуска необходимо сделать и применить миграции
python manage.py makemigrations
python manage.py migrate
Для запуска dev сервера
python manage.py runservera
Настройки подключения к postgresql базе:
    'NAME': 'wallet'
    'USER': 'wallet'
    'PASSWORD': 'wallet'
    'HOST': '127.0.0.1'
    'PORT': '5432'
```