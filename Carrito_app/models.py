from django.db import models
from django.contrib.auth.models import User





# Crea un modelo real (ejemplo: Producto)
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    en_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Productos"

# -------------------------------
# MODELO DE VUELOS
# -------------------------------
class Vuelos(models.Model):
    REGION_CHOICES = [
        ('Sudamérica', 'Sudamérica'),
        ('Europa', 'Europa'),
        ('Norteamérica', 'Norteamérica'),
        ('Medio Oriente', 'Medio Oriente'),
        ('Centroamérica', 'Centroamérica'),
        ('Asia', 'Asia'),
        ('África', 'África'),
    ]

    CLASE_CHOICES = [
        ('Económica', 'Económica'),
        ('Premium Económica', 'Premium Económica'),
        ('Business', 'Business'),
        ('Primera Clase', 'Primera Clase'),
    ]

    AEROLINEA_CHOICES = [
        ('Aerolíneas Argentinas', 'Aerolíneas Argentinas'),
        ('LATAM Airlines', 'LATAM Airlines'),
        ('Emirates', 'Emirates'),
        ('Lufthansa', 'Lufthansa'),
        ('Iberia', 'Iberia'),
        ('Qatar Airways', 'Qatar Airways'),
        ('Air France', 'Air France'),
        ('KLM', 'KLM'),
        ('Turkish Airlines', 'Turkish Airlines'),
        ('United Airlines', 'United Airlines'),
        ('British Airways', 'British Airways'),
        ('Copa Airlines', 'Copa Airlines'),
        ('Delta Air Lines', 'Delta Air Lines'),
        ('American Airlines', 'American Airlines'),
        ('Swiss Air', 'Swiss Air'),
        ('Alitalia', 'Alitalia'),
        ('Air Canada', 'Air Canada'),
        ('Air Europa', 'Air Europa'),
        ('Etihad Airways', 'Etihad Airways'),
        ('Ethiopian Airlines', 'Ethiopian Airlines'),
        ('Singapore Airlines', 'Singapore Airlines'),
        ('ANA Japan', 'ANA Japan'),
        ('Thai Airways', 'Thai Airways'),
        ('EVA Air', 'EVA Air'),
        ('South African Airways', 'South African Airways'),
        ('Finnair', 'Finnair'),
        ('Virgin Atlantic', 'Virgin Atlantic'),
    ]

    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    region = models.CharField(max_length=50, choices=REGION_CHOICES, default='Sudamérica')
    precio_por_persona = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_salida = models.DateField()
    horario_salida = models.TimeField()
    fecha_regreso = models.DateField()
    horario_regreso = models.TimeField()
    clase = models.CharField(max_length=50, choices=CLASE_CHOICES, default='Económica')
    aerolinea = models.CharField(max_length=100, choices=AEROLINEA_CHOICES, default='Aerolíneas Argentinas')
    detalles = models.TextField(blank=True)
    escala = models.CharField(max_length=100, blank=True, help_text="Ej: 1 escala en Lima")
    duracion = models.CharField(max_length=50, help_text="Duración total del vuelo")

    def __str__(self):
        return f"{self.origen} → {self.destino}"


# -------------------------------
# MODELO DE PAQUETES
# -------------------------------
class Paquete(models.Model):
    TIPO_CHOICES = [
        ('Nacional', 'Nacional'),
        ('Internacional', 'Internacional'),
    ]

    CATEGORIA_CHOICES = [
        ('Familiares', 'Familiares'),
        ('Grupales', 'Grupales'),
        ('Luna de miel', 'Luna de miel'),
        ('Aventura', 'Aventura'),
        ('Culturales', 'Culturales'),
        ('Relax', 'Relax'),
        ('Spa', 'Spa'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default='Nacional')
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='Familiares')
    imagen = models.ImageField(upload_to='paquetes/', blank=True, null=True)
    duracion = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    oferta = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    destino = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


# -------------------------------
# MODELO DE ALOJAMIENTO
# -------------------------------
class Alojamiento(models.Model):
    TIPO_CHOICES = [
        ('Hotel', 'Hotel'),
        ('Hostel', 'Hostel'),
        ('Resort', 'Resort'),
        ('Apartamento', 'Apartamento'),
    ]

    nombre = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='alojamientos/', blank=True, null=True)
    precio_por_persona = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default='Hotel')
    
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=200)
    habitaciones = models.IntegerField(default=1)
    entrada_salida = models.CharField(max_length=100, help_text="Ej: Check-in 14:00 / Check-out 10:00")
    

    def __str__(self):
        return self.nombre


# -------------------------------
# MODELO DE ALQUILERES
# -------------------------------
class Alquiler(models.Model):
    TIPO_ALQUILER_CHOICES = [
        ('Casa', 'Casa'),
        ('Departamento', 'Departamento'),
        ('Cabaña', 'Cabaña'),
        ('Villa', 'Villa'),
        ('Loft', 'Loft'),
    ]

    nombre = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='alquileres/', blank=True, null=True)
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=2)
    habitaciones = models.IntegerField(default=1)
    baños = models.IntegerField(default=1)
    capacidad = models.IntegerField()
    descripcion = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    tipo_alquiler = models.CharField(max_length=50, choices=TIPO_ALQUILER_CHOICES, default='Casa')

    def __str__(self):
        return self.nombre


# -------------------------------
# MODELO DE TRANSPORTE
# -------------------------------
class Transporte(models.Model):
    TIPO_CHOICES = [
        ('Auto', 'Auto'),
        ('Auto Premium', 'Auto Premium'),
        ('Mini Van', 'Mini Van'),
        ('Bus', 'Bus'),
        ('Van', 'Van'),
        ('Limusina', 'Limusina'),
        ('Bicicleta', 'Bicicleta'),
        ('Yate', 'Yate'),
        ('Helicóptero', 'Helicóptero'),
        ('Scouter', 'Scouter'),
        ('Tren', 'Tren'),
    
    ]

    TIPO_TRASLADO_CHOICES = [
        ('Desde aeropuerto', 'Desde aeropuerto'),
        ('Hacia aeropuerto', 'Hacia aeropuerto'),
        ('Traslado urbano', 'Traslado urbano'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default='Auto')
    imagen = models.ImageField(upload_to='transportes/', blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad = models.IntegerField()
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_salida = models.DateField()
    hora_salida = models.TimeField()
    duracion = models.CharField(max_length=50)
    tipo_traslado = models.CharField(max_length=50, choices=TIPO_TRASLADO_CHOICES, default='Traslado urbano')

    def __str__(self):
        return self.nombre


# -------------------------------
# MODELO DE ACTIVIDADES
# -------------------------------
class Actividad(models.Model):
    CATEGORIA_CHOICES = [
        ('Aventura', 'Aventura'),
        ('Gastronomía', 'Gastronomía'),
        ('Relajación', 'Relajación'),
        ('Culturales', 'Culturales'),
        ('Naturales', 'Naturales'),
    ]

    nombre = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio_por_persona = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='Aventura')
    duracion = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='actividades/', blank=True, null=True)
    dias_disponibles = models.CharField(max_length=100, help_text="Ej: Lunes, Martes, Miércoles, Jueves, Viernes")
    hora = models.TimeField()
    fecha = models.DateField()

    @property
    def precio(self):
        return self.precio_por_persona

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

class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    



    metodo_pago = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Compra #{self.id} - {self.usuario.username}"


# -------------------------------
# MODELOS DE CARRITO
# -------------------------------
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    paquetes = models.ManyToManyField('Paquete', blank=True)
    alojamientos = models.ManyToManyField('Alojamiento', blank=True)
    vuelos = models.ManyToManyField('Vuelos', blank=True)
    alquileres = models.ManyToManyField('Alquiler', blank=True)
    transportes = models.ManyToManyField('Transporte', blank=True)
    actividades = models.ManyToManyField('Actividad', blank=True)
    creado = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    def get_total(self):
        total = 0
        total += sum([p.precio for p in self.paquetes.all()])
        total += sum([a.precio for a in self.alojamientos.all()])
        total += sum([v.precio for v in self.vuelos.all()])
        total += sum([al.precio for al in self.alquileres.all()])
        total += sum([t.precio for t in self.transportes.all()])
        total += sum([act.precio for act in self.actividades.all()])
        return total


class ItemCarrito(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE)
    paquete = models.ForeignKey('Paquete', on_delete=models.CASCADE, null=True, blank=True)
    vuelo = models.ForeignKey('Vuelos', on_delete=models.CASCADE, null=True, blank=True)
    alojamiento = models.ForeignKey('Alojamiento', on_delete=models.CASCADE, null=True, blank=True)
    alquiler = models.ForeignKey('Alquiler', on_delete=models.CASCADE, null=True, blank=True)
    transporte = models.ForeignKey('Transporte', on_delete=models.CASCADE, null=True, blank=True)
    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    
    def subtotal(self):
        producto = (
            self.paquete or self.vuelo or self.alojamiento or
            self.alquiler or self.transporte or self.actividad 
            
        )
        if not producto:
            return 0

        if hasattr(producto, 'precio'):
            return producto.precio * self.cantidad
        elif hasattr(producto, 'precio_por_persona'):
            return producto.precio_por_persona * self.cantidad
        elif hasattr(producto, 'precio_por_noche'):
            return producto.precio_por_noche * self.cantidad
        elif hasattr(producto, 'precio_por_pasaje'):
            return producto.precio_por_pasaje * self.cantidad
        else:
            return 0

    def __str__(self):
        producto = (
            self.paquete or self.vuelo or self.alojamiento or
            self.alquiler or self.transporte or self.actividad
        )
        return f"{producto} x {self.cantidad}"

    @property
    def get_producto(self):
        return self.paquete or self.vuelo or self.actividad or self.alojamiento or self.alquiler or self.transporte 
