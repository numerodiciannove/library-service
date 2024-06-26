# Library Management System

This is a Django-based Library Management System (LMS) that allows users to manage books borrowing, user authentication, telegram notifications and payments. It provides functionalities for CRUD operations on books, users, and borrowings, along with integration with Stripe for handling payments.

## Technologies used:
-  Django
-  Django REST Framework
-  Redis
-  Docker
-  Celery
-  Swagger
-  Telegram API
-  Stripe


## Features:
- > JWT authenticated: Users can register, login, and manage their accounts.
- > Books Service: Allows CRUD operations on books. Only admin users can create, update, or delete books. 
- > Users Service: Provides endpoints for managing user accounts.
- > Borrowings Service: Manages the borrowing of books by users. Includes functionalities for creating borrowings, listing borrowings, returning books, and sending telegram notifications for overdue borrowings.
- > Payments Service: Integrates with Stripe for handling payments associated with borrowings.
  
## Installation:
```shell
git clone https://github.com/numerodiciannove/library-service

cd library-service

python -m venv venv 
source venv/bin/activate 
pip install -r requirements.txt 

python manage.py makemigrations
python manage.py migrate
python manage-py runserver
```
Also don't forget copy and change [.env.sample](.env.sample) before starting your server.


## Run Celery & Redis:
If you want to use "every day telegram notification" for overdue clients borrowings, use this:
```shell
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest

celery -A library_service worker -l INFO -P solo
celery -A library_service beat -l INFO
```

## Swagger documentation:
Use this endpoint to view the documentation
```shell
{your_host}/api/doc/swagger/
```
## Library API:
### Books:

- GET /api/v1/books/
- POST /api/v1/books/
- GET /api/v1/books/{id}/
- PUT /api/v1/books/{id}/
- PATCH /api/v1/books/{id}/
- DELETE /api/v1/books/{id}/

### Borrowings:

- GET /api/v1/borrowings/
- POST /api/v1/borrowings/
- GET /api/v1/borrowings/{id}/
- DELETE /api/v1/borrowings/{id}/
- POST /api/v1/borrowings/{id}/return/

### Payments:

- GET /api/v1/payments/
- GET /api/v1/payments/{id}/

### Users:

- POST /api/v1/users/
- GET /api/v1/users/me/
- PUT /api/v1/users/me/
- POST /api/v1/users/token/
- POST /api/v1/users/token/refresh/

## Helpful:
For testing you can use fixture to create books.
```shell
python manage.py loaddata 1_books_db_fixture
```

## For collaboration:
Use this board to track project if you want to collaborate.

```shell
https://trello.com/b/SZDloEaE/drf-library
```