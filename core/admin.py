from django.contrib import admin
from .models import Contenido

@admin.register(Contenido)
class ContenidoAdmin(admin.ModelAdmin):
    # Esto define qué columnas ves en la lista general
    list_display = ('titulo', 'materia', 'tipo', 'autor', 'fecha_publicacion')
    
    # Esto permite filtrar por materia o tipo en la barra lateral derecha del admin
    list_filter = ('materia', 'tipo', 'autor')
    
    # Barra de búsqueda
    search_fields = ('titulo', 'descripcion')