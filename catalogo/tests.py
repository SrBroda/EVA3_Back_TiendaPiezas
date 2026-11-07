from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Perfil, Pieza


class CatalogoYCotizadorTests(TestCase):
	def setUp(self):
		self.categoria = Categoria.objects.create(nombre='Procesadores')
		self.pieza = Pieza.objects.create(
			codigo='cpu-prueba',
			nombre='Procesador de prueba',
			descripcion='Pieza para las pruebas del catálogo',
			precio=1000,
			stock=3,
			categoria=self.categoria,
		)

	def test_busqueda_por_codigo_categoria_y_paginacion(self):
		for numero in range(7):
			Pieza.objects.create(
				codigo=f'parte-{numero}',
				nombre=f'Parte {numero}',
				descripcion='Componente de prueba',
				precio=500,
				stock=1,
				categoria=self.categoria,
			)

		respuesta = self.client.get(reverse('catalogo_publico'))
		self.assertEqual(respuesta.status_code, 200)
		self.assertEqual(len(respuesta.context['piezas']), 6)
		self.assertEqual(respuesta.context['page_obj'].paginator.num_pages, 2)

		respuesta = self.client.get(
			reverse('catalogo_publico'),
			{'q': 'cpu-prueba', 'categoria': self.categoria.id},
		)
		self.assertEqual(len(respuesta.context['piezas']), 1)
		self.assertEqual(respuesta.context['piezas'][0], self.pieza)

	def test_carrito_calcula_iva_y_respeta_stock(self):
		ruta_agregar = reverse('agregar_carrito', args=[self.pieza.id])
		self.client.post(ruta_agregar)
		self.client.post(ruta_agregar)

		respuesta = self.client.get(reverse('ver_carrito'))
		self.assertEqual(respuesta.status_code, 200)
		self.assertEqual(respuesta.context['subtotal'], 2000)
		self.assertEqual(respuesta.context['iva'], 380)
		self.assertEqual(respuesta.context['total'], 2380)

		for _ in range(2):
			self.client.post(ruta_agregar)
		self.assertEqual(self.client.session['carrito'][str(self.pieza.id)], 3)

		self.client.post(reverse('vaciar_carrito'))
		self.assertNotIn('carrito', self.client.session)

	def test_simular_solicitud_descuenta_stock_y_vacia_sesion(self):
		self.client.post(reverse('agregar_carrito', args=[self.pieza.id]))
		respuesta = self.client.post(reverse('simular_solicitud'))

		self.assertRedirects(respuesta, reverse('catalogo_publico'))
		self.pieza.refresh_from_db()
		self.assertEqual(self.pieza.stock, 2)
		self.assertNotIn('carrito', self.client.session)

	def test_registro_guarda_datos_del_perfil(self):
		respuesta = self.client.post(
			reverse('registro_cliente'),
			{
				'username': 'cliente-prueba',
				'first_name': 'Ana',
				'last_name': 'Prueba',
				'email': 'ana@example.com',
				'rut': '12.345.678-9',
				'telefono': '+56912345678',
				'password1': 'UnaClaveFuerte-2026!',
				'password2': 'UnaClaveFuerte-2026!',
			},
		)
		self.assertRedirects(respuesta, reverse('login'))
		perfil = Perfil.objects.get(usuario__username='cliente-prueba')
		self.assertEqual(perfil.rut, '12.345.678-9')
