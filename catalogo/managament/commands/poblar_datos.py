from django.core.management.base import BaseCommand
from catalogo.models import Categoria, Pieza
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Puebla la base de datos con categorías, piezas de PC y usuarios de prueba'

    def handle(self, *args, **kwargs):
        # Crear usuarios de prueba
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        if not User.objects.filter(username='vendedor').exists():
            User.objects.create_user('vendedor', 'vende@tienda.com', 'vende123')

        # Crear 4 categorías
        cat_nombres = ['Procesadores', 'Tarjetas Gráficas', 'Placas Madre', 'Memorias RAM']
        categorias = {}
        for nombre in cat_nombres:
            cat, created = Categoria.objects.get_or_create(nombre=nombre)
            categorias[nombre] = cat

        # Crear 8 piezas
        piezas = [
            {'codigo': 'CPU-01', 'nombre': 'AMD Ryzen 5 5600X', 'precio': 150000, 'cat': 'Procesadores'},
            {'codigo': 'CPU-02', 'nombre': 'Intel Core i5-12400F', 'precio': 140000, 'cat': 'Procesadores'},
            {'codigo': 'GPU-01', 'nombre': 'NVIDIA RTX 3060 12GB', 'precio': 300000, 'cat': 'Tarjetas Gráficas'},
            {'codigo': 'GPU-02', 'nombre': 'AMD Radeon RX 6600', 'precio': 220000, 'cat': 'Tarjetas Gráficas'},
            {'codigo': 'MB-01', 'nombre': 'ASUS B550M-A Wi-Fi', 'precio': 110000, 'cat': 'Placas Madre'},
            {'codigo': 'MB-02', 'nombre': 'MSI B660M Mortar', 'precio': 135000, 'cat': 'Placas Madre'},
            {'codigo': 'RAM-01', 'nombre': 'Corsair Vengeance 16GB (2x8) 3200MHz', 'precio': 450000, 'cat': 'Memorias RAM'},
            {'codigo': 'RAM-02', 'nombre': 'Kingston Fury 16GB (1x16) 3600MHz', 'precio': 48000, 'cat': 'Memorias RAM'},
        ]

        for p in piezas:
            Pieza.objects.get_or_create(
                codigo=p['codigo'],
                defaults={
                    'nombre': p['nombre'],
                    'descripcion': f"Excelente componente de la categoría {p['cat']}.",
                    'precio': p['precio'],
                    'categoria': categorias[p['cat']]
                }
            )
        
        self.stdout.write(self.style.SUCCESS('¡Base de datos poblada exitosamente!'))