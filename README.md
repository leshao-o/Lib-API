# Lib-API
=====================

Lib-API - это REST API для управления библиотекой. Он позволяет добавлять, удалять и редактировать книги, авторов и пользователей.

## Установка и запуск

### Скачайте репозиторий

Скачайте этот репозиторий с помощью команды:

git clone https://github.com/leshao-o/lib-api.git

### Перейдите в папку проекта

```
cd lib-api
```

### Создайте файл .env
Создайте файл .env в корне проекта и добавьте в него следующие переменные:

```
DB_NAME=lib_db
DB_HOST=localhost
DB_PORT=5432
DB_USER=lib_user
DB_PASS=lib_pass
JWT_SECRET_KEY=secret_key
JWT_ALGORITHM=HS256
```


### Запустите Docker Compose
Запустите Docker Compose с помощью команды:

```
docker-compose up --build
```

## API Документация
Документация по API доступна по адресу: http://localhost:8001/docs