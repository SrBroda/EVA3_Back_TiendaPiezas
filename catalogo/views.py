from decimal import Decimal, ROUND_HALF_UP

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import PiezaForm, RegistroClienteForm
from .models import Categoria, Perfil, Pieza

# Función para verificar si es staff
def es_staff(user):
    return user.is_staff

@login_required
@user_passes_test(es_staff)
def crear_pieza(request):
    if request.method == 'POST':
        form = PiezaForm(request.POST, request.FILES) # request.FILES obligatorio para multimedia
        if form.is_valid():
            form.save()
            messages.success(request, 'Pieza agregada correctamente.')
            return redirect('listar_piezas_admin') # Ajustaremos esta URL luego
    else:
        form = PiezaForm()
    return render(request, 'catalogo/form_pieza.html', {'form': form, 'titulo': 'Agregar Pieza'})

@login_required
@user_passes_test(es_staff)
def editar_pieza(request, id):
    pieza = get_object_or_404(Pieza, id=id)
    if request.method == 'POST':
        form = PiezaForm(request.POST, request.FILES, instance=pieza) # Formulario precargado
        if form.is_valid():
            form.save()
            messages.success(request, 'Pieza actualizada correctamente.')
            return redirect('listar_piezas_admin')
    else:
        form = PiezaForm(instance=pieza)
    return render(request, 'catalogo/form_pieza.html', {'form': form, 'titulo': 'Editar Pieza'})

@login_required
@user_passes_test(es_staff)
def eliminar_pieza(request, id):
    pieza = get_object_or_404(Pieza, id=id)
    if request.method == 'POST':
        # Eliminación física (también puedes optar por baja lógica: pieza.vigente = False; pieza.save())
        pieza.delete()
        messages.success(request, 'Pieza eliminada.')
        return redirect('listar_piezas_admin')
    return render(request, 'catalogo/confirmar_eliminar.html', {'pieza': pieza})


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
            messages.success(request, 'Tu cuenta se creó correctamente. Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroClienteForm()
    return render(request, 'catalogo/registro.html', {'form': form})


def catalogo_publico(request):
    piezas = Pieza.objects.filter(vigente=True).select_related('categoria')
    query = request.GET.get('q', '').strip()
    categoria_seleccionada = request.GET.get('categoria', '').strip()

    if query:
        piezas = piezas.filter(
            Q(nombre__icontains=query)
            | Q(codigo__icontains=query)
            | Q(descripcion__icontains=query)
        )
    if categoria_seleccionada:
        piezas = piezas.filter(categoria_id=categoria_seleccionada)

    paginator = Paginator(piezas.order_by('nombre'), 6)
    page_obj = paginator.get_page(request.GET.get('page'))
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


@require_POST
def agregar_al_carrito(request, id):
    pieza = get_object_or_404(Pieza, id=id, vigente=True)
    if pieza.stock <= 0:
        messages.error(request, 'Esta pieza no tiene stock disponible.')
        return redirect('catalogo_publico')

    carrito = request.session.get('carrito', {})
    if not isinstance(carrito, dict):
        carrito = {}
    try:
        cantidad_actual = max(int(carrito.get(str(pieza.id), 0)), 0)
    except (TypeError, ValueError):
        cantidad_actual = 0

    if cantidad_actual >= pieza.stock:
        messages.warning(request, 'No hay más unidades disponibles de esta pieza.')
        return redirect('catalogo_publico')

    carrito[str(pieza.id)] = cantidad_actual + 1
    request.session['carrito'] = carrito
    messages.success(request, 'Pieza agregada al carrito.')
    return redirect('catalogo_publico')


def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    if not isinstance(carrito, dict):
        carrito = {}

    pieza_ids = []
    cantidades = {}
    for pieza_id, cantidad in carrito.items():
        try:
            pieza_id = str(int(pieza_id))
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            continue
        if cantidad > 0:
            pieza_ids.append(pieza_id)
            cantidades[pieza_id] = cantidad

    piezas = {
        str(pieza.id): pieza
        for pieza in Pieza.objects.filter(id__in=pieza_ids, vigente=True)
    }
    items = []
    subtotal = Decimal('0')
    for pieza_id in pieza_ids:
        pieza = piezas.get(pieza_id)
        if pieza is None:
            continue
        cantidad = cantidades[pieza_id]
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
    total = subtotal + iva
    return render(
        request,
        'catalogo/carrito.html',
        {'items': items, 'subtotal': subtotal, 'iva': iva, 'total': total},
    )


@require_POST
def eliminar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})
    if isinstance(carrito, dict):
        carrito.pop(str(id), None)
        request.session['carrito'] = carrito
    messages.info(request, 'Pieza eliminada del carrito.')
    return redirect('ver_carrito')


@require_POST
def simular_compra(request):
    carrito = request.session.get('carrito', {})
    if not isinstance(carrito, dict) or not carrito:
        messages.warning(request, 'El carrito está vacío.')
        return redirect('ver_carrito')

    try:
        with transaction.atomic():
            for pieza_id, cantidad in carrito.items():
                try:
                    pieza_id = int(pieza_id)
                    cantidad = int(cantidad)
                except (TypeError, ValueError) as error:
                    raise ValueError('El carrito contiene una cantidad no válida.') from error
                if cantidad <= 0:
                    raise ValueError('El carrito contiene una cantidad no válida.')

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
                if pieza.stock == 0:
                    pieza.estado = 'Agotado'
                    pieza.save(update_fields=['stock', 'estado'])
                else:
                    pieza.save(update_fields=['stock'])
    except Pieza.DoesNotExist:
        messages.error(request, 'Una pieza del carrito ya no está disponible.')
        return redirect('ver_carrito')
    except ValueError as error:
        messages.error(request, str(error))
        return redirect('ver_carrito')

    request.session.flush()
    messages.success(request, 'Compra simulada correctamente. ¡Gracias!')
    return redirect('catalogo_publico')