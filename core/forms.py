from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import SetPasswordForm
from .models import Contenido

# ==============================================================================
# FORMULARIO DE GESTIÓN DE CONTENIDO (Para Profesores)
# ==============================================================================
class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = [
            # Campos Generales
            'materia', 
            'tipo', 
            'titulo', 
            
            # Campos Específicos para Coloquios/Seminarios
            'ponente', 
            'fecha_evento',
            
            # Descripción (Markdown/LaTeX)
            'descripcion', 
            
            # Archivos y Multimedia (Soporte Múltiple)
            'imagen',            # Nuevo: Fotos/Diagramas
            'archivo_pdf',       # Documentos
            'archivo_notebook',  # Jupyter
            'archivo_video',     # Archivos MP4
            'link_video',        # YouTube/Externo
            'link_externo'       # URLs de interés
        ]
        
        # WIDGETS: Añadimos clases CSS y IDs para control visual y JavaScript
        widgets = {
            'materia': forms.Select(attrs={
                'class': 'form-control', 
                'id': 'select-materia'  # ID CRÍTICO para el script de eventos
            }),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            
            'titulo': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'input-titulo',   # ID CRÍTICO para cambiar placeholder
                'placeholder': 'Ej: Derivadas Parciales'
            }),
            
            # Campos de Eventos (Ocultos por defecto vía JS en el HTML)
            'ponente': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: Dr. Juan Pérez'
            }),
            'fecha_evento': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'  # Activa el calendario nativo del navegador
            }),
            
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Escribe aquí la explicación. Soporta **Markdown** y fórmulas LaTeX entre signos $'
            }),
            
            # Inputs de Archivos
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
            'archivo_pdf': forms.FileInput(attrs={'class': 'form-control-file'}),
            'archivo_notebook': forms.FileInput(attrs={'class': 'form-control-file'}),
            'archivo_video': forms.FileInput(attrs={'class': 'form-control-file'}),
            
            # Inputs de Enlaces
            'link_video': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://youtube.com/...'
            }),
            'link_externo': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://sitio-interesante.com'
            })
        }

# ==============================================================================
# FORMULARIO PARA CREAR PROFESORES (Para Panel Admin)
# ==============================================================================
class ProfesorCreationForm(forms.ModelForm):
    # Campos adicionales que no están directos en el modelo User pero necesitamos
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Contraseña"
    )
    nombre_completo = forms.CharField(
        max_length=100, 
        label="Nombre del Profesor", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email'] # El username será el usuario de acceso
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # 1. Crear la instancia del usuario sin guardar aún en BD
        user = super().save(commit=False)
        
        # 2. Establecer la contraseña de forma segura (Hash)
        user.set_password(self.cleaned_data['password'])
        
        # 3. Guardar el nombre
        user.first_name = self.cleaned_data['nombre_completo']
        
        if commit:
            user.save()
            # 4. Asignar automáticamente al grupo "Profesores"
            # Esto define sus permisos (solo agregar, no borrar)
            grupo_profes, created = Group.objects.get_or_create(name='Profesores')
            user.groups.add(grupo_profes)
            
            # 5. Dar estatus de staff para validaciones internas (pero sin superusuario)
            user.is_staff = True 
            user.save()
            
        return user

# ==============================================================================
# FORMULARIO PARA RESETEAR CONTRASEÑA (Para Panel Admin)
# ==============================================================================
class AdminPasswordChangeForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        # Aplicar estilo Bootstrap a todos los campos generados
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'