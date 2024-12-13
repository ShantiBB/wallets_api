# Описание проекта
Это приложение представляет собой API для работы с кошельками. Оно предоставляет возможность выполнять операции пополнения (DEPOSIT)
и снятия средств (WITHDRAW) с указанного кошелька, а также позволяет получать текущий баланс кошелька.

## Проект использует стек технологий:

- Django REST Framework (DRF) для реализации API
- Djoser для работы с аутентификацией
- Celery для обработки асинхронных задач
- Flower для мониторинга задач Celery
- Redis для кеширования
- RabbitMQ в качестве брокера сообщений
- PostgreSQL для хранения данных
- pytest для тестирования
- Locus для нагрузки
- Docker для контейнеризации
- Pydantic Settings для конфигурации

## Установка и настройка

### Шаг 1: Клонирование репозитория
Для начала нужно клонировать репозиторий с GitHub:
```bash
git clone git@github.com:ShantiBB/wallets_api.git
cd wallets_api
```

### Шаг 2: Создание и активация виртуального окружения
Создайте виртуальное окружение и активируйте его:

```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/macOS
source venv\Scripts\activate  # Для Windows
```

### Шаг 3: Установка зависимостей
Установите все зависимости из requirements.txt:
```bash
pip install poetry
poetry install
```

### Шаг 4: Запуск контейнеров Docker
Проект упакован в Docker-контейнеры.  

Для удобства запуска используйте команду:
```bash
docker-compose up --build
```
Это создаст все необходимые сервисы, такие как Django, PostgreSQL, Celery, Flower, Redis и RabbitMQ.

### Шаг 5: Миграция базы данных
После того как контейнеры запустились, выполните миграцию базы данных:
```bash
docker-compose exec wallet python manage.py migrate
```
### Шаг 6: Создание суперпользователя
Создайте суперпользователя для доступа к Django Admin:

```bash
docker-compose exec wallet python manage.py createsuperuser
```

## API
1. Создание кошелька  
POST /api/v1/wallets/

2. Обновление кошелька  
PUT /api/v1/wallets/<WALLET_UUID>/

3. Операции с кошельком  
POST /api/v1/wallets/<WALLET_UUID>/operation

4. Получение баланса кошелька  
GET /api/v1/wallets/<WALLET_UUID>

5. Регистрация пользователя  
POST /api/v1/auth/users/

7. Создание пользователя  
POST /api/v1//users/

6. Получение токена (Login)  
POST /api/v1/auth//token/login/

## Нагрузочное тестирование с Locus
Для выполнения нагрузочного тестирования с использованием Locus, выполните команду:

```bash
locust -f tests/locustfile.py --users 1000 --spawn-rate 50 --run-time 60 --host http://127.0.0.1:8000
```
В результате оптимизации запросов к бд удалось добиться 1000 RPS к одному кошельку без ошибок
