from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Pieza


class CatalogoYCarritoTests(TestCase):
	def setUp(self):
		self.categoria = Categoria.objects.create(nombre='Procesadores')
		self.pieza = Pieza.objects.create(
			codigo='cpu-prueba',
			nombre='Procesador de prueba',
			descripcion='Pieza para pruebas del catálogo',
			precio=1000,
			stock=3,
			categoria=self.categoria,
		)

	def test_busqueda_y_paginacion_del_catalogo(self):
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
			{'q': 'cpu-prueba'},
		)
		self.assertEqual(len(respuesta.context['piezas']), 1)
		self.assertEqual(respuesta.context['piezas'][0], self.pieza)

	def test_carrito_calcula_totales_y_compra_descuenta_stock(self):
		ruta_agregar = reverse('agregar_al_carrito', args=[self.pieza.id])
		self.client.post(ruta_agregar)
		self.client.post(ruta_agregar)

		respuesta = self.client.get(reverse('ver_carrito'))
		self.assertEqual(respuesta.status_code, 200)
		self.assertEqual(respuesta.context['subtotal'], 2000)
		self.assertEqual(respuesta.context['iva'], 380)
		self.assertEqual(respuesta.context['total'], 2380)

		respuesta = self.client.post(reverse('simular_compra'))
		self.assertRedirects(respuesta, reverse('catalogo_publico'))
		self.pieza.refresh_from_db()
		self.assertEqual(self.pieza.stock, 1)
		self.assertNotIn('carrito', self.client.session)

	def test_agregar_no_supera_stock_disponible(self):
		self.pieza.stock = 1
		self.pieza.save(update_fields=['stock'])
		ruta_agregar = reverse('agregar_al_carrito', args=[self.pieza.id])

		self.client.post(ruta_agregar)
		self.client.post(ruta_agregar)

		self.assertEqual(self.client.session['carrito'][str(self.pieza.id)], 1)

	def test_plantillas_de_acceso_y_formulario_pieza_renderizan(self):
		for nombre_url in ('login', 'registro_cliente'):
			respuesta = self.client.get(reverse(nombre_url))
			self.assertEqual(respuesta.status_code, 200)
			self.assertContains(respuesta, '<form')

		from django.contrib.auth.models import User

		usuario = User.objects.create_user(
			username='staff-prueba',
			password='UnaClaveDePrueba-123',
			is_staff=True,
		)
		self.client.force_login(usuario)
		respuesta = self.client.get(reverse('crear_pieza'))
		self.assertEqual(respuesta.status_code, 200)
		self.assertContains(respuesta, 'multipart/form-data')
