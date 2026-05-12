"""
Management command: ensure_admin
Creates the initial superuser from environment variables if it doesn't exist yet.
Called in build.sh so the first deploy has a working admin account.

Usage:
  python manage.py ensure_admin

Environment variables (set in Render dashboard):
  DJANGO_ADMIN_USERNAME  (default: admin)
  DJANGO_ADMIN_EMAIL     (default: admin@sibane.zw)
  DJANGO_ADMIN_PASSWORD  (default: SibaneAdmin2024!)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Create superuser from env vars if it does not exist'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_ADMIN_USERNAME', 'admin')
        email    = os.environ.get('DJANGO_ADMIN_EMAIL',    'admin@sibane.zw')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD', 'SibaneAdmin2024!')

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Admin user "{username}" already exists — skipping.')
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(
                f'Superuser "{username}" created. '
                f'CHANGE THE PASSWORD immediately via /admin/ or the shell.'
            ))
