
from django.core.management.base import BaseCommand
from Carrito_app.models import Paquete, Destino
import os

class Command(BaseCommand):
    help = 'Carga paquetes de viaje iniciales en la base de datos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando la carga de paquetes...'))

        # Limpiar datos antiguos para evitar duplicados
        Paquete.objects.all().delete()
        Destino.objects.all().delete()
        self.stdout.write(self.style.WARNING('Paquetes y Destinos existentes eliminados.'))

        # Lista de paquetes a crear
        paquetes_data = [
            {
                "nombre": "Europa Mágica",
                "descripcion": "Descubre el encanto de las capitales europeas. Un viaje por la historia, el arte y la gastronomía de ciudades como París, Roma y Praga.",
                "precio": 3000.00,
                "destino_nombre": "Europa",
                "imagen": "paquetes/europa_magica.jpg"
            },
            {
                "nombre": "Safari Fotográfico en Península Valdés",
                "descripcion": "Captura la majestuosidad de la fauna marina en su hábitat natural. Ballenas, pingüinos y lobos marinos te esperan.",
                "precio": 1800.00,
                "destino_nombre": "Península Valdés, Argentina",
                "imagen": "paquetes/safari_fotografico_peninsula_valdes.jpg"
            },
            {
                "nombre": "Aventura en los Alpes Suizos",
                "descripcion": "Ascenso al Matterhorn con guía experto, hotel 4 estrellas incluido y seguro de aventura.",
                "precio": 2850.00,
                "destino_nombre": "Alpes Suizos",
                "imagen": "paquetes/alpes_suizos.jpg"
            },
            {
                "nombre": "Maravillas de Islandia",
                "descripcion": "Auroras boreales garantizadas, visita a Blue Lagoon, cascadas espectaculares y transporte 4x4 incluido.",
                "precio": 1950.00,
                "destino_nombre": "Islandia",
                "imagen": "paquetes/maravillas_de_islandia.jpg"
            },
            {
                "nombre": "Safari Africano Premium",
                "descripcion": "Big Five garantizado, alojamientos en lodges de lujo, vuelos internos incluidos y guía naturalista profesional.",
                "precio": 4200.00,
                "destino_nombre": "África",
                "imagen": "paquetes/safari.jpg"
            },
            {
                "nombre": "Templos Místicos de Myanmar",
                "descripcion": "Bagan al amanecer, hoteles boutique, experiencias auténticas y crucero por el río Irrawaddy.",
                "precio": 1680.00,
                "destino_nombre": "Myanmar",
                "imagen": "paquetes/Templos Místicos de Myanmar.jpg"
            },
            {
                "nombre": "Patagonia Salvaje",
                "descripcion": "Torres del Paine, Glaciar Perito Moreno, trekking guiado y refugios de montaña.",
                "precio": 3100.00,
                "destino_nombre": "Patagonia, Argentina",
                "imagen": "paquetes/patagonia salvaje.jpg"
            },
            {
                "nombre": "Escapada Tropical Maldivas",
                "descripcion": "Villa sobre el agua, todo incluido premium, spa de lujo y deportes acuáticos.",
                "precio": 5200.00,
                "destino_nombre": "Maldivas",
                "imagen": "paquetes/escapada_tropical_maldivas.jpg"
            },
            {
                "nombre": "Cataratas de Iguazú",
                "descripcion": "Lado argentino y brasileño, hotel frente a las cataratas, senderos ecológicos y fauna autóctona.",
                "precio": 850.00,
                "destino_nombre": "Iguazú, Argentina",
                "imagen": "paquetes/cataratas_de_iguazu.jpg"
            },
            {
                "nombre": "Mendoza y la Ruta del Vino",
                "descripcion": "Degustación de vinos, tour por bodegas premium, vista de los Andes y gastronomía regional.",
                "precio": 1200.00,
                "destino_nombre": "Mendoza, Argentina",
                "imagen": "paquetes/ruta del vino.jpg"
            },
            {
                "nombre": "Tesoros de Japón",
                "descripcion": "Explora la fascinante cultura japonesa, desde los templos de Kioto hasta la modernidad de Tokio. Sumérgete en la belleza de sus jardines, la deliciosa gastronomía y la calidez de su gente.",
                "precio": 3500.00,
                "destino_nombre": "Japón",
                "imagen": "paquetes/tesoros_de_japon.jpg"
            },
            {
                "nombre": "Playas de Tailandia",
                "descripcion": "Relájate en las playas de Phuket, explora las islas Phi Phi y disfruta de la vibrante vida nocturna de Bangkok.",
                "precio": 2200.00,
                "destino_nombre": "Tailandia",
                "imagen": "paquetes/playas_tailandia.jpg"
            },
            {
                "nombre": "Aventura en Costa Rica",
                "descripcion": "Descubre la pura vida en Costa Rica. Selvas tropicales, volcanes y playas paradisíacas te esperan en esta aventura inolvidable.",
                "precio": 1900.00,
                "destino_nombre": "Costa Rica",
                "imagen": "paquetes/aventura_costa_rica.jpg"
            }
        ]

        # Crear los paquetes
        for paquete_info in paquetes_data:
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
