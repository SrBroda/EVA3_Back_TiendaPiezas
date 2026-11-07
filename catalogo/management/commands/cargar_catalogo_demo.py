from django.core.management.base import BaseCommand

from catalogo.models import Categoria, Pieza


PRODUCTOS = [
    {
        'categoria': 'Procesadores',
        'codigo': 'amd-ryzen-5-5600',
        'nombre': 'AMD Ryzen 5 5600',
        'descripcion': 'Procesador de 6 nucleos y 12 hilos para gaming y productividad.',
        'precio': 119990,
        'stock': 8,
    },
    {
        'categoria': 'Procesadores',
        'codigo': 'intel-core-i5-12400f',
        'nombre': 'Intel Core i5-12400F',
        'descripcion': 'Procesador de 12a generacion con 6 nucleos de rendimiento.',
        'precio': 139990,
        'stock': 6,
    },
    {
        'categoria': 'Tarjetas graficas',
        'codigo': 'nvidia-rtx-4060-8gb',
        'nombre': 'GeForce RTX 4060 8 GB',
        'descripcion': 'Tarjeta grafica de 8 GB para juegos y creacion de contenido.',
        'precio': 379990,
        'stock': 4,
    },
    {
        'categoria': 'Tarjetas graficas',
        'codigo': 'amd-radeon-rx-7600-8gb',
        'nombre': 'Radeon RX 7600 8 GB',
        'descripcion': 'Tarjeta grafica de 8 GB con arquitectura RDNA 3.',
        'precio': 329990,
        'stock': 7,
    },
    {
        'categoria': 'Placas madre',
        'codigo': 'asus-prime-b550m-a',
        'nombre': 'ASUS Prime B550M-A',
        'descripcion': 'Placa madre micro-ATX con chipset B550 y socket AM4.',
        'precio': 99990,
        'stock': 5,
    },
    {
        'categoria': 'Placas madre',
        'codigo': 'msi-pro-b760m-p-ddr4',
        'nombre': 'MSI PRO B760M-P DDR4',
        'descripcion': 'Placa madre micro-ATX para procesadores Intel socket LGA1700.',
        'precio': 119990,
        'stock': 3,
    },
    {
        'categoria': 'Memoria RAM',
        'codigo': 'kingston-fury-beast-16gb',
        'nombre': 'Kingston Fury Beast 16 GB DDR4',
        'descripcion': 'Kit de memoria DDR4 de 3200 MHz para equipos de escritorio.',
        'precio': 39990,
        'stock': 12,
    },
    {
        'categoria': 'Almacenamiento',
        'codigo': 'wd-blue-sn580-1tb',
        'nombre': 'WD Blue SN580 NVMe 1 TB',
        'descripcion': 'Unidad SSD NVMe M.2 de 1 TB para cargas rapidas y uso diario.',
        'precio': 72990,
        'stock': 9,
    },
    {
        'categoria': 'Procesadores',
        'codigo': 'amd-ryzen-7-5700x',
        'nombre': 'AMD Ryzen 7 5700X',
        'descripcion': 'Procesador AM4 de 8 nucleos y 16 hilos para gaming y creacion.',
        'precio': 189990,
        'stock': 6,
    },
    {
        'categoria': 'Procesadores',
        'codigo': 'intel-core-i5-13400f',
        'nombre': 'Intel Core i5-13400F',
        'descripcion': 'Procesador hibrido de 10 nucleos para equipos de alto rendimiento.',
        'precio': 219990,
        'stock': 5,
    },
    {
        'categoria': 'Tarjetas graficas',
        'codigo': 'nvidia-rtx-4070-super-12gb',
        'nombre': 'GeForce RTX 4070 SUPER 12 GB',
        'descripcion': 'Tarjeta grafica de 12 GB para juegos en alta resolucion.',
        'precio': 749990,
        'stock': 3,
    },
    {
        'categoria': 'Tarjetas graficas',
        'codigo': 'amd-radeon-rx-7700-xt-12gb',
        'nombre': 'Radeon RX 7700 XT 12 GB',
        'descripcion': 'Tarjeta grafica de 12 GB para gaming de alto rendimiento.',
        'precio': 599990,
        'stock': 4,
    },
    {
        'categoria': 'Placas madre',
        'codigo': 'gigabyte-b650m-ds3h',
        'nombre': 'Gigabyte B650M DS3H',
        'descripcion': 'Placa madre AM5 micro-ATX con soporte para memoria DDR5.',
        'precio': 159990,
        'stock': 4,
    },
    {
        'categoria': 'Placas madre',
        'codigo': 'msi-pro-b650m-a-wifi',
        'nombre': 'MSI PRO B650M-A WiFi',
        'descripcion': 'Placa madre AM5 con WiFi integrado y formato micro-ATX.',
        'precio': 189990,
        'stock': 7,
    },
    {
        'categoria': 'Memoria RAM',
        'codigo': 'corsair-vengeance-32gb-ddr5',
        'nombre': 'Corsair Vengeance 32 GB DDR5',
        'descripcion': 'Kit de memoria DDR5 de 6000 MHz para plataformas recientes.',
        'precio': 119990,
        'stock': 6,
    },
    {
        'categoria': 'Memoria RAM',
        'codigo': 'kingston-fury-beast-32gb-ddr4',
        'nombre': 'Kingston Fury Beast 32 GB DDR4',
        'descripcion': 'Kit de memoria DDR4 de 3200 MHz para equipos de escritorio.',
        'precio': 69990,
        'stock': 8,
    },
    {
        'categoria': 'Almacenamiento',
        'codigo': 'kingston-nv2-2tb',
        'nombre': 'Kingston NV2 NVMe 2 TB',
        'descripcion': 'SSD M.2 PCIe 4.0 de 2 TB para juegos y bibliotecas de archivos.',
        'precio': 119990,
        'stock': 5,
    },
]


class Command(BaseCommand):
    help = 'Carga categorias y piezas de demostracion sin modificar productos existentes.'

    def handle(self, *args, **options):
        categorias = {}
        for nombre in {producto['categoria'] for producto in PRODUCTOS}:
            categoria, _ = Categoria.objects.get_or_create(nombre=nombre)
            categorias[nombre] = categoria

        creados = 0
        for producto in PRODUCTOS:
            datos = producto.copy()
            categoria = categorias[datos.pop('categoria')]
            _, creado = Pieza.objects.get_or_create(
                codigo=datos['codigo'],
                defaults={**datos, 'categoria': categoria},
            )
            creados += int(creado)

        self.stdout.write(
            self.style.SUCCESS(
                f'Catalogo listo: {len(categorias)} categorias; {creados} piezas nuevas.'
            )
        )
