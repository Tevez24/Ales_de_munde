from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    # Página de inicio principal del sitio
    path('', views.inicio, name='inicio'), 
    path('home/', views.home, name='home'),

    # Páginas de contenido y productos
    path('paquetes/', views.paquetes, name='paquetes'),
    path('paquete/<int:paquete_id>/', views.paquete_detalle, name='paquete_detalle'), 
    path('vuelos/', views.vuelos, name='vuelos'),
    path('actividades/', views.actividades, name='actividades'),
    path('alojamiento/', views.alojamiento, name='alojamiento'),
    path('alquileres/', views.alquileres, name='alquileres'),
    path('medios_pago/', views.medios_pago, name='medios_pago'),
    path('transporte/', views.transporte, name='transporte'),
    path('transporte/<int:transporte_id>/', views.transporte_detalle, name='transporte_detalle'),
    path('arrepentimiento/', views.arrepentimiento, name='arrepentimiento'),
    path('acerca/', views.acerca, name='acerca'),
    path('contacto/', views.contacto, name='contacto'),
    path('pago/', views.pago, name='pago'),
    path('preguntas_frecuentes/', views.preguntas_frecuentes, name='preguntas_frecuentes'),
    path('support/', views.support, name='support'),

    path('termino_condiciones/', TemplateView.as_view(template_name='Carrito_app/termino_condiciones.html'), name='termino_condiciones'),
    path('politica_privacidad/', TemplateView.as_view(template_name='Carrito_app/politica_privacidad.html'), name='politica_privacidad'),

    # Vistas del Carrito
    path('carrito/', views.carrito, name='carrito'),
    path('add_to_cart/<int:paquete_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_cart/<int:paquete_id>/', views.update_cart, name='update_cart'), 

    # Vistas de Autenticación y Registro
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Vistas de Perfil de Usuario
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('order_history/', views.order_history, name='order_history'),

    # Cambio de contraseña con Django
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
]
