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

	def test_detalle_muestra_descripcion_completa(self):
		respuesta = self.client.get(
			reverse('detalle_pieza', args=[self.pieza.id])
		)
		self.assertEqual(respuesta.status_code, 200)
		self.assertContains(respuesta, self.pieza.descripcion)

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

	def test_actualizar_cantidad_valida_stock(self):
		ruta_agregar = reverse('agregar_al_carrito', args=[self.pieza.id])
		self.client.post(ruta_agregar)
		ruta_actualizar = reverse('actualizar_cantidad_carrito', args=[self.pieza.id])

		respuesta = self.client.post(ruta_actualizar, {'cantidad': 3})
		self.assertRedirects(respuesta, reverse('ver_carrito'))
		self.assertEqual(self.client.session['carrito'][str(self.pieza.id)], 3)

		self.client.post(ruta_actualizar, {'cantidad': 4})
		self.assertEqual(self.client.session['carrito'][str(self.pieza.id)], 3)

	def test_simular_compra_conserva_sesion_autenticada(self):
		from django.contrib.auth.models import User

		usuario = User.objects.create_user(
			username='cliente-carrito',
			password='UnaClaveDePrueba-123',
		)
		self.client.force_login(usuario)
		self.client.post(reverse('agregar_al_carrito', args=[self.pieza.id]))
		self.client.post(reverse('simular_compra'))

		self.assertIn('_auth_user_id', self.client.session)

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

	def test_logout_se_realiza_por_post(self):
		from django.contrib.auth.models import User

		usuario = User.objects.create_user(
			username='cliente-logout',
			password='UnaClaveDePrueba-123',
		)
		self.client.force_login(usuario)

		respuesta_get = self.client.get(reverse('logout'))
		self.assertEqual(respuesta_get.status_code, 405)

		respuesta_post = self.client.post(reverse('logout'))
		self.assertRedirects(respuesta_post, reverse('login'))
		self.assertNotIn('_auth_user_id', self.client.session)

	def test_staff_crea_actualiza_y_elimina_pieza_con_confirmacion(self):
		from django.contrib.auth.models import User

		usuario = User.objects.create_user(
			username='staff-crud',
			password='UnaClaveDePrueba-123',
			is_staff=True,
		)
		self.client.force_login(usuario)
		url_listado = reverse('listar_piezas_admin')
		url_crear = reverse('crear_pieza')
		datos = {
			'codigo': 'pieza-crud',
			'nombre': 'Pieza CRUD',
			'categoria': self.categoria.id,
			'descripcion': 'Descripción de prueba',
			'precio': 5000,
			'stock': 4,
			'estado': 'Disponible',
			'vigente': 'on',
		}

		respuesta = self.client.post(url_crear, datos)
		self.assertRedirects(respuesta, url_listado)
		pieza = Pieza.objects.get(codigo='pieza-crud')

		datos['precio'] = 6000
		datos['stock'] = 7
		respuesta = self.client.post(reverse('editar_pieza', args=[pieza.id]), datos)
		self.assertRedirects(respuesta, url_listado)
		pieza.refresh_from_db()
		self.assertEqual(pieza.precio, 6000)
		self.assertEqual(pieza.stock, 7)

		url_eliminar = reverse('eliminar_pieza', args=[pieza.id])
		self.assertEqual(self.client.get(url_eliminar).status_code, 200)
		respuesta = self.client.post(url_eliminar)
		self.assertRedirects(respuesta, url_listado)
		self.assertFalse(Pieza.objects.filter(pk=pieza.id).exists())
