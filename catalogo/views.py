from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import PiezaForm, RegistroClienteForm
from .models import Perfil, Pieza

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