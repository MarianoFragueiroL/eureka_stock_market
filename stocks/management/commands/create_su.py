from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crea un superusuario si no existe'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='test_interview').exists():
            User.objects.create_superuser('test_interview', '', 'test_123456')
            self.stdout.write(self.style.SUCCESS('Superusuario creado exitosamente'))
        else:
            self.stdout.write(self.style.SUCCESS('El superusuario ya existe'))