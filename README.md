# 📦 AuthonPy

Backend-сервис на Python с REST API, системой авторизации пользователей и PostgreSQL базой данных, развёрнутой в Docker-контейнере.

Проект предназначен для регистрации, аутентификации и управления пользователями через API.

---

## 🚀 Возможности

- Регистрация пользователей
- Авторизация (login/logout)
- Хранение пользователей в PostgreSQL
- Работа через REST API
- Docker-развёртывание
- SQL-интерфейс для анализа базы

---

## 🧱 Технологии

- Python
- PostgreSQL
- Docker & Docker Compose
- SQL (psql)
- JWT / Auth система

---

## 📁 Структура проекта

```
auth_service/
│
├── main.py                  # Точка входа FastAPI + seed_default_employer
│
├── api/
│   └── api.py               # Роутер: /login, /me, /register/administrator, /register/worker
│
├── db/
│   └── db.py                # Подключение к БД, engine, SessionLocal, get_db
│
├── models/
│   └── models.py            # SQLAlchemy модели (Employer, Administrator, Worker, Store)
│
├── schemas/
│   └── schemas.py           # Pydantic схемы
│
├── jwt/
│   └── jwt.py               # Хэширование паролей, создание/проверка JWT, get_current_user
│
├── docker-compose.yml       # Поднимает API (fastapi_app) + PostgreSQL (postgres_db)
├── Dockerfile               # Сборка backend контейнера
│
├── adminmetrics.sql         # Файл с таблитаци базы данных на SQL
│
├── requirements.txt         # Python зависимости
├── .env                     # Переменные окружения (SECRET_KEY, DB_USER, DB_PASS...)
├── .gitignore
└── README.md
```

---

## 🔐 API

### Регистрация
```
POST /register/administrator
```

```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "string",
  "ID_employer": 0,
  "ip_address": "string"
}
```

---

```
POST /register/worker
```

```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "string",
  "ID_store": 0,
  "ID_administrator": 0,
  "ip_address": "string"
}
```

---

### Логин

```
POST /login
```

```
{
  "username": "string",
  "password": "string",
  "ip_address": "string"
}
```

---

### Получить пользователя
```
GET /auth/me
```

```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "string",
  "additional_info": {}
}
```
---

## 🐳 Запуск проекта

### Клонирование
```bash
git clone https://github.com/moiseyevanton/authonpy.git
cd authonpy
```

---

### Запуск Docker
```bash
docker-compose up --build
```

---

## 🛑 Остановка

```bash
docker-compose down
```

Полная очистка:
```bash
docker-compose down -v
```

---

## 🐘 Работа с PostgreSQL

Подключение:
```bash
docker exec -it postgres_db psql -U postgres
```


Подключения из контейнера:
```bash
psql -U app_user -d app_db
```

---

### SQL команды

```sql
-- Показать таблицы
\dt

-- Структура users
\d users

-- Все пользователи
SELECT * FROM users;

-- Кол-во пользователей
SELECT COUNT(*) FROM users;

-- Последние регистрации
SELECT * FROM users ORDER BY created_at DESC LIMIT 10;

-- Выход
\q
```

---

## ⚙️ .env пример

```
POSTGRES_DB=app_db
POSTGRES_USER=app_user
POSTGRES_PASSWORD=supersecret

DB_HOST=db
DB_PORT=5432

SECRET_KEY=super_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24
```

---

## 📌 Swagger

```
http://localhost:8000/docs
```

---

## 🧠 Архитектура

Client → FastAPI → Router → Pydantic (валидация) / JWT (токены) → SQLAlchemy (модели) → PostgreSQL
---

## ⭐ Автор

masquadd