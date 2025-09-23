
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from Carrito_app.models import Actividad, Destino
from decimal import Decimal

class Command(BaseCommand):
    help = 'Carga datos de muestra de actividades en la base de datos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Eliminando datos de actividades existentes...'))
        Actividad.objects.all().delete()

        # Asegurarse de que el directorio para las imágenes de actividades existe
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'actividades'), exist_ok=True)

        self.stdout.write(self.style.SUCCESS('Creando nuevas actividades...'))

        try:
            # Intentamos obtener los destinos, o crearlos si no existen
            destino_playa, _ = Destino.objects.get_or_create(nombre='Playa del Carmen')
            destino_tulum, _ = Destino.objects.get_or_create(nombre='Tulum')
            destino_cancun, _ = Destino.objects.get_or_create(nombre='Cancún')

            actividades = [
                {
                    'nombre': 'Snorkel en Cenote Dos Ojos',
                    'destino': destino_tulum,
                    'descripcion': 'Explora las cavernas inundadas de uno de los cenotes más famosos del mundo. Ideal para nadadores de todos los niveles.',
                    'precio': Decimal('75.00'),
                    'imagen': 'actividades/snorkel_cenote.jpg'
                },
                {
                    'nombre': 'Visita a las Ruinas de Tulum',
                    'destino': destino_tulum,
                    'descripcion': 'Recorrido guiado por la antigua ciudad maya amurallada con vistas espectaculares al mar Caribe.',
                    'precio': Decimal('50.00'),
                    'imagen': 'actividades/ruinas_tulum.jpg'
                },
                {
                    'nombre': 'Paseo en Catamarán a Isla Mujeres',
                    'destino': destino_cancun,
                    'descripcion': 'Un día completo de navegación, snorkel en el arrecife El Meco y relajación en la playa de Isla Mujeres. Incluye almuerzo y barra libre.',
                    'precio': Decimal('120.00'),
                    'imagen': 'actividades/catamaran_isla_mujeres.jpg'
                },
                {
                    'nombre': 'Nado con Tiburón Ballena',
                    'destino': destino_cancun,
                    'descripcion': 'Una experiencia única en la vida para nadar junto al pez más grande del mundo en su hábitat natural (solo en temporada).',
                    'precio': Decimal('190.00'),
                    'imagen': 'actividades/tiburon_ballena.jpg'
                },
                {
                    'nombre': 'Excursión a Xcaret',
                    'destino': destino_playa,
                    'descripcion': 'Disfruta de más de 50 atracciones naturales y culturales. Ríos subterráneos, espectáculos y fauna local en un solo lugar.',
                    'precio': Decimal('150.00'),
                    'imagen': 'actividades/xcaret.jpg'
                },
                {
                    'nombre': 'Coco Bongo Show & Disco',
                    'destino': destino_playa,
                    'descripcion': 'Vive una noche de fiesta inolvidable con espectáculos acrobáticos, imitaciones de artistas y la mejor música.',
                    'precio': Decimal('90.00'),
                    'imagen': 'actividades/coco_bongo.jpg'
                }
            ]

            for actividad_data in actividades:
                Actividad.objects.create(**actividad_data)

            self.stdout.write(self.style.SUCCESS(f'Se crearon {len(actividades)} actividades de muestra.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocurrió un error inesperado: {str(e)}'))
