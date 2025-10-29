from django.db import models
from django.contrib.auth.models import User


# -------------------------------
# MODELO DE VUELOS
# -------------------------------
class Vuelos(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    precio_por_persona = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_salida = models.DateField()
    horario_salida = models.TimeField()
    fecha_regreso = models.DateField()
    horario_regreso = models.TimeField()
    clase = models.CharField(max_length=50)
    aerolinea = models.CharField(max_length=100)
    detalles = models.TextField(blank=True)
    escala = models.CharField(max_length=100, blank=True, help_text="Ej: 1 escala en Lima")
    duracion = models.CharField(max_length=50, help_text="Duración total del vuelo")

    def __str__(self):
        return f"{self.origen} → {self.destino}"


# -------------------------------
# MODELO DE PAQUETES
# -------------------------------
class Paquete(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='paquetes/', blank=True, null=True)
    duracion = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Porcentaje de descuento")
    oferta = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True)
    reseña = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


# -------------------------------
# MODELO DE ALOJAMIENTO
# -------------------------------
class Alojamiento(models.Model):
    nombre = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    precio_por_persona = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50)
    capacidad = models.IntegerField()
    imagen = models.ImageField(upload_to='alojamientos/', blank=True, null=True)
    ubicacion = models.CharField(max_length=200)
    habitaciones = models.IntegerField(default=1)
    reseña = models.TextField(blank=True)
    entrada_salida = models.CharField(max_length=100, help_text="Ej: Check-in 14:00 / Check-out 10:00")
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Porcentaje de descuento")

    def __str__(self):
        return self.nombre


# -------------------------------
# MODELO DE ALQUILERES
# -------------------------------
class Alquiler(models.Model):
    nombre = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=2)
    habitaciones = models.IntegerField(default=1)
    imagen = models.ImageField(upload_to='alquileres/', blank=True, null=True)
    baños = models.IntegerField(default=1)
    capacidad = models.IntegerField()
    descripcion = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=200)
    tipo_alquiler = models.CharField(
        max_length=50,
        choices=[
            ('Casa', 'Casa'),
            ('Cabaña', 'Cabaña'),
            ('Departamento', 'Departamento'),
            ('Villa', 'Villa'),
            ('Loft', 'Loft'),
            ('Penthouse', 'Penthouse')
        ]
    )
    reseña = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


# -------------------------------
# MODELO DE TRANSPORTE
# -------------------------------
class Transporte(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad = models.IntegerField()
    imagen = models.ImageField(upload_to='transportes/', blank=True, null=True)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    reseña = models.TextField(blank=True)
    fecha_salida = models.DateField()
    hora_salida = models.TimeField()
    duracion = models.CharField(max_length=50)
    tipo_traslado = models.CharField(
        max_length=50,
        choices=[
            ('Desde aeropuerto', 'Desde aeropuerto'),
            ('Hacia aeropuerto', 'Hacia aeropuerto'),
            ('Traslado urbano', 'Traslado urbano')
        ]
    )

    def __str__(self):
        return self.nombre


# -------------------------------
# MODELO DE ACTIVIDADES
# -------------------------------
class Actividad(models.Model):
    nombre = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='actividades/', blank=True, null=True)
    precio_por_persona = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)
    duracion = models.CharField(max_length=50)
    reseña = models.TextField(blank=True)
    fecha = models.DateField()

    def __str__(self):
        return self.nombre


# -------------------------------
# MODELO DE PERFIL DE USUARIO
# -------------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)
    pais = models.CharField(max_length=50, blank=True)
    ciudad = models.CharField(max_length=50, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    codigo_postal = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=20, blank=True)
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# -------------------------------
# MODELOS DE CARRITO
# -------------------------------
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.paquete.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.paquete.nombre}"
