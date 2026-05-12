# Deploy Sibane ECD Academy on Render

This project is ready to deploy as a Django web app on Render with an online PostgreSQL database.

## Important free-plan note

Render currently supports free web services and free Postgres databases, but free services have limits:

- Free web services sleep after about 15 minutes without traffic and can take about a minute to wake up.
- Free web services have an ephemeral filesystem, so do not use SQLite or uploaded local files for permanent data.
- Free Render Postgres is limited to 1 GB and currently expires after 30 days.
- Free Render Postgres has no backups.

For real school operations, use the free plan only for testing. Upgrade the database before the 30-day expiry if you want to keep live data.

## 1. Put the project on GitHub

If this folder is not already a Git repository, run:

```bash
git init
git add .
git commit -m "Prepare Sibane ECD Academy for Render"
git branch -M main
```

Create a new GitHub repository, then connect and push:

```bash
git remote add origin https://github.com/YOUR_USERNAME/sibane-preschool.git
git push -u origin main
```

## 2. Create the Render Blueprint

1. Log in to Render.
2. Click **New**.
3. Choose **Blueprint**.
4. Connect the GitHub repository.
5. Render will read `render.yaml` and create:
   - a free Python web service named `sibane-preschool`
   - a free PostgreSQL database named `sibane-db`
6. When Render asks for `DJANGO_ADMIN_PASSWORD`, enter a strong password you will use for the first admin login.
7. Click **Apply** or **Deploy**.

## 3. What Render runs

The `build.sh` script does the deployment setup:

```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py ensure_admin
```

The web service starts with:

```bash
gunicorn sibane_preschool.wsgi --workers 2 --timeout 120 --log-file -
```

## 4. Open the app

After deploy finishes, open the Render service URL:

```text
https://sibane-preschool.onrender.com
```

Log in with:

- Username: `admin`
- Password: the `DJANGO_ADMIN_PASSWORD` you entered during Blueprint setup

## 5. Health check

Render checks:

```text
/health/
```

If it returns `200`, both the web service and database connection are working.
