import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrito_project.settings')
django.setup()

from Carrito_app.models import Transporte

def load_transportes():
    # Elimina los transportes existentes para evitar duplicados
    Transporte.objects.all().delete()

    transportes = [
        {
            'nombre': 'Transfer Premium Aeropuerto',
            'descripcion': 'Auto Premium',
            'precio': 25.00,
            'imagen': 'transportes/transfer.jpg',
            'capacidad': 3,
            'tipo': 'Aeropuerto'
        },
        {
            'nombre': 'Minivan Familiar',
            'descripcion': 'Minivan',
            'precio': 35.00,
            'imagen': 'transportes/minivan.jpg',
            'capacidad': 7,
            'tipo': 'Aeropuerto'
        },
        {
            'nombre': 'Bus Turístico',
            'descripcion': 'Bus',
            'precio': 50.00,
            'imagen': 'transportes/bus.jpg',
            'capacidad': 20,
            'tipo': 'Urbano'
        }
    ]

    for t in transportes:
        Transporte.objects.create(
            nombre=t['nombre'],
            descripcion=t['descripcion'],
            precio=t['precio'],
            imagen=t['imagen'],
            capacidad=t['capacidad'],
            tipo=t['tipo']
        )

if __name__ == '__main__':
    load_transportes()
    print("Transportes cargados exitosamente!")
