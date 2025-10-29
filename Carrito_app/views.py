from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import logging

from Carrito_app.models import Paquete, UserProfile, Carrito, ItemCarrito
from .forms import RegisterForm

# Configuración de logs
logger = logging.getLogger(__name__)

# ------------------ PÁGINAS PRINCIPALES ------------------

def home(request):
    return render(request, 'Carrito_app/home.html')

def inicio(request):
    # 🔹 Ahora ya no da error: 'activo' existe en el modelo
    paquetes = Paquete.objects.filter(activo=True)[:4]
    logger.debug(f"Paquetes cargados en inicio: {paquetes}")
    return render(request, 'Carrito_app/inicio.html', {'paquetes': paquetes})

def vuelos(request):
    return render(request, 'Carrito_app/vuelos.html')

def actividades(request):
    return render(request, 'Carrito_app/actividades.html')

def alojamiento(request):
    return render(request, 'Carrito_app/alojamiento.html')

def alquileres(request):
    return render(request, 'Carrito_app/alquileres.html')

def medios_pago(request):
    return render(request, 'Carrito_app/medios_pago.html')

def transporte(request):
    return render(request, 'Carrito_app/transporte.html')

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
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso')
            return redirect('inicio')
    else:
        form = RegisterForm()
    return render(request, 'Carrito_app/register.html', {'form': form})


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


# ------------------ PAQUETES ------------------

def paquetes(request):
    paquetes = Paquete.objects.filter(activo=True)
    return render(request, 'Carrito_app/paquetes.html', {'paquetes': paquetes})


def paquete_detalle(request, paquete_id):
    paquete = get_object_or_404(Paquete, pk=paquete_id)
    return render(request, 'Carrito_app/paquete_detalle.html', {'paquete': paquete})


# ------------------ CARRITO ------------------

def carrito(request):
    if not request.user.is_authenticated:
        return render(request, 'Carrito_app/carrito.html', {'items': [], 'total': 0})

    try:
        carrito = Carrito.objects.get(usuario=request.user)
        items = ItemCarrito.objects.filter(carrito=carrito)
        total = sum(item.subtotal() for item in items)
    except Carrito.DoesNotExist:
        items = []
        total = 0

    return render(request, 'Carrito_app/carrito.html', {
        'items': items,
        'total': total
    })


@login_required
def add_to_cart(request, paquete_id):
    paquete = get_object_or_404(Paquete, id=paquete_id)
    cantidad = int(request.GET.get('cantidad', 1))
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        paquete=paquete,
        defaults={'cantidad': cantidad}
    )
    if not created:
        item.cantidad += cantidad
        item.save()
    messages.success(request, f'{paquete.nombre} agregado al carrito')
    return redirect('carrito')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    paquete_nombre = item.paquete.nombre
    item.delete()
    messages.success(request, f'{paquete_nombre} eliminado del carrito')
    return redirect('carrito')


@login_required
def clear_cart(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        ItemCarrito.objects.filter(carrito=carrito).delete()
        messages.success(request, 'Carrito vaciado')
    except Carrito.DoesNotExist:
        messages.warning(request, 'No hay carrito para vaciar')
    return redirect('carrito')


# ------------------ PAGO ------------------

@login_required
def checkout(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        items = ItemCarrito.objects.filter(carrito=carrito)
        if not items:
            messages.warning(request, 'Tu carrito está vacío')
            return redirect('carrito')
        total = sum(item.subtotal() for item in items)
    except Carrito.DoesNotExist:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('carrito')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method_type')
        if payment_method in ['pagofacil', 'rapipago']:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="comprobante_pago.pdf"'
            p = canvas.Canvas(response, pagesize=letter)
            width, height = letter
            p.drawString(100, height - 100, "AILES DU MONDE - Comprobante de Pago")
            p.drawString(100, height - 120, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
            p.drawString(100, height - 140, f"Total: ${total}")
            p.drawString(100, height - 160, f"Método: {payment_method.upper()}")
            p.showPage()
            p.save()
            ItemCarrito.objects.filter(carrito=carrito).delete()
            return response

    return render(request, 'Carrito_app/checkout.html', {'items': items, 'total': total})


def pago(request):
    return render(request, 'Carrito_app/pago.html')


def pago_exitoso(request):
    return render(request, 'Carrito_app/pago_exitoso.html')


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


# ------------------ OTROS ------------------

def order_history(request):
    return render(request, 'Carrito_app/order_history.html')


def terminos(request):
    return render(request, 'Carrito_app/termino_condiciones.html')


def arrepentimiento(request):
    return render(request, 'Carrito_app/arrepentimiento.html')


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        messages.success(request, '¡Gracias por suscribirte a Ailes du Monde!')
        return redirect('inicio')
    return render(request, 'Carrito_app/inicio.html')
