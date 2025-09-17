from django.urls import path
from . import views

urlpatterns = [
    # La página de paquetes ahora es la página de inicio principal del sitio
    path('', views.inicio, name='inicio'), 

    # Página del panel de usuario (cuando ya ha iniciado sesión)
    path('home/', views.home, name='home'),

    # Páginas de contenido y productos
    path('paquetes/', views.paquetes, name='paquetes'),
    path('paquete/<int:paquete_id>/', views.paquete_detalle, name='paquete_detalle'), 
    path('vuelos/', views.vuelos, name='vuelos'),
    path('actividades/', views.actividades, name='actividades'),
    path('alojamiento/', views.alojamiento, name='alojamiento'),
    path('alquileres/', views.alquileres, name='alquileres'),
    path('transporte/', views.transporte, name='transporte'),
    path('transporte/<int:transporte_id>/', views.transporte_detalle, name='transporte_detalle'),
    path('arrepentimiento/', views.arrepentimiento, name='arrepentimiento'),
    path('acerca/', views.acerca, name='acerca'),
    path('contacto/', views.contacto, name='contacto'),

    # Vistas del Carrito
    path('carrito/', views.carrito, name='carrito'),
    path('add_to_cart/<int:paquete_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # Vistas de Autenticación
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]