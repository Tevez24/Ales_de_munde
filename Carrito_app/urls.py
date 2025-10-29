from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    # ==================== PÁGINA PRINCIPAL ====================
    path('', views.inicio, name='inicio'),
    path('home/', views.home, name='home'),


    # ==================== PAQUETES Y PRODUCTOS ====================
    path('paquetes/', views.paquetes, name='paquetes'),
    path('paquete/<int:paquete_id>/', views.paquete_detalle, name='paquete_detalle'),
    path('vuelos/', views.vuelos, name='vuelos'),
    path('actividades/', views.actividades, name='actividades'),
    path('alojamiento/', views.alojamiento, name='alojamiento'),
    path('alquileres/', views.alquileres, name='alquileres'),
    path('transporte/', views.transporte, name='transporte'),

    # ==================== CARRITO ====================
    path('carrito/', views.carrito, name='carrito'),
    path('add_to_cart/<int:paquete_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # ==================== PAGOS ====================
    path('pago/', views.pago, name='pago'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('medios_pago/', views.medios_pago, name='medios_pago'),

    # ==================== AUTENTICACIÓN ====================
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ==================== PERFIL USUARIO ====================
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('order_history/', views.order_history, name='order_history'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='Carrito_app/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='Carrito_app/password_change_done.html'), name='password_change_done'),

    # ==================== PÁGINAS INFORMACIÓN ====================
    path('acerca/', views.acerca, name='acerca'),
    path('contacto/', views.contacto, name='contacto'),
    path('preguntas_frecuentes/', views.preguntas_frecuentes, name='preguntas_frecuentes'),
    path('support/', views.support, name='support'),  # Fixed typo 'supprt'

    # ==================== LEGALES ====================
    path('arrepentimiento/', views.arrepentimiento, name='arrepentimiento'),
    path('defensa_consumidor/', views.defensa_consumidor, name='defensa_consumidor'),
    path('termino_condiciones/', views.termino_condiciones, name='termino_condiciones'),

    # ==================== TEMPLATES ESTÁTICOS ====================
    path('politica_arrepentimiento/', TemplateView.as_view(template_name='Carrito_app/politica_arrepentimiento.html'), name='politica_arrepentimiento'),
    path('politica_reembolso/', TemplateView.as_view(template_name='Carrito_app/politica_reembolso.html'), name='politica_reembolso'),
    path('politica_cookies/', TemplateView.as_view(template_name='Carrito_app/politica_cookies.html'), name='politica_cookies'),
    path('politica_datos_personales/', TemplateView.as_view(template_name='Carrito_app/politica_datos_personales.html'), name='politica_datos_personales'),
    path('terminos_uso/', TemplateView.as_view(template_name='Carrito_app/terminos_uso.html'), name='terminos_uso'),
    path('eliminacion_datos_personales/', TemplateView.as_view(template_name='Carrito_app/eliminacion_datos_personales.html'), name='eliminacion_datos_personales'),
    path('politica_seguridad/', TemplateView.as_view(template_name='Carrito_app/politica_seguridad.html'), name='politica_seguridad'),
    path('politica_privacidad/', TemplateView.as_view(template_name='Carrito_app/politica_privacidad.html'), name='politica_privacidad'),
]