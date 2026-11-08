from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from catalogo.models import Categoria, Pieza


PRODUCTOS = [
    {
        'codigo': 'amd-ryzen-5-5600',
        'nombre': 'AMD Ryzen 5 5600',
        'categoria': 'Procesadores',
        'descripcion': 'Procesador AMD Ryzen 5 de la serie 5000 para equipos de escritorio.',
        'precio': 150000,
        'stock': 8,
        'imagen': 'piezas/Captura de pantalla 2026-11-07 204724.png',
    },
    {
        'codigo': 'amd-ryzen-7-5700x',
        'nombre': 'AMD Ryzen 7 5700X',
        'categoria': 'Procesadores',
        'descripcion': 'Procesador AMD Ryzen 7 de 8 nucleos y 16 hilos para escritorio.',
        'precio': 189990,
        'stock': 6,
        'imagen': 'piezas/Captura de pantalla 2026-11-07 204743.png',
    },
    {
        'codigo': 'asus-prime-b550m-a-wifi',
        'nombre': 'ASUS Prime B550M-A WiFi',
        'categoria': 'Placas Madre',
        'descripcion': 'Placa madre micro-ATX ASUS Prime con chipset B550 y WiFi.',
        'precio': 110000,
        'stock': 5,
        'imagen': 'piezas/Captura de pantalla 2026-11-07 204928.png',
    },
    {
        'codigo': 'corsair-vengeance-32gb-ddr5',
        'nombre': 'Corsair Vengeance 32 GB DDR5 RGB',
        'categoria': 'Memorias RAM',
        'descripcion': 'Kit Corsair Vengeance DDR5 de 32 GB con iluminacion RGB.',
        'precio': 119990,
        'stock': 6,
        'imagen': 'piezas/Captura de pantalla 2026-11-07 205002.png',
    },
    {
        'codigo': 'gigabyte-b650m-ds3h-ax',
        'nombre': 'Gigabyte B650M DS3H AX',
        'categoria': 'Placas Madre',
        'descripcion': 'Placa madre micro-ATX AM5 Gigabyte con conectividad AX.',
        'precio': 159990,
        'stock': 4,
        'imagen': 'piezas/Captura de pantalla 2026-11-07 205131.png',
    },
    {
        'codigo': 'intel-core-i5-12400f',
        'nombre': 'Intel Core i5-12400F',
        'categoria': 'Procesadores',
        'descripcion': 'Procesador Intel Core i5 de 12a generacion para escritorio.',
        'precio': 140000,
        'stock': 6,
        'imagen': 'piezas/Captura de pantalla 2026-11-07 205157.png',
    },
    {
        'codigo': 'intel-core-i5-13400f',
        'nombre': 'Intel Core i5-13400F',
        'categoria': 'Procesadores',
        'descripcion': 'Procesador Intel Core i5 de 13a generacion para escritorio.',
        'precio': 219990,
        'stock': 5,
        'imagen': 'piezas/Captura de pantalla 2026-11-07 205219.png',
    },
    {
        'codigo': 'kingston-fury-beast-16gb-ddr4',
        'nombre': 'Kingston Fury Beast 16 GB DDR4',
        'categoria': 'Memorias RAM',
        'descripcion': 'Modulo Kingston Fury Beast DDR4 de 16 GB para escritorio.',
        'precio': 39990,
        'stock': 12,
        'imagen': 'piezas/Captura de pantalla 2026-11-07 205240.png',
    },
    {
        'codigo': 'kingston-fury-beast-rgb-32gb-ddr4',
        'nombre': 'Kingston Fury Beast RGB 32 GB DDR4',
        'categoria': 'Memorias RAM',
        'descripcion': 'Kit Kingston Fury Beast RGB DDR4 de 32 GB para escritorio.',
        'precio': 69990,
        'stock': 8,
        'imagen': 'piezas/Captura de pantalla 2026-11-07 205324.png',
    },
    {
        'codigo': 'kingston-nv2-2tb',
        'nombre': 'Kingston NV2 NVMe 2 TB',
        'categoria': 'Almacenamiento',
        'descripcion': 'Unidad SSD Kingston NV2 M.2 NVMe de 2 TB.',
        'precio': 119990,
        'stock': 5,
        'imagen': 'piezas/Captura de pantalla 2026-11-07 205345.png',
    },
    {
        'codigo': 'asrock-b650m-pro-rs-wifi',
        'nombre': 'ASRock B650M Pro RS WiFi',
        'categoria': 'Placas Madre',
        'descripcion': 'Placa madre micro-ATX AM5 ASRock B650M Pro RS con WiFi.',
        'precio': 169990,
        'stock': 5,
        'imagen': 'piezas/Captura de pantalla 2026-11-07 205412.png',
    },
    {
        'codigo': 'asus-dual-radeon-rx-7600-8gb',
        'nombre': 'ASUS Dual Radeon RX 7600 8 GB',
        'categoria': 'Tarjetas Gráficas',
        'descripcion': 'Tarjeta grafica ASUS Dual Radeon RX 7600 con 8 GB de memoria.',
        'precio': 329990,
        'stock': 7,
        'imagen': 'piezas/Captura de pantalla 2026-11-07 205433.png',
    },
    {
        'codigo': 'asus-tuf-radeon-rx-7700-xt-12gb',
        'nombre': 'ASUS TUF Radeon RX 7700 XT 12 GB',
        'categoria': 'Tarjetas Gráficas',
        'descripcion': 'Tarjeta grafica ASUS TUF Radeon RX 7700 XT con 12 GB.',
        'precio': 599990,
        'stock': 4,
        'imagen': 'Captura de pantalla 2026-11-07 205451.png',
    },
    {
        'codigo': 'wd-blue-sn580-1tb',
        'nombre': 'WD Blue SN580 NVMe 1 TB',
        'categoria': 'Almacenamiento',
        'descripcion': 'Unidad SSD WD Blue SN580 M.2 NVMe de 1 TB.',
        'precio': 72990,
        'stock': 9,
        'imagen': 'Captura de pantalla 2026-11-07 205511.png',
    },
]


class Command(BaseCommand):
    help = 'Crea productos de muestra y asigna las imágenes locales proporcionadas.'

    def handle(self, *args, **options):
        faltantes = [
            producto['imagen']
            for producto in PRODUCTOS
            if not (Path(settings.MEDIA_ROOT) / producto['imagen']).is_file()
        ]
        if faltantes:
            self.stderr.write(
                self.style.WARNING(
                    'Algunas fotos no están disponibles; los productos se crearán '
                    'sin imagen: ' + ', '.join(faltantes)
                )
            )

        categorias = {}
        for producto in PRODUCTOS:
            nombre_categoria = producto['categoria']
            if nombre_categoria not in categorias:
                categorias[nombre_categoria], _ = Categoria.objects.get_or_create(
                    nombre=nombre_categoria
                )

        creados = 0
        imagenes_asignadas = 0
        for producto in PRODUCTOS:
            datos = producto.copy()
            nombre_categoria = datos.pop('categoria')
            imagen = datos.pop('imagen')
            ruta_imagen = Path(settings.MEDIA_ROOT) / imagen
            defaults = {
                **datos,
                'categoria': categorias[nombre_categoria],
            }
            if ruta_imagen.is_file():
                defaults['imagen'] = imagen
            pieza, creado = Pieza.objects.get_or_create(
                codigo=producto['codigo'],
                defaults=defaults,
            )
            creados += int(creado)
            if not creado and not pieza.imagen and ruta_imagen.is_file():
                pieza.imagen = imagen
                pieza.save(update_fields=['imagen'])
                imagenes_asignadas += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'{creados} productos creados; '
                f'{imagenes_asignadas} imágenes asignadas a productos existentes.'
            )
        )