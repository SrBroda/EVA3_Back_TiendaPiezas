import os

from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandError, call_command
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = 'Puebla el catálogo y crea cuentas locales de prueba de forma segura.'

    def handle(self, *args, **options):
        call_command('cargar_catalogo_imagenes', verbosity=0)
        self._crear_cuenta_prueba(
            username='admin',
            email='admin@hardware-store.local',
            password_variable='SEED_ADMIN_PASSWORD',
            administrador=True,
        )
        self._crear_cuenta_prueba(
            username='vendedor',
            email='vendedor@hardware-store.local',
            password_variable='SEED_USER_PASSWORD',
            administrador=False,
        )

    def _crear_cuenta_prueba(
        self,
        *,
        username,
        email,
        password_variable,
        administrador,
    ):
        usuario = User.objects.filter(username=username).first()
        if usuario:
            if administrador and not usuario.is_superuser:
                raise CommandError(
                    'El usuario admin ya existe, pero no es superusuario. '
                    'Corrígelo manualmente antes de volver a poblar.'
                )
            self.stdout.write(f'La cuenta {username} ya existe; no se modificó.')
            return

        password = os.getenv(password_variable) or get_random_string(24)
        if administrador:
            usuario = User.objects.create_superuser(username, email, password)
        else:
            usuario = User.objects.create_user(username, email, password)

        self.stdout.write(self.style.SUCCESS(f'Cuenta de prueba: {username}'))
        self.stdout.write(f'Contraseña generada: {password}')