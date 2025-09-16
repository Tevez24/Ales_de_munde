
import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrito_project.settings')
django.setup()

from Carrito_app.models import Paquete, Destino

def run():
    # Limpiar datos antiguos para evitar duplicados
    Paquete.objects.all().delete()
    Destino.objects.all().delete()
    print("Paquetes y Destinos existentes eliminados.")

    # Lista de paquetes a crear
    paquetes_data = [
        {
            "nombre": "Aventura Patagónica",
            "descripcion": "Explora los confines de la tierra en esta épica aventura por la Patagonia. Incluye trekking, navegación por glaciares y avistamiento de fauna.",
            "precio": 2500.00,
            "destino_nombre": "Patagonia, Argentina",
            "imagen": "paquetes/aventura_patagonica.jpg"
        },
        {
            "nombre": "Escapada Tropical a Maldivas",
            "descripcion": "Relájate en las playas de arena blanca y aguas cristalinas de las Maldivas. Un paraíso para los amantes del sol y el buceo.",
            "precio": 3500.00,
            "destino_nombre": "Maldivas",
            "imagen": "paquetes/escapada_tropical_maldivas.jpg"
        },
        {
            "nombre": "Europa Mágica",
            "descripcion": "Descubre el encanto de las capitales europeas. Un viaje por la historia, el arte y la gastronomía de ciudades como París, Roma y Praga.",
            "precio": 3000.00,
            "destino_nombre": "Europa",
            "imagen": "paquetes/europa_magica.jpg"
        },
        {
            "nombre": "Maravillas de Islandia",
            "descripcion": "Contempla auroras boreales, géiseres y volcanes en la tierra de hielo y fuego. Una experiencia natural que nunca olvidarás.",
            "precio": 2800.00,
            "destino_nombre": "Islandia",
            "imagen": "paquetes/maravillas_de_islandia.jpg"
        },
        {
            "nombre": "Safari Fotográfico en Península Valdés",
            "descripcion": "Captura la majestuosidad de la fauna marina en su hábitat natural. Ballenas, pingüinos y lobos marinos te esperan.",
            "precio": 1800.00,
            "destino_nombre": "Península Valdés, Argentina",
            "imagen": "paquetes/safari_fotografico_peninsula_valdes.jpg"
        },
        {
            "nombre": "Cataratas del Iguazú",
            "descripcion": "Siente la fuerza de una de las maravillas naturales del mundo. Un espectáculo de agua y selva que te dejará sin aliento.",
            "precio": 1200.00,
            "destino_nombre": "Iguazú, Argentina",
            "imagen": "paquetes/cataratas_de_iguazu.jpg"
        }
    ]

    # Crear los paquetes
    for paquete_info in paquetes_data:
        # Obtener o crear el objeto Destino
        destino, created = Destino.objects.get_or_create(nombre=paquete_info["destino_nombre"])
        if created:
            print(f"Destino '{destino.nombre}' creado.")

        # Crear el Paquete y asociarlo con el Destino
        Paquete.objects.create(
            nombre=paquete_info["nombre"],
            destino=destino,
            descripcion=paquete_info["descripcion"],
            precio=paquete_info["precio"],
            imagen=paquete_info["imagen"],
        )
        print(f"Paquete '{paquete_info['nombre']}' creado.")

    print("\n¡Carga de paquetes completada con éxito!")

if __name__ == "__main__":
    run()
