# Database Guide

This project uses **SQLite** as the backend database.

SQLite is different from MySQL. It does not run as a separate server and it will not appear in phpMyAdmin or a hosting database panel. The complete database is stored in one local file:

```text
db.sqlite3
```

Project database file path:

```text
/var/www/html/electricitybillmanagementsystem/db.sqlite3
```

## Main Tables

The important project tables are:

```text
billing_consumer
billing_bill
billing_payment
auth_user
```

Other tables are created automatically by Django for login, sessions, permissions, and admin panel.

## Method 1: View Database Using Django Admin

This is the easiest method for college demo and viva.

Start the server:

```bash
source venv/bin/activate
python manage.py runserver
```

Open this URL:

```text
http://127.0.0.1:8000/admin/
```

Login with your admin account:

```text
Username: your_admin_username
Password: your_admin_password
```

Inside Django Admin you can view:

- Consumers
- Bills
- Payments
- Users

## Method 2: View Database Using DB Browser for SQLite

Install **DB Browser for SQLite**.

Then open this file:

```text
db.sqlite3
```

After opening the file:

1. Go to the **Browse Data** tab.
2. Select a table like `billing_consumer`.
3. View table entries.
4. Select `billing_bill` to view bill records.

This is useful if you want to show the actual database tables during presentation.

## Method 3: View Database Using VS Code

Install a SQLite extension in VS Code, for example:

```text
SQLite Viewer
```

Then open:

```text
db.sqlite3
```

You can inspect all tables directly inside VS Code.

## Method 4: View Tables From Terminal

Activate the virtual environment:

```bash
source venv/bin/activate
```

Show all database tables:

```bash
python manage.py shell -c "from django.db import connection; print(connection.introspection.table_names())"
```

Show all consumers:

```bash
python manage.py shell -c "from billing.models import Consumer; print(list(Consumer.objects.values()))"
```

Show all bills:

```bash
python manage.py shell -c "from billing.models import Bill; print(list(Bill.objects.values()))"
```

Show all users:

```bash
python manage.py shell -c "from django.contrib.auth.models import User; print(list(User.objects.values('username', 'is_staff', 'is_superuser')))"
```

## Why Database Is Not Visible In phpMyAdmin

phpMyAdmin is only for MySQL or MariaDB databases.

This project uses SQLite, so there is no MySQL database name, username, host, or table list in phpMyAdmin.

SQLite database is simply this file:

```text
db.sqlite3
```

## If Tables Are Missing

Run migrations again:

```bash
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

Then check tables:

```bash
python manage.py shell -c "from django.db import connection; print(connection.introspection.table_names())"
```

## If Admin Login Does Not Work

Create a new admin account:

```bash
source venv/bin/activate
python manage.py createsuperuser
```

Then open:

```text
http://127.0.0.1:8000/admin/
```

## Viva Explanation

You can explain it like this:

> This project uses SQLite as the database. SQLite stores all data in a local `db.sqlite3` file. Django ORM creates tables using migrations. Consumer details are stored in `billing_consumer`, bill records are stored in `billing_bill`, payment details are stored in `billing_payment`, and login users are stored in Django's `auth_user` table. Since SQLite is file-based, it is not shown in phpMyAdmin.
