from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings               
from django.conf.urls.static import static
from core.views import home, ver_materia, agregar_contenido, generador_graficas, panel_admin, crear_profesor, eliminar_usuario, reset_password, eliminar_contenido, paginas_interes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('ingresar/', LoginView.as_view(template_name='ingresar.html'), name='login'),
    path('salir/', LogoutView.as_view(next_page='home'), name='logout'),

    path('materia/<str:asignatura_url>/', ver_materia, name='detalle_materia'),
    path('agregar/', agregar_contenido, name='agregar_contenido'),
    path('herramientas/generador-graficas/', generador_graficas, name='generador'),

    path('panel-control/', panel_admin, name='panel_admin'),
    path('panel-control/nuevo-profesor/', crear_profesor, name='crear_profesor'),
    path('panel-control/eliminar-usuario/<int:user_id>/', eliminar_usuario, name='eliminar_usuario'),
    path('panel-control/reset-password/<int:user_id>/', reset_password, name='reset_password'),
    path('panel-control/eliminar-contenido/<int:contenido_id>/', eliminar_contenido, name='eliminar_contenido'),
    path('paginas-interes/', paginas_interes, name='paginas_interes'),
]

# --- BLOQUE OBLIGATORIO PARA VER ARCHIVOS SUBIDOS ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)