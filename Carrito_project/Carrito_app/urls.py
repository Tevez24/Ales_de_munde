from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('home/', views.home, name='home'),
    path('paquetes/', views.paquetes, name='paquetes'),
    path('paquete/<int:paquete_id>/', views.paquete_detalle, name='paquete_detalle'), 
    path('vuelos/', views.vuelos, name='vuelos'),
    path('carrito/', views.carrito, name='carrito'),
    path('add_to_cart/<int:paquete_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('actividades/', views.actividades, name='actividades'),
    path('alojamiento/', views.alojamiento, name='alojamiento'),
    path('alquileres/', views.alquileres, name='alquileres'),
    path('transporte/', views.transporte, name='transporte'),
    path('arrepentimiento/', views.arrepentimiento, name='arrepentimiento'),
    path('acerca/', views.acerca, name='acerca'),
    path('contacto/', views.contacto, name='contacto'),
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
