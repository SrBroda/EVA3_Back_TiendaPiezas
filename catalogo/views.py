from decimal import Decimal, ROUND_HALF_UP

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import RegistroClienteForm
from .models import Categoria, Perfil, Pieza


def catalogo_publico(request):
	piezas = Pieza.objects.filter(vigente=True).select_related('categoria')
	query = request.GET.get('q', '').strip()
	categoria_seleccionada = request.GET.get('categoria', '').strip()

	if query:
		piezas = piezas.filter(
			Q(codigo__icontains=query)
			| Q(nombre__icontains=query)
			| Q(descripcion__icontains=query)
		)
	if categoria_seleccionada:
		piezas = piezas.filter(categoria_id=categoria_seleccionada)

	page_obj = Paginator(piezas.order_by('nombre'), 6).get_page(
		request.GET.get('page')
	)
	return render(
		request,
		'catalogo/catalogo_publico.html',
		{
			'piezas': page_obj,
			'page_obj': page_obj,
			'categorias': Categoria.objects.order_by('nombre'),
			'query': query,
			'categoria_seleccionada': categoria_seleccionada,
		},
	)


def detalle_pieza(request, id):
	pieza = get_object_or_404(
		Pieza.objects.select_related('categoria'),
		id=id,
		vigente=True,
	)
	return render(request, 'catalogo/detalle_pieza.html', {'pieza': pieza})


def agregar_carrito(request, id):
	if request.method != 'POST':
		return redirect('catalogo_publico')

	pieza = get_object_or_404(Pieza, id=id, vigente=True)
	carrito = request.session.get('carrito', {})
	if not isinstance(carrito, dict):
		carrito = {}
	try:
		cantidad_actual = max(int(carrito.get(str(pieza.id), 0)), 0)
	except (TypeError, ValueError):
		cantidad_actual = 0

	if pieza.stock <= 0:
		messages.error(request, 'Esta pieza no tiene stock disponible.')
	elif cantidad_actual >= pieza.stock:
		messages.warning(request, 'No hay más unidades disponibles de esta pieza.')
	else:
		carrito[str(pieza.id)] = cantidad_actual + 1
		request.session['carrito'] = carrito
		messages.success(request, 'Pieza agregada al cotizador.')
	return redirect('catalogo_publico')


def ver_carrito(request):
	carrito = request.session.get('carrito', {})
	if not isinstance(carrito, dict):
		carrito = {}

	cantidades = {}
	for pieza_id, cantidad in carrito.items():
		try:
			pieza_id = str(int(pieza_id))
			cantidad = int(cantidad)
		except (TypeError, ValueError):
			continue
		if cantidad > 0:
			cantidades[pieza_id] = cantidad

	piezas = {
		str(pieza.id): pieza
		for pieza in Pieza.objects.filter(
			id__in=cantidades,
			vigente=True,
		).select_related('categoria')
	}
	items = []
	subtotal = Decimal('0')
	for pieza_id, cantidad in cantidades.items():
		pieza = piezas.get(pieza_id)
		if pieza is None:
			continue
		total_linea = Decimal(pieza.precio) * cantidad
		subtotal += total_linea
		items.append({
			'pieza': pieza,
			'cantidad': cantidad,
			'subtotal': total_linea,
		})

	iva = (subtotal * Decimal('0.19')).quantize(
		Decimal('1'), rounding=ROUND_HALF_UP
	)
	return render(
		request,
		'catalogo/carrito.html',
		{
			'items': items,
			'subtotal': subtotal,
			'iva': iva,
			'total': subtotal + iva,
		},
	)


@require_POST
def vaciar_carrito(request):
	request.session.pop('carrito', None)
	messages.info(request, 'Cotizador vaciado.')
	return redirect('ver_carrito')


@require_POST
def simular_solicitud(request):
	carrito = request.session.get('carrito', {})
	if not isinstance(carrito, dict) or not carrito:
		messages.warning(request, 'El cotizador está vacío.')
		return redirect('ver_carrito')

	try:
		with transaction.atomic():
			for pieza_id, cantidad in carrito.items():
				try:
					pieza_id = int(pieza_id)
					cantidad = int(cantidad)
				except (TypeError, ValueError) as error:
					raise ValueError('El cotizador contiene una cantidad no válida.') from error
				if cantidad <= 0:
					raise ValueError('El cotizador contiene una cantidad no válida.')

				pieza = Pieza.objects.select_for_update().get(
					id=pieza_id,
					vigente=True,
				)
				if pieza.stock < cantidad:
					raise ValueError(
						f'Stock insuficiente para {pieza.nombre}. '
						f'Disponibles: {pieza.stock}.'
					)
				pieza.stock -= cantidad
				pieza.estado = 'Agotado' if pieza.stock == 0 else 'Disponible'
				pieza.save(update_fields=['stock', 'estado'])
	except Pieza.DoesNotExist:
		messages.error(request, 'Una pieza del cotizador ya no está disponible.')
		return redirect('ver_carrito')
	except ValueError as error:
		messages.error(request, str(error))
		return redirect('ver_carrito')

	request.session.flush()
	messages.success(request, 'Solicitud simulada correctamente.')
	return redirect('catalogo_publico')


def registro_cliente(request):
	if request.method == 'POST':
		form = RegistroClienteForm(request.POST)
		if form.is_valid():
			usuario = form.save()
			Perfil.objects.create(
				usuario=usuario,
				rut=form.cleaned_data['rut'],
				telefono=form.cleaned_data['telefono'],
				rol_institucional='Cliente',
			)
			messages.success(request, 'Cuenta creada correctamente. Ya puedes iniciar sesión.')
			return redirect('login')
	else:
		form = RegistroClienteForm()
	return render(request, 'catalogo/registro.html', {'form': form})
