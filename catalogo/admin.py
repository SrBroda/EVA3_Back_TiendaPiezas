from django.contrib import admin
from .models import Categoria, Pieza

# Identidad Corporativa
admin.site.site_header = 'Hardware Store - Panel de Control'
admin.site.site_title = 'Hardware Store Admin'
admin.site.index_title = 'Gestión Operativa de Recursos y Servicios'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Pieza)
class PiezaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'precio', 'estado', 'vigente') # Vista tabular
    list_filter = ('categoria', 'estado', 'vigente') # Filtros laterales
    search_fields = ('codigo', 'nombre', 'descripcion') # Búsqueda textual
    list_editable = ('precio', 'estado', 'vigente') # Edición rápida en grilla
    
    # Estructura modular del formulario
    fieldsets = (
        ('Información Principal', {
            'fields': ('codigo', 'nombre', 'categoria', 'descripcion')
        }),
        ('Valores y Estado', {
            'fields': ('precio', 'estado', 'vigente')
        }),
        ('Multimedia', {
            'fields': ('imagen',)
        }),
    )