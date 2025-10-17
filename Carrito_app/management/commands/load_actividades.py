
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
            # Destinos de las nuevas actividades
            destino_mendoza, _ = Destino.objects.get_or_create(nombre='Mendoza, Argentina')
            destino_calafate, _ = Destino.objects.get_or_create(nombre='El Calafate, Argentina')
            destino_puerto_madryn, _ = Destino.objects.get_or_create(nombre='Puerto Madryn, Argentina')
            destino_queenstown, _ = Destino.objects.get_or_create(nombre='Queenstown, Nueva Zelanda')
            destino_santorini, _ = Destino.objects.get_or_create(nombre='Santorini, Grecia')
            destino_cusco, _ = Destino.objects.get_or_create(nombre='Cusco, Perú')
            destino_bangkok, _ = Destino.objects.get_or_create(nombre='Bangkok, Tailandia')
            destino_geiranger, _ = Destino.objects.get_or_create(nombre='Geiranger, Noruega')
            destino_marrakech, _ = Destino.objects.get_or_create(nombre='Marrakech, Marruecos')
            destino_merzouga, _ = Destino.objects.get_or_create(nombre='Merzouga, Marruecos')

            actividades = [
                {
                    'nombre': 'Tour de Vinos en Mendoza',
                    'destino': destino_mendoza,
                    'descripcion': 'Un tour para degustar los mejores vinos de la región.',
                    'precio': Decimal('60.00'),
                    'imagen': 'actividades/tour_vinos_mendoza.jpg'
                },
                {
                    'nombre': 'Trekking Glaciar Perito Moreno',
                    'destino': destino_calafate,
                    'descripcion': 'Una caminata inolvidable sobre el famoso glaciar.',
                    'precio': Decimal('150.00'),
                    'imagen': 'actividades/trekking_perito_moreno.jpg'
                },
                {
                    'nombre': 'Safari Fotográfico Península Valdés',
                    'destino': destino_puerto_madryn,
                    'descripcion': 'Avistaje de ballenas y fauna marina en un entorno único.',
                    'precio': Decimal('120.00'),
                    'imagen': 'actividades/safari_peninsula_valdes.jpg'
                },
                {
                    'nombre': 'Bungee Jump Kawarau',
                    'destino': destino_queenstown,
                    'descripcion': 'Salto en bungee desde el histórico puente Kawarau.',
                    'precio': Decimal('180.00'),
                    'imagen': 'actividades/bungee_kawarau.jpg'
                },
                {
                    'nombre': 'Tour en Catamaran Santorini',
                    'destino': destino_santorini,
                    'descripcion': 'Navega por la caldera y disfruta de las vistas icónicas.',
                    'precio': Decimal('110.00'),
                    'imagen': 'actividades/catamaran_santorini.jpg'
                },
                {
                    'nombre': 'Trekking Camino Inca',
                    'destino': destino_cusco,
                    'descripcion': 'Una caminata histórica hacia Machu Picchu.',
                    'precio': Decimal('250.00'),
                    'imagen': 'actividades/camino_inca.jpg'
                },
                {
                    'nombre': 'Curso de Cocina Tailandesa',
                    'destino': destino_bangkok,
                    'descripcion': 'Aprende los secretos de la auténtica cocina tailandesa.',
                    'precio': Decimal('90.00'),
                    'imagen': 'actividades/cocina_tailandesa.jpg'
                },
                {
                    'nombre': 'Crucero por Geirangerfjord',
                    'destino': destino_geiranger,
                    'descripcion': 'Navega por uno de los fiordos más famosos del mundo.',
                    'precio': Decimal('140.00'),
                    'imagen': 'actividades/crucero_geirangerfjord.jpg'
                },
                {
                    'nombre': 'Paseo en Camello por el Sahara',
                    'destino': destino_marrakech,
                    'descripcion': 'Una aventura en camello por las dunas del desierto.',
                    'precio': Decimal('85.00'),
                    'imagen': 'actividades/paseo_sahara.jpg'
                },
                {
                    'nombre': 'Safari en el Desierto del Sahara',
                    'destino': destino_merzouga,
                    'descripcion': 'Explora las dunas de Merzouga en un 4x4.',
                    'precio': Decimal('220.00'),
                    'imagen': 'actividades/safari_sahara.jpg'
                }
            ]

            for actividad_data in actividades:
                Actividad.objects.create(**actividad_data)

            self.stdout.write(self.style.SUCCESS(f'Se crearon {len(actividades)} actividades de muestra.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocurrió un error inesperado: {str(e)}'))
