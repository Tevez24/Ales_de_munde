from django.contrib import admin
from .models import (
    Paquete, Transporte, Actividad, Vuelos,
    Alojamiento, Alquiler, UserProfile,
    Carrito, ItemCarrito
)

class AdminCustomMixin:
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }   

# ------------------------------- ADMIN DE VUELOS -------------------------------
@admin.register(Vuelos)
class VuelosAdmin(admin.ModelAdmin):
    list_display = (
        'origen', 'destino', 'precio_por_persona', 'fecha_salida', 'horario_salida',
        'fecha_regreso', 'horario_regreso', 'clase', 'aerolinea', 'detalles',
        'duracion', 'escala'
    )
    list_filter = ('origen', 'destino', 'aerolinea', 'clase')
    search_fields = ('origen', 'destino', 'aerolinea')
    ordering = ('origen',)

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

# ------------------------------- ADMIN DE PAQUETES -------------------------------
@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'categoria', 'duracion', 'precio', 'descuento', 'oferta', 'reseña', 'activo','imagen')
    list_filter = ('tipo', 'categoria')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

# ------------------------------- ADMIN DE ALOJAMIENTOS -------------------------------
@admin.register(Alojamiento)
class AlojamientoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'destino', 'precio_por_persona', 'tipo',
        'capacidad', 'ubicacion', 'habitaciones', 'reseña',
        'entrada_salida', 'descuento', 'imagen'
    )
    list_filter = ('destino', 'tipo')
    search_fields = ('nombre', 'destino')

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

# ------------------------------- ADMIN DE ALQUILERES -------------------------------
@admin.register(Alquiler)
class AlquilerAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'destino', 'precio_por_noche', 'habitaciones',
        'baños', 'capacidad', 'descripcion', 'tipo_alquiler',
        'reseña', 'ubicacion', 'imagen'
    )
    list_filter = ('destino',)
    search_fields = ('nombre', 'destino')

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

# ------------------------------- ADMIN DE TRANSPORTE -------------------------------
@admin.register(Transporte)
class TransporteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'tipo', 'precio', 'capacidad', 'origen', 'destino',
        'descripcion', 'reseña', 'fecha_salida', 'hora_salida',
        'duracion', 'tipo_traslado', 'imagen'
    )
    list_filter = ('tipo',)
    search_fields = ('nombre', 'descripcion')

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

# ------------------------------- ADMIN DE ACTIVIDADES -------------------------------
@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'destino', 'ubicacion', 'precio_por_persona',
        'categoria', 'duracion', 'reseña', 'fecha', 'imagen'
    )
    list_filter = ('destino', 'categoria')
    search_fields = ('nombre', 'destino')

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

# ------------------------------- ADMIN DE USUARIOS (PERFIL) -------------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'telefono', 'pais', 'ciudad', 'direccion',
        'codigo_postal', 'fecha_nacimiento', 'genero', 'foto_perfil', 'fecha_creacion'
    )
    search_fields = ('user__username', 'user__email', 'telefono', 'pais', 'ciudad', 'direccion')
    list_filter = ('pais', 'genero')

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

# ------------------------------- ADMIN DE ITEMS DEL CARRITO -------------------------------
class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 1
    readonly_fields = ('subtotal',)

    def subtotal(self, obj):
        return obj.cantidad * obj.paquete.precio
    subtotal.short_description = 'Subtotal ($)'

# ------------------------------- ADMIN DE CARRITO -------------------------------
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'get_total')
    inlines = [ItemCarritoInline]
    readonly_fields = ('get_total',)
    search_fields = ('usuario__username',)

    def get_total(self, obj):
        total = sum([item.cantidad * item.paquete.precio for item in obj.itemcarrito_set.all()])
        return total
    get_total.short_description = 'Total ($)'

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
