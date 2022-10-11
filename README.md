# Благотворительного фонда поддержки котиков QRKot
## Описание проекта.
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых,
на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Установка
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ggerasyanov/cat_charity_fund.git
```

```
cd ../cat_charity_fund/
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
alembic init --template async alembic # инициализация библиотеки alembic
alembic revision --autogenerate -m "your message" # создание файла миграции
alembic upgrade head # выполнение всех неприменённых миграций
```
Запустить проект:
```
uvicorn app.main:app --reload # аргумент reload опционален (перезапускает проект при изменении кода)
```

## Примеры
Отправив POST запрос на этот эндпоинт можно зарегестрировать аккаунт:
(все url относительные)
```
/auth/register/
```
Необходимые параметры:
```
{
  "email": "user@example.com",
  "password": "string",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```
Далее необходимо получить токен для работы с API. GET запросы регестрации не требуют.
Отправте POST Запрос с username и password на эндпоинт:
```
/auth/jwt/login/
```
В ответ вы получите токен:
```
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2ZDMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ.M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
  "token_type": "bearer"
}
```
Запрос к эндпоинту вернёт все проекты, которые были созданы:
```
/charity_project/
```
Вернёт результат:
```
[
  {
    "name": "string",
    "description": "string",
    "full_amount": 0,
    "id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "create_date": "2022-10-11T11:02:22.239Z",
    "close_date": "2022-10-11T11:02:22.239Z"
  }
]
```
Создать пожертвования можно по этому эндпоинту:
```
/donation/
```
Пример запроса:
```
{
  "full_amount": 0,
  "comment": "string"
}
```

Пример ответа:
```
{
  "full_amount": 0,
  "comment": "string",
  "id": 0,
  "create_date": "2022-10-11T11:03:37.546Z",
  "close_date": "2022-10-11T11:03:37.546Z"
}
```
Полный перечень возможностей вы можете найти в [документации](/docs/)

Проект написан на фреймворке FastAPI и работает асинхронно.
Backend автоматически при создании доната или проекта перечисляет деньги и если
нужная сумма набрана закрывает проект или донат.

## Стек использованных технологий
```
FastAPI, SQLAlchemy, Uvicorn, Alembic, Pydantic
```