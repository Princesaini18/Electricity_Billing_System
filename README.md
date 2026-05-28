# Smart Electricity Billing System

A professional BCA final semester Django project for electricity consumer management, bill generation, analytics dashboards, and PDF bill downloads.

## Tech Stack

- Python 3
- Django 6
- SQLite
- Tailwind CSS
- Alpine.js
- Lucide Icons
- Chart.js
- ReportLab

## Quick Setup

### 1. Backend setup

Recommended Python version: **3.12**

On Windows PowerShell:

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

If you already created a `venv` using Python 3.15, delete it and recreate it with Python 3.12:

```powershell
Remove-Item -Recurse -Force .\venv
py -3.12 -m venv venv
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### 2. Frontend setup (Tailwind build)

```bash
npm install
npm run build:css
```

For live CSS rebuild while editing templates:

```bash
npm run watch:css
```

### 3. Run project

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Demo Admin (Current Workspace)

```text
Username: admin
Password: use your local admin password
```

Create your own admin account with `python manage.py createsuperuser`.

---

## Main Features

- Admin authentication (login/logout)
- Consumer portal login (consumer number + meter number)
- Dashboard with analytics cards and charts
- Consumer CRUD management
- Electricity bill generation with slab logic
- Paid/Pending status tracking
- Bill history with filters and pagination
- Bill detail invoice view with print support
- PDF bill download using ReportLab
- Responsive Tailwind SaaS-style UI
- Dark/Light mode toggle

---

## Tariff Logic

| Units | Rate |
| --- | --- |
| 0-100 | Rs. 3/unit |
| 101-300 | Rs. 5/unit |
| Above 300 | Rs. 7/unit |

Additional charges:

- Fixed charge: Rs. 100
- Tax: 5%

---

## Project Guides

- Database guide: `docs/DATABASE_GUIDE.md`
- Frontend/Tailwind implementation guide: `docs/FRONTEND_UPGRADE_GUIDE.md`

## Login Routes

- Admin login: `http://127.0.0.1:8000/login/`
- Consumer login: `http://127.0.0.1:8000/consumer/login/`

---

## Useful Commands

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
npm run build:css
```
