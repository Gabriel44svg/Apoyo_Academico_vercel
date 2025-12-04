from django.db import models
from django.contrib.auth.models import User

class Contenido(models.Model):
    # Opciones para las Materias (Basado en tu Sidebar)
    MATERIAS = [
        ('probabilidad', 'Probabilidad y Estadística'),
        ('calculo', 'Cálculo'),
        ('ecuaciones', 'Ecuaciones Diferenciales'),
        ('optimizacion', 'Optimización'),
        ('algebra', 'Álgebra Lineal'),
        ('metodos', 'Métodos Numéricos'),
        ('procesos', 'Procesos Estocásticos'),
        ('geometria', 'Geometría'),
        ('coloquios', 'Coloquios'),
        ('seminarios', 'Seminarios'),
    ]

    # Opciones para el Tipo de Recurso (SRS RF-008) [cite: 52]
    TIPOS = [
        ('definicion', 'Definición/Teorema'),
        ('video', 'Video'),
        ('notebook', 'Notebook (.ipynb)'),
        ('aplicacion', 'Aplicación/Streamlit'),
        ('pdf', 'Archivo PDF'),
        ('url', 'Página de Interés/URL Externa'),
    ]

    # --- TUS REQUERIMIENTOS ESPECÍFICOS ---
    titulo = models.CharField(max_length=200, verbose_name="Título del Material")
    descripcion = models.TextField(verbose_name="Breve Explicación")
    # --------------------------------------

    materia = models.CharField(max_length=50, choices=MATERIAS, verbose_name="Asignatura") 
    tipo = models.CharField(max_length=50, choices=TIPOS, verbose_name="Tipo de Recurso") 
    
    # Archivos y Links (Opcionales según el tipo)
    archivo_pdf = models.FileField(upload_to='pdfs/', blank=True, null=True, verbose_name="Archivo PDF")
    archivo_notebook = models.FileField(upload_to='notebooks/', blank=True, null=True, verbose_name="Notebook Jupyter")
    link_video = models.URLField(blank=True, null=True, verbose_name="Link de Video (YouTube/Vimeo)")
    link_externo = models.URLField(blank=True, null=True, verbose_name="Link Externo (Para pág. interés)")

    # Metadatos de control (SRS RF-006, RF-007)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Profesor/Autor")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True, verbose_name="Imagen o Diagrama")
    archivo_video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="Video (Archivo MP4)")
    
    ponente = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre del Ponente")
    fecha_evento = models.DateField(blank=True, null=True, verbose_name="Fecha del Evento")
    
    class Meta:
        verbose_name = "Material Didáctico"
        verbose_name_plural = "Materiales Didácticos"

    def __str__(self):
        return f"{self.titulo} ({self.get_materia_display()})"