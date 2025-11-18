from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
from io import BytesIO
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import random

import logging

from Carrito_app.models import (
    Paquete, UserProfile, Carrito, ItemCarrito, Vuelos, 
    Alojamiento, Alquiler, Transporte, Actividad, Compra
)
from .forms import RegisterForm

# Configuración de logs
logger = logging.getLogger(__name__)



def custom_admin_view(request):
    return render(request, 'admin/custom_admin.html')
def index(request):
    return render(request, 'admin/index.html')





# ------------------ PÁGINAS PRINCIPALES ------------------

def home(request):
    return render(request, 'Carrito_app/home.html')

def inicio(request):
    paquetes = Paquete.objects.filter(activo=True)[:4]
    logger.debug(f"Paquetes cargados en inicio: {paquetes}")
    return render(request, 'Carrito_app/inicio.html', {'paquetes': paquetes})

def vuelos(request):
    vuelos = Vuelos.objects.all()

    # Filtros básicos
    if request.GET.get('origen'):
        vuelos = vuelos.filter(origen__icontains=request.GET['origen'])
    if request.GET.get('destino'):
        vuelos = vuelos.filter(destino__icontains=request.GET['destino'])
    if request.GET.get('fecha_salida'):
        vuelos = vuelos.filter(fecha_salida=request.GET['fecha_salida'])
    if request.GET.get('fecha_regreso'):
        vuelos = vuelos.filter(fecha_regreso=request.GET['fecha_regreso'])

    # Filtros múltiples (checkboxes)
    clases_seleccionadas = request.GET.getlist('clase')
    regiones_seleccionadas = request.GET.getlist('region')
    aerolineas_seleccionadas = request.GET.getlist('aerolinea')

    if clases_seleccionadas:
        vuelos = vuelos.filter(clase__in=clases_seleccionadas)
    if regiones_seleccionadas:
        vuelos = vuelos.filter(region__in=regiones_seleccionadas)
    if aerolineas_seleccionadas:
        vuelos = vuelos.filter(aerolinea__in=aerolineas_seleccionadas)

    context = {
        'vuelos': vuelos,
        'clases_distintas': Vuelos.objects.values_list('clase', flat=True).distinct(),
        'regiones_distintas': Vuelos.objects.values_list('region', flat=True).distinct(),
        'aerolineas_distintas': Vuelos.objects.values_list('aerolinea', flat=True).distinct(),
        'clases_seleccionadas': clases_seleccionadas,
        'regiones_seleccionadas': regiones_seleccionadas,
        'aerolineas_seleccionadas': aerolineas_seleccionadas,
    }
    return render(request, 'Carrito_app/vuelos.html', context)

def vuelo_detalle(request, pk):
    vuelo = get_object_or_404(Vuelos, id=pk)
    return render(request, 'Carrito_app/vuelo_detalle.html', {'vuelo': vuelo})

def actividades(request):
    actividades = Actividad.objects.all()
    return render(request, 'Carrito_app/actividades.html', {'actividades': actividades})

def actividad_detalle(request, pk):
    actividad = get_object_or_404(Actividad, id=pk)
    return render(request, 'Carrito_app/actividad_detalle.html', {'actividad': actividad})

def alojamiento(request):
    alojamientos = Alojamiento.objects.filter(activo=True)
    return render(request, 'Carrito_app/alojamiento.html', {'alojamientos': alojamientos})

def alojamiento_detalle(request, id):
    alojamiento = get_object_or_404(Alojamiento, id=id)
    return render(request, 'Carrito_app/alojamiento_detalle.html', {'alojamiento': alojamiento})

def alquileres(request):
    alquileres = Alquiler.objects.all()
    return render(request, 'Carrito_app/alquileres.html', {'alquileres': alquileres})

def alquileres_detalle(request, id):
    alquiler = get_object_or_404(Alquiler, id=id)
    return render(request, 'Carrito_app/alquileres_detalle.html', {'alquiler': alquiler})

def transporte_detalle(request):
    transporte = get_object_or_404(Transporte, id=id)
    return render(request, 'Carrito_app/transporte_detalle.html', {'transporte': transporte})

def transporte(request):
    transportes = Transporte.objects.all()
    return render(request, 'Carrito_app/transporte.html', {'transportes': transportes})

def medios_pago(request):
    return render(request, 'Carrito_app/medios_pago.html')

def defensa_consumidor(request):
    return render(request, 'Carrito_app/defensa_consumidor.html')

def eliminacion_datos_personales(request):
    return render(request, 'Carrito_app/eliminacion_datos_personales.html')

def contacto(request):
    return render(request, 'Carrito_app/contacto.html')

def preguntas_frecuentes(request):
    return render(request, 'Carrito_app/preguntas_frecuentes.html')

def soporte(request):
    return render(request, 'Carrito_app/soporte.html')

def acerca(request):
    return render(request, 'Carrito_app/acerca.html')

def arrepentimiento(request):
    return render(request, 'Carrito_app/arrepentimiento.html')

def password_change(request):
    return render(request, 'Carrito_app/password_change.html')

def termino_condiciones(request):
    return render(request, 'Carrito_app/termino_condiciones.html')

def support(request):
    return render(request, 'Carrito_app/support.html')

def password_reset(request):
    return render(request, 'Carrito_app/password_reset.html')

# ------------------ REGISTRO Y LOGIN ------------------

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            codigo_verificacion = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            request.session['user_data'] = user_data
            request.session['codigo_verificacion'] = codigo_verificacion
            
            # Envía el correo de verificación
            send_mail(
                'Código de Verificación',
                f'Tu código de verificación es: {codigo_verificacion}',
                settings.EMAIL_HOST_USER,
                [user_data['email']],
                fail_silently=False,
            )
            
            return redirect('verificacion') # Redirige a la página de verificación
    else:
        form = RegisterForm()
    return render(request, 'Carrito_app/register.html', {'form': form})

def verify_email(request):
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo')
        codigo_verificacion = request.session.get('codigo_verificacion')

        if codigo_ingresado == codigo_verificacion:
            user_data = request.session.get('user_data')
            user = UserProfile.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            login(request, user)
            messages.success(request, 'Registro exitoso')
            # Limpia los datos de la sesión
            del request.session['user_data']
            del request.session['codigo_verificacion']
            return redirect('inicio')
        else:
            messages.error(request, 'El código de verificación es incorrecto.')
            return render(request, 'Carrito_app/verificacion.html', {'error': 'El código de verificación es incorrecto.'})
    return render(request, 'Carrito_app/verificacion.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('inicio')
        messages.error(request, 'Credenciales inválidas')
    return render(request, 'Carrito_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('inicio')

def detalle_compra(request, order_id):
    compra = get_object_or_404(Compra, id=order_id, usuario=request.user)
    return render(request, 'Carrito_app/detalle_compra.html', {'compra': compra})





# ------------------ PAQUETES ------------------
def alojamiento_detalle(request, id):
    alojamiento = get_object_or_404(Alojamiento, id=id)
    return render(request, 'Carrito_app/alojamiento_detalle.html', {'alojamiento': alojamiento})

def actividad_detalle(request, pk):
    actividad = get_object_or_404(Actividad, id=pk)
    return render(request, 'Carrito_app/actividad_detalle.html', {'actividad': actividad})

def vuelo_detalle(request, vuelo_id):
    vuelo = get_object_or_404(Vuelos, id=vuelo_id)
    return render(request, 'Carrito_app/vuelo_detalle.html', {'vuelo': vuelo})

def paquetes(request):
    paquetes = Paquete.objects.filter(activo=True)
    return render(request, 'Carrito_app/paquetes.html', {'paquetes': paquetes})

def paquete_detalle(request, paquete_id):
    paquete = get_object_or_404(Paquete, pk=paquete_id)
    return render(request, 'Carrito_app/paquete_detalle.html', {'paquete': paquete})

# ------------------ CARRITO ------------------

@login_required
def carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    
    # CARGAR TODOS LOS PRODUCTOS RELACIONADOS
    items = ItemCarrito.objects.filter(carrito=carrito).select_related(
        'paquete', 'vuelo', 'alojamiento', 'alquiler', 'transporte', 'actividad'
    )
    
    total = sum(item.subtotal() for item in items)

    return render(request, 'Carrito_app/carrito.html', {
        'items': items,
        'total': total
    })

@login_required
def add_to_cart(request, tipo, id):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    if tipo == "paquete":
        producto = get_object_or_404(Paquete, id=id)
        item, created = ItemCarrito.objects.get_or_create(carrito=carrito, paquete=producto)
    elif tipo == "alojamiento":
        producto = get_object_or_404(Alojamiento, id=id)
        item, created = ItemCarrito.objects.get_or_create(carrito=carrito, alojamiento=producto)
    elif tipo == "vuelo":
        producto = get_object_or_404(Vuelos, id=id)
        item, created = ItemCarrito.objects.get_or_create(carrito=carrito, vuelo=producto)
    elif tipo == "alquiler":
        producto = get_object_or_404(Alquiler, id=id)
        item, created = ItemCarrito.objects.get_or_create(carrito=carrito, alquiler=producto)
    elif tipo == "transporte":
        producto = get_object_or_404(Transporte, id=id)
        item, created = ItemCarrito.objects.get_or_create(carrito=carrito, transporte=producto)
    elif tipo == "actividad":
        producto = get_object_or_404(Actividad, id=id)
        item, created = ItemCarrito.objects.get_or_create(carrito=carrito, actividad=producto)
    else:
        messages.error(request, 'Tipo de producto inválido.')
        return redirect('carrito')

    if not created:
        item.cantidad += 1
        item.save()

    messages.success(request, f'{producto} agregado al carrito.')
    return redirect('carrito')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('carrito')

@login_required
def clear_cart(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    ItemCarrito.objects.filter(carrito=carrito).delete()
    messages.success(request, 'Carrito vaciado')
    return redirect('carrito')

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            item.cantidad += 1
        elif action == 'decrease' and item.cantidad > 1:
            item.cantidad -= 1
        item.save()
    return redirect('carrito')

@login_required
def checkout(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = ItemCarrito.objects.filter(carrito=carrito).select_related(
        'paquete', 'vuelo', 'alojamiento', 'alquiler', 'transporte', 'actividad'
    )
    
    if not items:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('carrito')

    total = sum(item.subtotal() for item in items)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method_type')
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="comprobante_compra.pdf"'
        pdf = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        pdf.setTitle("Comprobante de Compra - AILES DU MONDE")
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawCentredString(width / 2, height - 80, "AILES DU MONDE")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, height - 120, f"Cliente: {request.user.username}")
        pdf.drawString(50, height - 140, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        pdf.drawString(50, height - 160, f"Método de pago: {payment_method}")

        y = height - 200
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "Detalle de la compra:")
        y -= 20
        pdf.setFont("Helvetica", 11)

        for item in items:
            producto = item.get_producto()
            nombre = str(producto)
            precio = getattr(producto, 'precio', None) or getattr(producto, 'precio_por_persona', None) or getattr(producto, 'precio_por_noche', None)
            subtotal = precio * item.cantidad
            pdf.drawString(60, y, f"- {nombre} x{item.cantidad} = ${subtotal}")
            y -= 20
            if y < 100:
                pdf.showPage()
                y = height - 100

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(50, y - 10, f"Total: ${total}")
        pdf.line(45, y - 15, width - 45, y - 15)
        pdf.setFont("Helvetica-Oblique", 11)
        pdf.drawCentredString(width / 2, 60, "¡Gracias por confiar en AILES DU MONDE!")

        pdf.showPage()
        pdf.save()

        ItemCarrito.objects.filter(carrito=carrito).delete()

        return response

    return render(request, 'Carrito_app/checkout.html', {'items': items, 'total': total})

# ------------------ PERFIL ------------------

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.telefono = request.POST.get('telefono', '')
        profile.fecha_nacimiento = request.POST.get('fecha_nacimiento', None)
        profile.pais = request.POST.get('pais', '')
        profile.ciudad = request.POST.get('ciudad', '')
        profile.genero = request.POST.get('genero', '')
        profile.foto_perfil = request.FILES.get('foto_perfil', None)
        profile.direccion = request.POST.get('direccion', '')
        profile.codigo_postal = request.POST.get('codigo_postal', '')
        profile.save()

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('edit_profile')

    profile = getattr(request.user, 'userprofile', None)
    return render(request, 'Carrito_app/edit_profile.html', {'profile': profile})

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if request.user.check_password(old_password):
            if new_password1 == new_password2:
                request.user.set_password(new_password1)
                request.user.save()
                messages.success(request, 'Contraseña cambiada correctamente.')
                return redirect('login')
            else:
                messages.error(request, 'Las nuevas contraseñas no coinciden.')
        else:
            messages.error(request, 'Contraseña actual incorrecta.')

    return render(request, 'Carrito_app/change_password.html')
def order_history(request):
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha_compra')
    return render(request, 'Carrito_app/order_history.html', {'compras': compras})

@login_required
def detalle_compra(request, order_id):
    compra = get_object_or_404(Compra, id=order_id, usuario=request.user)
    return render(request, 'Carrito_app/detalle_compra.html', {'compra': compra})

@login_required
def compra_exitosa(request):
    return render(request, 'Carrito_app/compra_exitosa.html')   


@login_required
def finalizar_compra(request):
    carrito = request.user.carrito  # o como tengas el carrito
    total = carrito.get_total()     # método que calcule el total

    # Crear la compra
    compra = Compra.objects.create(
        usuario=request.user,
        total=total,
        metodo_pago=request.GET.get('metodo_pago', 'No especificado')  # ejemplo
    )

    # Agregar ítems según su tipo
    for item in carrito.items.all():
        if hasattr(item, 'paquete') and item.paquete:
            compra.paquetes.add(item.paquete)
        if hasattr(item, 'alojamiento') and item.alojamiento:
            compra.alojamientos.add(item.alojamiento)
        if hasattr(item, 'vuelo') and item.vuelo:
            compra.vuelos.add(item.vuelo)
        if hasattr(item, 'alquiler') and item.alquiler:
            compra.alquileres.add(item.alquiler)
        if hasattr(item, 'transporte') and item.transporte:
            compra.transportes.add(item.transporte)
        if hasattr(item, 'actividad') and item.actividad:
            compra.actividades.add(item.actividad)

    # Guardar la compra
    compra.save()

    # Limpiar carrito si querés
    carrito.items.clear()

    return redirect('compra_exitosa')  # o la URL que tengas

@login_required
def descargar_comprobante(request):
    compra = Compra.objects.filter(usuario=request.user).last()
    if not compra:
        messages.error(request, 'No se encontró ninguna compra reciente.')
        return redirect('order_history')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="comprobante_compra.pdf"'
    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    pdf.setTitle("Comprobante de Compra - AILES DU MONDE")
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(width / 2, height - 80, "AILES DU MONDE")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 120, f"Cliente: {request.user.username}")
    pdf.drawString(50, height - 140, f"Fecha: {compra.fecha_compra.strftime('%d/%m/%Y %H:%M')}")

    y = height - 180
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Detalle de la compra:")
    y -= 20
    pdf.setFont("Helvetica", 11)

    for producto in compra.items.all():
        nombre = str(producto)
        precio = getattr(producto, 'precio', None) or getattr(producto, 'precio_por_persona', None) or getattr(producto, 'precio_por_noche', None)
        pdf.drawString(60, y, f"- {nombre} = ${precio}")
        y -= 20
        if y < 100:
            pdf.showPage()
            y = height - 100

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y - 10, f"Total: ${compra.total}")
    pdf.line(45, y - 15, width - 45, y - 15)
    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawCentredString(width / 2, 60, "¡Gracias por confiar en AILES DU MONDE!")

    pdf.showPage()
    pdf.save()

    return response

@login_required
def pago(request):
    return render(request, 'Carrito_app/pago.html') 

@login_required
def pago_exitoso(request):
    return render(request, 'Carrito_app/pago_exitoso.html')

# ------------------ PAGOS ------------------   
@login_required
def medios_pago(request):
    return render(request, 'Carrito_app/medios_pago.html')

# ------------------ UPDATE CART MEJORADO ------------------
@login_required
def update_cart(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            item.cantidad += 1
        elif action == 'decrease' and item.cantidad > 1:
            item.cantidad -= 1
        item.save()
    return redirect('carrito')



def detalle_compra(request, order_id=None):
    if order_id is None:
        # Redirigir a historial de compras o mostrar un mensaje
        return redirect('order_history')
    compra = Compra.objects.get(id=order_id)
    return render(request, 'Carrito_app/detalle_compra.html', {'compra': compra})
