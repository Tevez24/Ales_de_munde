from django.db import models

class Destino(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class Paquete(models.Model):
    nombre = models.CharField(max_length=100)
    destino = models.ForeignKey(Destino, on_delete=models.CASCADE, related_name='paquetes')
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='paquetes/')

    def __str__(self):
        return self.nombre

class Transporte(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='transportes/')
    capacidad = models.IntegerField()
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    nombre = models.CharField(max_length=100)
    destino = models.ForeignKey(Destino, on_delete=models.CASCADE, related_name='actividades')
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='actividades/')
    fecha = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre
