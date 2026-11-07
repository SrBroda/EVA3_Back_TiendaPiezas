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
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar-carrito/<int:id>/', views.agregar_carrito, name='agregar_carrito'),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('simular-solicitud/', views.simular_solicitud, name='simular_solicitud'),
]