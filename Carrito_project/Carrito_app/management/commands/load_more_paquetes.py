
from django.core.management.base import BaseCommand
from Carrito_app.models import Paquete, Destino

class Command(BaseCommand):
    help = 'Carga paquetes de viaje adicionales en la base de datos con los nombres de archivo correctos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando la carga de paquetes con nombres de imagen corregidos...'))

        # Limpia los paquetes existentes para evitar duplicados
        Paquete.objects.all().delete()
        Destino.objects.all().delete()
        self.stdout.write(self.style.WARNING('Paquetes y destinos existentes eliminados para una carga limpia.'))

        paquetes_adicionales = [
            {
                "nombre": "Aventura Patagónica",
                "descripcion": "Un viaje inolvidable a la Patagonia, con paisajes que te dejarán sin aliento.",
                "precio": 2500.00,
                "destino_nombre": "Patagonia, Argentina",
                "imagen": "paquetes/aventura patagonica.jpg"
            },
            {
                "nombre": "Caribe Paradisíaco",
                "descripcion": "Relájate en las playas de arena blanca y aguas cristalinas del Caribe.",
                "precio": 3800.00,
                "destino_nombre": "Caribe",
                "imagen": "paquetes/caribe paradisiaco.jpg"
            },
            {
                "nombre": "Cabaña en Bariloche",
                "descripcion": "Disfruta de la nieve y los hermosos paisajes de Bariloche en una acogedora cabaña.",
                "precio": 1200.00,
                "destino_nombre": "Bariloche, Argentina",
                "imagen": "paquetes/cabana_en_bariloche.jpg"
            },
            {
                "nombre": "Casa de Playa",
                "descripcion": "Escápate a una hermosa casa de playa y disfruta del sol y el mar.",
                "precio": 4500.00,
                "destino_nombre": "Costa",
                "imagen": "paquetes/casa de playa.jpg"
            },
            {
                "nombre": "Departamento en Mendoza",
                "descripcion": "Descubre la capital del vino y disfruta de la cordillera de los Andes.",
                "precio": 900.00,
                "destino_nombre": "Mendoza, Argentina",
                "imagen": "paquetes/departamento Centro Mendoza.jpg"
            },
            {
                "nombre": "Hotel Boutique en Palermo",
                "descripcion": "Disfruta de la vibrante vida de Buenos Aires en un hotel con todas las comodidades.",
                "precio": 1500.00,
                "destino_nombre": "Buenos Aires, Argentina",
                "imagen": "paquetes/hotel_boutique_palermo.jpg"
            },
            {
                "nombre": "Resort & Spa en Mendoza",
                "descripcion": "Relájate y disfruta de los mejores vinos en un resort de lujo.",
                "precio": 5500.00,
                "destino_nombre": "Mendoza, Argentina",
                "imagen": "paquetes/resort_and_spa_mendoza.jpg"
            },
            {
                "nombre": "Backpackers Hostel",
                "descripcion": "La opción ideal para los viajeros que buscan aventura y conocer gente nueva.",
                "precio": 500.00,
                "destino_nombre": "Mochileros",
                "imagen": "paquetes/backpackers hostel.jpg"
            }
        ]

        for paquete_info in paquetes_adicionales:
            destino, created = Destino.objects.get_or_create(nombre=paquete_info["destino_nombre"])
            if created:
                self.stdout.write(self.style.SUCCESS(f"Destino '{destino.nombre}' creado."))

            Paquete.objects.create(
                nombre=paquete_info["nombre"],
                destino=destino,
                descripcion=paquete_info["descripcion"],
                precio=paquete_info["precio"],
                imagen=paquete_info["imagen"],
            )
            self.stdout.write(f"Paquete '{paquete_info['nombre']}' creado.")

        self.stdout.write(self.style.SUCCESS('\n¡Carga de paquetes completada con éxito!'))
