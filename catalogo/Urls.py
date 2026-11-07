from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Rutas de autenticación
    path('login/', auth_views.LoginView.as_view(template_name='catalogo/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', views.registro_cliente, name='registro_cliente'),
    
    # Aquí irán las rutas de tu CRUD protegido que ya hiciste
    path('agregar-pieza/', views.crear_pieza, name='crear_pieza'),
    path('editar-pieza/<int:id>/', views.editar_pieza, name='editar_pieza'),
    path('eliminar-pieza/<int:id>/', views.eliminar_pieza, name='eliminar_pieza'),
]