from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.catalogo_publico, name='catalogo_publico'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='catalogo/login.html'),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout',
    ),
    path('registro/', views.registro_cliente, name='registro_cliente'),
    path('pieza/<int:id>/', views.detalle_pieza, name='detalle_pieza'),
    path('gestion/piezas/', views.listar_piezas_admin, name='listar_piezas_admin'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path(
        'carrito/actualizar/<int:id>/',
        views.actualizar_cantidad_carrito,
        name='actualizar_cantidad_carrito',
    ),
    path(
        'carrito/eliminar/<int:id>/',
        views.eliminar_del_carrito,
        name='eliminar_del_carrito',
    ),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path(
        'agregar-carrito/<int:id>/',
        views.agregar_al_carrito,
        name='agregar_al_carrito',
    ),
    path('simular-compra/', views.simular_compra, name='simular_compra'),
    path('agregar-pieza/', views.crear_pieza, name='crear_pieza'),
    path('editar-pieza/<int:id>/', views.editar_pieza, name='editar_pieza'),
    path('eliminar-pieza/<int:id>/', views.eliminar_pieza, name='eliminar_pieza'),
]