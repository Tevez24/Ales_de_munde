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
    imagen = models.CharField(max_length=200, help_text="Ruta a la imagen desde la carpeta static. Ej: Carrito_app/img/nombre_archivo.jpg")

    def __str__(self):
        return self.nombre
