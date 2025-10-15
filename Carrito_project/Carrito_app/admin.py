from django.contrib import admin
from .models import Paquete, Transporte, Actividad, Destino, UserProfile

admin.site.register(Paquete)
admin.site.register(Transporte)
admin.site.register(Actividad)
admin.site.register(Destino)
admin.site.register(UserProfile)
