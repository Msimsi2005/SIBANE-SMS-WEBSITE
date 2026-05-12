# Sibane ECD Academy — Pre-School Management System

A complete web-based management system for Sibane Pre-School, built with Django 4.2 and Bootstrap 5.

## Features

| Module | Description |
|---|---|
| 📚 Students | Add/edit/deactivate students, view profiles, track fees |
| 👩‍🏫 Staff | Manage teachers, general hand, supervisors, cooks, drivers |
| ✅ Attendance | Daily class-level marking with bulk entry + history |
| 💰 Payments | Record school fees, levies, bus fare — with history |
| 🍽 Meals | Track breakfast, lunch, snack counts per class |
| 🧾 Expenses | Categorised expense tracking with monthly filter |
| 📦 Inventory | Stock management with in/out/adjustment transactions |
| 📖 Library | Books catalogue + borrow/return tracking per student |
| 📅 Timetable | Weekly schedule grid by class |
| 👁 Supervisor Visits | Record visit notes per class (Week 2 & 4) |
| 🛍 Contributions | Uniform sales, grocery submissions, relish contributions |

---

## 🖥 Run Locally

### Prerequisites
- Python 3.11+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/sibane-preschool.git
cd sibane-preschool
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
copy .env.example .env        # Windows
cp .env.example .env          # Mac/Linux
```

Edit `.env`:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

> Generate a secret key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create admin user

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open: **http://127.0.0.1:8000/**

Login with the superuser credentials you just created.

---

## 🚀 Deploy on Render

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit — Sibane ECD Academy"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/sibane-preschool.git
git push -u origin main
```

### Step 2 — Create a PostgreSQL database on Render

1. Log in to [render.com](https://render.com)
2. Click **New → PostgreSQL**
3. Give it a name: `sibane-db`
4. Click **Create Database**
5. Copy the **Internal Database URL** (starts with `postgresql://...`)

### Step 3 — Create a Web Service on Render

1. Click **New → Web Service**
2. Connect your GitHub repository
3. Fill in:
   - **Name**: `sibane-preschool`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn sibane_preschool.wsgi --log-file -`

### Step 4 — Add Environment Variables on Render

In your Web Service → **Environment** tab, add:

| Key | Value |
|---|---|
| `SECRET_KEY` | (generate a new one) |
| `DEBUG` | `False` |
| `DATABASE_URL` | (paste the PostgreSQL internal URL) |
| `ALLOWED_HOSTS` | `your-service-name.onrender.com` |

### Step 5 — Deploy

Click **Deploy**. Render will:
- Install dependencies
- Run `python manage.py migrate` (via the `release` command in Procfile)
- Start the web server

### Step 6 — Create superuser on Render

In your Web Service → **Shell** tab:
```bash
python manage.py createsuperuser
```

---

## 📁 Project Structure

```
sibane_preschool/
├── core/
│   ├── models.py          ← All database models
│   ├── views.py           ← All views
│   ├── forms.py           ← Bootstrap-styled forms
│   ├── urls.py            ← URL routing
│   ├── admin.py           ← Django admin configuration
│   └── templatetags/
│       └── core_filters.py ← Custom template filters
├── templates/
│   ├── base.html          ← Sidebar layout
│   ├── dashboard.html     ← Main dashboard
│   ├── students/
│   ├── staff/
│   ├── attendance/
│   ├── payments/
│   ├── meals/
│   ├── expenses/
│   ├── inventory/
│   ├── library/
│   ├── timetable/
│   ├── supervisor/
│   └── contributions/
├── requirements.txt
├── Procfile               ← Render start command
├── runtime.txt            ← Python version
└── .env.example           ← Environment variable template
```

---

## 🔐 Default Login (development only)

| Username | Password |
|---|---|
| `admin` | `sibane2024` |

> ⚠️ **Change this password immediately in production.**

---

## 🛠 Tech Stack

- **Backend**: Django 4.2
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **Hosting**: Render
- **Static files**: WhiteNoise
