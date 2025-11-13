# Carrito_app/admin.py
from django.contrib import admin
from .models import (
    Producto, Vuelos, Paquete, Alojamiento, Alquiler,
    Transporte, Actividad, UserProfile, Carrito, ItemCarrito, Compra
)

# REGISTRAR MODELOS
admin.site.register(Producto)
admin.site.register(Vuelos)
admin.site.register(Paquete)
admin.site.register(Alojamiento)
admin.site.register(Alquiler)
admin.site.register(Transporte)
admin.site.register(Actividad)
admin.site.register(UserProfile)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Compra)

# PERSONALIZACIÓN
admin.site.site_header = "AILES DU MUNDE"
admin.site.site_title = "Admin | Ailes du Monde"
admin.site.index_title = "Dashboard - Gestión Completa"
admin.site.enable_nav_sidebar = True