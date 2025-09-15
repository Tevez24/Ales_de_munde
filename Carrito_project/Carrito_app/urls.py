from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('home/', views.home, name='home'),
    path('paquetes/', views.paquetes, name='paquetes'),
    path('vuelos/', views.vuelos, name='vuelos'),
    path('carrito/', views.carrito, name='carrito'),
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
