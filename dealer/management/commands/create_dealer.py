import os
import getpass
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a dealer user account for managing Sitaram Cars (supports interactive, args, or env vars).'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Dealer username')
        parser.add_argument('--password', type=str, help='Dealer password')

    def handle(self, *args, **options):
        # 1. Check CLI options or environment variables first
        username = (options.get('username') or os.environ.get('DEALER_USERNAME') or '').strip()
        password = (options.get('password') or os.environ.get('DEALER_PASSWORD') or '').strip()

        if username and password:
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'Dealer user "{username}" already exists.'))
                return
            User.objects.create_superuser(username=username, email='', password=password)
            self.stdout.write(self.style.SUCCESS(f'Dealer user "{username}" successfully created!'))
            return

        # 2. Interactive CLI fallback
        self.stdout.write(self.style.SUCCESS('=== Create Dealer Account ==='))
        
        while True:
            username = input('Username: ').strip()
            if not username:
                self.stdout.write(self.style.ERROR('Username cannot be empty.'))
                continue
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.ERROR(f'User "{username}" already exists.'))
                continue
            break

        while True:
            password = getpass.getpass('Password: ')
            if not password:
                self.stdout.write(self.style.ERROR('Password cannot be empty.'))
                continue
            password_confirm = getpass.getpass('Password confirmation: ')
            if password != password_confirm:
                self.stdout.write(self.style.ERROR('Passwords do not match. Please try again.'))
                continue
            break

        User.objects.create_superuser(username=username, email='', password=password)
        self.stdout.write(self.style.SUCCESS(f'\nDealer user "{username}" successfully created!'))
