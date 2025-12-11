import os 
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError 
from .models import Contenido

# ==============================================================================
# FORMULARIO DE GESTIÓN DE CONTENIDO (Para Profesores)
# ==============================================================================
class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = [
            'materia', 'tipo', 'titulo', 
            'ponente', 'fecha_evento',
            'descripcion', 
            'imagen',            
            'archivo_pdf',       
            'archivo_notebook',  
            # 'archivo_video',   
            'link_video',        
            'link_externo'
        ]
        
        widgets = {
            'materia': forms.Select(attrs={'class': 'form-control', 'id': 'select-materia'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'id': 'input-titulo', 'placeholder': 'Ej: Derivadas Parciales'}),
            'ponente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Dr. Juan Pérez'}),
            'fecha_evento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe aquí la explicación...'}),
            
            # --- VALIDACIÓN VISUAL (FILTROS EN EL EXPLORADOR DE ARCHIVOS) ---
            'imagen': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'  # Acepta jpg, png, gif, webp, etc.
            }),
            'archivo_pdf': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': '.pdf'     # Solo muestra PDFs
            }),
            'archivo_notebook': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': '.ipynb'   # Solo muestra Notebooks de Jupyter
            }),
            
            'link_video': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/...'}),
            'link_externo': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://sitio-interesante.com'})
        }

    # ==========================================================================
    # VALIDACIONES DE SERVIDOR (SEGURIDAD REAL)
    # ==========================================================================

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            # Obtener extensión
            ext = os.path.splitext(imagen.name)[1].lower()
            validas = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
            if ext not in validas:
                raise ValidationError("Solo se permiten archivos de imagen (jpg, png, etc).")
        return imagen

    def clean_archivo_pdf(self):
        pdf = self.cleaned_data.get('archivo_pdf')
        if pdf:
            ext = os.path.splitext(pdf.name)[1].lower()
            if ext != '.pdf':
                raise ValidationError("El archivo debe ser un PDF válido (.pdf).")
        return pdf

    def clean_archivo_notebook(self):
        nb = self.cleaned_data.get('archivo_notebook')
        if nb:
            ext = os.path.splitext(nb.name)[1].lower()
            if ext != '.ipynb':
                raise ValidationError("El archivo debe ser un Jupyter Notebook (.ipynb).")
        return nb

# ==============================================================================
# FORMULARIO PARA CREAR PROFESORES
# ==============================================================================
class ProfesorCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Contraseña")
    nombre_completo = forms.CharField(max_length=100, label="Nombre del Profesor", widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.first_name = self.cleaned_data['nombre_completo']
        if commit:
            user.save()
            grupo_profes, created = Group.objects.get_or_create(name='Profesores')
            user.groups.add(grupo_profes)
            user.is_staff = True 
            user.save()
        return user

# ==============================================================================
# FORMULARIO PARA RESETEAR CONTRASEÑA
# ==============================================================================
class AdminPasswordChangeForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'