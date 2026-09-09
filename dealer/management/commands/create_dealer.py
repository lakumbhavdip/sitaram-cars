import getpass
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Interactively create a dealer user account for managing Sitaram Cars.'

    def handle(self, *args, **options):
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

        user = User.objects.create_superuser(username=username, email='', password=password)
        self.stdout.write(self.style.SUCCESS(f'\nDealer user "{username}" successfully created!'))
