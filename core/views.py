from django.shortcuts import render, get_object_or_404, redirect
from .models import Contenido
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ContenidoForm, ProfesorCreationForm, AdminPasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
import matplotlib.pyplot as plt
import io
import urllib, base64
import numpy as np
from django.contrib.auth.models import User
from django.contrib import messages



def home(request):
    return render(request, 'base.html')

def ver_materia(request, asignatura_url):
    # Diccionario para convertir el texto de la URL al nombre bonito
    nombres_materias = dict(Contenido.MATERIAS)
    
    # Obtenemos el nombre legible (ej: "calculo" -> "Cálculo")
    nombre_real = nombres_materias.get(asignatura_url, "Asignatura")

    # Filtramos el contenido de la base de datos solo para esta materia
    contenidos = Contenido.objects.filter(materia=asignatura_url)

    # Agrupamos por tipo para mostrarlo ordenado (Videos, PDFs, etc.)
    # Esto es clave para que el menú lateral funcione (#videos, #definiciones)
    tipos_orden = [
        ('definicion', 'Definiciones y Teoremas'),
        ('video', 'Videos'),
        ('notebook', 'Notebooks'),
        ('aplicacion', 'Aplicaciones'),
        ('pdf', 'Documentos PDF'),
    ]

    contenido_agrupado = []
    for tipo_codigo, tipo_nombre in tipos_orden:
        # Filtramos por tipo dentro de la materia
        items = contenidos.filter(tipo=tipo_codigo)
        if items.exists():
            contenido_agrupado.append((tipo_codigo, tipo_nombre, items))

    context = {
        'nombre_materia': nombre_real,
        'contenido_agrupado': contenido_agrupado,
    }
    return render(request, 'materia.html', context)

@login_required  # Esto protege la vista: solo usuarios autenticados pueden entrar
def agregar_contenido(request):
    if request.method == 'POST':
        form = ContenidoForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardamos el formulario pero sin enviar a la BD todavía
            nuevo_material = form.save(commit=False)
            # Asignamos automáticamente el autor (el usuario logueado)
            nuevo_material.autor = request.user 
            nuevo_material.save()
            
            # Redirigimos a la página de la materia donde acaba de subir la tarea
            # Así el profesor verifica inmediatamente que se subió en el lugar correcto
            return redirect('detalle_materia', asignatura_url=nuevo_material.materia)
    else:
        form = ContenidoForm()

    return render(request, 'agregar_contenido.html', {'form': form})


def generador_graficas(request):
    imagen_grafica = None
    error_mensaje = None
    codigo_inicial = "import numpy as np\nimport matplotlib.pyplot as plt\n\n# Crear datos\nx = np.linspace(-10, 10, 100)\ny = np.sin(x)\n\n# Graficar\nplt.figure(figsize=(6,4))\nplt.plot(x, y, label='Seno de x')\nplt.title('Ejemplo de Gráfica')\nplt.grid(True)\nplt.legend()"

    if request.method == 'POST':
        # Obtenemos el código que escribió el profesor
        codigo_usuario = request.POST.get('codigo')
        
        try:
            # PRECAUCIÓN: exec() ejecuta código real. En un entorno de producción real,
            # esto debe estar aislado (sandbox). Para este prototipo académico es funcional.
            
            # Preparamos un espacio seguro para que Matplotlib dibuje sin interfaz de ventana
            plt.switch_backend('AGG') 
            
            # Diccionario local para que el código tenga acceso a librerías estándar
            contexto_local = {'np': np, 'plt': plt}
            
            # Ejecutamos el código del usuario
            exec(codigo_usuario, {}, contexto_local)
            
            # Guardamos la gráfica en un buffer de memoria (RAM) en vez de disco
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            
            # Convertimos la imagen a código Base64 para enviarla al HTML
            string = base64.b64encode(buffer.read())
            uri = urllib.parse.quote(string)
            imagen_grafica = uri
            
            # Limpiamos la memoria para la siguiente gráfica
            plt.close()
            codigo_inicial = codigo_usuario # Mantenemos el código en pantalla

        except Exception as e:
            error_mensaje = f"Error en el código: {str(e)}"
            codigo_inicial = codigo_usuario

    return render(request, 'generador.html', {
        'imagen_grafica': imagen_grafica,
        'codigo': codigo_inicial,
        'error': error_mensaje
    })

# Verificación: Solo entra si es Superusuario (Administrador)
def es_admin(user):
    return user.is_superuser

@user_passes_test(es_admin)
def panel_admin(request):
    # Listar todos los profesores (excluyendo al superusuario actual)
    profesores = User.objects.filter(is_superuser=False).order_by('-date_joined')
    # Listar últimos contenidos subidos para moderación
    contenidos = Contenido.objects.all().order_by('-fecha_publicacion')[:20]
    
    return render(request, 'panel_admin.html', {
        'profesores': profesores,
        'contenidos': contenidos
    })

@user_passes_test(es_admin)
def crear_profesor(request):
    if request.method == 'POST':
        form = ProfesorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profesor creado exitosamente.')
            return redirect('panel_admin')
    else:
        form = ProfesorCreationForm()
    return render(request, 'admin_crear_profesor.html', {'form': form})

@user_passes_test(es_admin)
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if not usuario.is_superuser: # Seguridad: No borrarse a sí mismo
        usuario.delete()
        messages.success(request, 'Usuario eliminado.')
    return redirect('panel_admin')

@user_passes_test(es_admin)
def reset_password(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(usuario, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Contraseña restablecida para {usuario.username}')
            return redirect('panel_admin')
    else:
        form = AdminPasswordChangeForm(usuario)
    return render(request, 'admin_reset_password.html', {'form': form, 'usuario': usuario})

@user_passes_test(es_admin)
def eliminar_contenido(request, contenido_id):
    material = get_object_or_404(Contenido, id=contenido_id)
    material.delete()
    messages.success(request, 'Material eliminado correctamente.')
    # Regresa a la página anterior (el panel o la materia)
    return redirect(request.META.get('HTTP_REFERER', 'panel_admin'))

def paginas_interes(request):
    # RF-009: Buscar automáticamente todos los contenidos que tengan un enlace externo
    # Ordenamos por materia para poder agruparlos visualmente después
    links = Contenido.objects.exclude(link_externo__exact='') \
                             .exclude(link_externo__isnull=True) \
                             .order_by('materia', '-fecha_publicacion')
    
    return render(request, 'paginas_interes.html', {'links': links})