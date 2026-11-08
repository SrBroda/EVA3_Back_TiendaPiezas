from django.contrib import admin
from .models import Categoria, Perfil, Pieza

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rut', 'telefono', 'rol_institucional')

# Identidad Corporativa
admin.site.site_header = 'Tienda de componentes - Panel de administración'
admin.site.site_title = 'Administración de la tienda'
admin.site.index_title = 'Administración del catálogo'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Pieza)
class PiezaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'precio', 'stock', 'estado', 'vigente') # Vista tabular
    list_filter = ('categoria', 'estado', 'vigente') # Filtros laterales
    search_fields = ('codigo', 'nombre', 'descripcion') # Búsqueda textual
    list_editable = ('precio', 'stock', 'estado', 'vigente') # Edición rápida en grilla
    
    # Estructura modular del formulario
    fieldsets = (
        ('Información Principal', {
            'fields': ('codigo', 'nombre', 'categoria', 'descripcion')
        }),
        ('Valores y Estado', {
            'fields': ('precio', 'stock', 'estado', 'vigente')
        }),
        ('Multimedia', {
            'fields': ('imagen',)
        }),
    )