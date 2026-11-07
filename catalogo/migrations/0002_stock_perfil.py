import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('catalogo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='pieza',
            name='stock',
            field=models.IntegerField(
                default=0,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('rut', models.CharField(max_length=12)),
                ('telefono', models.CharField(max_length=15)),
                (
                    'rol_institucional',
                    models.CharField(default='Cliente', max_length=50),
                ),
                (
                    'usuario',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]