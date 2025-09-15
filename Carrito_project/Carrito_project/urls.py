from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Carrito_app.urls')),  # 👈 carga todas las rutas de la app
]
