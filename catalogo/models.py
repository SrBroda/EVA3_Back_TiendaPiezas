from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Entidad de Contexto
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Entidad Principal Gestionable
class Pieza(models.Model):
    ESTADO_CHOICES = [
        ('Disponible', 'Disponible'),
        ('Agotado', 'Agotado'),
    ]

    codigo = models.SlugField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.IntegerField(validators=[MinValueValidator(0)]) # Impide valores negativos
    stock = models.IntegerField(validators=[MinValueValidator(0)], default=0) # Valida que el stock nunca baje de cero
    imagen = models.ImageField(upload_to='piezas/', null=True, blank=True) # Soporte multimedia
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Disponible') # Opciones cerradas
    vigente = models.BooleanField(default=True) # Control de vigencia / baja lógica
    
    # Relación referencial
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, help_text="Ejemplo: 12.345.678-9")
    telefono = models.CharField(max_length=15)
    rol_institucional = models.CharField(max_length=50, default='Cliente') # Puede ser 'Staff' o 'Cliente'

    def __str__(self):
        return f"Perfil de {self.usuario.username}"