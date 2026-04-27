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
authonpy/
│
├── main.py             
├── db.py             
├── models.py              
├── schemas.py            
├── auth.py                        
│
│
├── docker-compose.yml   # Поднимает API + PostgreSQL
├── Dockerfile           # Сборка backend контейнера
│
├── requirements.txt     # Python зависимости
├── .env                 # Переменные окружения
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
  "full_name": "string",
  "password": "string",
  "ID_employer": 0
}
```

---

### Логин
```
POST /register/worker
```

```json
{
  "full_name": "string",
  "password": "string",
  "ID_store": 0,
  "ID_administrator": 0
}
```

---

### Получить пользователя
```
GET /auth/me
```

```json
{
  "full_name": "string",
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
```

---

## 📌 Swagger

```
http://localhost:8000/docs
```

---

## 🧠 Архитектура

Client → API → Routes → Services → Models → PostgreSQL

---

## ⭐ Автор

masquadd