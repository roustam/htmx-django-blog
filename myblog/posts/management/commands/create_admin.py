from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials (adm / BlgScrtPassword1234#)'

    def handle(self, *args, **options):
        username = 'adm'
        password = 'BlgScrtPassword1234#'
        email = 'xyz@xyz.by'  # You can change this if needed

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password, email=email)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists'))