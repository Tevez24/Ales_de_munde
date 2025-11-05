
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import JsonResponse, FileResponse
from .forms import CustomUser_CreationForm
from .models import Paquete, Destino, Transporte, Actividad, Carrito, ItemCarrito
from django.core.paginator import Paginator
import io
from reportlab.pdfgen import canvas
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import random
import string

# Vista para la página principal
def inicio(request):
    return render(request, 'Carrito_app/inicio.html')

# Vista para el login basado en formularios (HTML) con mensajes de error mejorados
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            # Intentamos encontrar al usuario para dar mensajes más claros
            try:
                user = User.objects.get(username=username)
                
                # 1. Comprobamos si la cuenta del usuario está inactiva
                if not user.is_active:
                    messages.error(request, "Tu cuenta no ha sido activada. Por favor, revisa tu correo electrónico y completa el proceso de verificación.")
                    return render(request, "Carrito_app/login.html", {"form": form})

                # 2. Si la cuenta está activa, intentamos autenticar (esto comprueba la contraseña)
                user_auth = authenticate(request, username=username, password=password)
                if user_auth is not None:
                    login(request, user_auth)
                    messages.success(request, f"¡Bienvenido de nuevo, {username}!")
                    return redirect('home')
                else:
                    # Si la autenticación falla, pero el usuario existe y está activo, la contraseña es incorrecta.
                    messages.error(request, "La contraseña es incorrecta. Por favor, inténtalo de nuevo.")

            except User.DoesNotExist:
                # 3. Si el usuario no existe en la base de datos
                messages.error(request, "No se encontró ninguna cuenta con ese nombre de usuario. Por favor, verifica tus datos o regístrate.")
        else:
            # Errores de validación del formulario (ej. campos vacíos)
            messages.error(request, "Por favor, introduce un nombre de usuario y contraseña válidos.")
    else:
        form = AuthenticationForm()
    
    return render(request, "Carrito_app/login.html", {"form": form})


def verify_code(request):
    if 'user_id_for_verification' not in request.session:
        messages.error(request, "Tu sesión de verificación ha expirado o es inválida. Por favor, regístrate o inicia sesión de nuevo.")
        return redirect('register')

    if request.method == 'POST':
        entered_code = request.POST.get('code')
        verification_code = request.session.get('verification_code')

        if entered_code and entered_code == verification_code:
            user_id = request.session.pop('user_id_for_verification')
            user = User.objects.get(id=user_id)
            
            if not user.is_active:
                user.is_active = True
                user.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            if 'verification_code' in request.session:
                del request.session['verification_code']

            messages.success(request, "¡Verificación exitosa! Has iniciado sesión.")
            return redirect('home')
        else:
            messages.error(request, "El código de verificación es incorrecto. Por favor, inténtalo de nuevo.")
    
    return render(request, 'Carrito_app/verify_code.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUser_CreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            verification_code = ''.join(random.choices(string.digits, k=6))
            
            request.session['user_id_for_verification'] = user.id
            request.session['verification_code'] = verification_code
            request.session.set_expiry(300)

            try:
                send_mail(
                    subject='Tu código de verificación - Ailes du Monde',
                    message=f'Hola {user.username},\n\nTu código de verificación es: {verification_code}\n\nGracias por registrarte en Ailes du Monde!',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                messages.success(request, "¡Registro exitoso! Te hemos enviado un código de verificación a tu correo.")
                return redirect('verify')
            except Exception as e:
                print(f'Error al enviar correo: {e}')
                messages.error(request, "No se pudo enviar el correo de verificación. Contacta a soporte.")
                return redirect('register')
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = CustomUser_CreationForm()
    return render(request, "Carrito_app/register.html", {"form": form})


@api_view(['POST'])
def login_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Faltan credenciales'}, status=status.HTTP_400_BAD_REQUEST)

    # Autenticar al usuario
    user = authenticate(request, username=username, password=password)

    # Verificar si el usuario está autenticado y activo
    if user is not None:
        if not user.is_active:
            return Response({'error': 'La cuenta no ha sido activada'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        
        try:
            if user.email:
                send_mail(
                    subject='Inicio de sesión exitoso - Ailes du Monde',
                    message=f'Hola {user.username},\n\nIniciaste sesión el {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.\nGracias por usar Ailes du Monde!',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
        except Exception as e:
            print(f'Error al enviar correo: {e}')
            
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Inicio de sesión exitoso. Revisa tu correo para la confirmación.'
        }, status=status.HTTP_200_OK)

    # Si la autenticación falla, devolver un error genérico
    return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

def support(request):
    return render(request, 'Carrito_app/support.html')

def pago(request):
    return render(request, 'Carrito_app/pago.html')

@login_required
def home(request):
    return render(request, 'Carrito_app/inicio.html')

def acerca(request):
    return render(request, 'Carrito_app/acerca.html')

def arrepentimiento(request):
    return render(request, 'Carrito_app/arrepentimiento.html')

def alojamiento(request):
    return render(request, 'Carrito_app/alojamiento.html')

def alquileres(request):
    return render(request, 'Carrito_app/alquileres.html')

def vuelos(request):
    return render(request, 'Carrito_app/vuelos.html')

def contacto(request):
    return render(request, 'Carrito_app/contacto.html')

def medios_pago(request):
    return render(request, 'Carrito_app/medios_pago.html')

def soporte_pago(request):
    return render(request, 'Carrito_app/soporte_pago.html')

def preguntas_frecuentes(request):
    return render(request, 'Carrito_app/preguntas_frecuentes.html')

def actividades(request):
    actividades = Actividad.objects.all()
    destinos = Destino.objects.filter(actividades__isnull=False).distinct()
    destino_id = request.GET.get('destino')
    if destino_id:
        actividades = actividades.filter(destino_id=destino_id)
    return render(request, 'Carrito_app/actividades.html', {
        'actividades': actividades,
        'destinos': destinos
    })

def transporte(request):
    transportes = Transporte.objects.all()
    return render(request, 'Carrito_app/transporte.html', {'transportes': transportes})

def transporte_detalle(request, transporte_id):
    transporte = get_object_or_404(Transporte, id=transporte_id)
    return render(request, 'Carrito_app/transporte_detalle.html', {'transporte': transporte})

def paquetes(request):
    destinos = Destino.objects.all()
    paquetes_list = Paquete.objects.all().select_related('destino').order_by('nombre')
    destino_id = request.GET.get('destino')
    if destino_id:
        paquetes_list = paquetes_list.filter(destino_id=destino_id)
    precio_max = request.GET.get('precio_max')
    if precio_max:
        try:
            paquetes_list = paquetes_list.filter(precio__lte=float(precio_max))
        except (ValueError, TypeError):
            pass
    paginator = Paginator(paquetes_list, 6)
    page_number = request.GET.get('page')
    paquetes_page = paginator.get_page(page_number)
    context = {
        'paquetes': paquetes_page,
        'destinos': destinos,
        'destino_id': destino_id,
        'precio_max': precio_max,
    }
    return render(request, 'Carrito_app/paquetes.html', context)

def paquete_detalle(request, paquete_id):
    paquete = get_object_or_404(Paquete, id=paquete_id)
    return render(request, 'Carrito_app/paquete_detalle.html', {'paquete': paquete})

@login_required
def update_cart(request, paquete_id):
    if request.method == 'POST':
        accion = request.POST.get('accion')
        carrito = request.session.get('carrito', {})
        if str(paquete_id) in carrito:
            if accion == 'increment':
                carrito[str(paquete_id)] += 1
            elif accion == 'decrement':
                carrito[str(paquete_id)] -= 1
                if carrito[str(paquete_id)] <= 0:
                    del carrito[str(paquete_id)]
        request.session['carrito'] = carrito
        request.session.modified = True
    return redirect('carrito')

@login_required
def carrito(request):
    carrito_sesion = request.session.get('carrito', {})
    paquetes = []
    total = 0
    for paquete_id, cantidad in carrito_sesion.items():
        paquete = get_object_or_404(Paquete, id=paquete_id)
        paquete.cantidad = cantidad
        paquete.subtotal = paquete.precio * cantidad
        total += paquete.subtotal
        paquetes.append(paquete)
    context = {
        'paquetes': paquetes,
        'total': total
    }
    return render(request, 'Carrito_app/carrito.html', context)

@login_required
@require_POST
def add_to_cart(request, paquete_id):
    carrito_sesion = request.session.get('carrito', {})
    if str(paquete_id) in carrito_sesion:
        carrito_sesion[str(paquete_id)] += 1
    else:
        carrito_sesion[str(paquete_id)] = 1
    request.session['carrito'] = carrito_sesion
    request.session.modified = True
    return JsonResponse({'status': 'success', 'message': 'Paquete añadido al carrito.'})

@login_required
def remove_from_cart(request, item_id):
    carrito_sesion = request.session.get('carrito', {})
    item_id_str = str(item_id)
    if item_id_str in carrito_sesion:
        del carrito_sesion[item_id_str]
        request.session['carrito'] = carrito_sesion
        request.session.modified = True
        messages.success(request, "El producto fue eliminado de tu carrito.")
    return redirect('carrito')

@login_required
def checkout(request):
    carrito_sesion = request.session.get('carrito', {})
    if not carrito_sesion:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('carrito')
    paquetes = []
    total = 0
    for paquete_id, cantidad in carrito_sesion.items():
        paquete = get_object_or_404(Paquete, id=paquete_id)
        paquete.cantidad = cantidad
        paquete.subtotal = paquete.precio * cantidad
        total += paquete.subtotal
        paquetes.append(paquete)
    if request.method == 'POST':
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica", 14)
        p.drawString(50, 800, f"Comprobante de compra - Usuario: {request.user.username}")
        y = 760
        for item in paquetes:
            p.drawString(50, y, f"{item.nombre} - Cantidad: {item.cantidad} - Precio: ${item.precio}")
            y -= 20
        p.drawString(50, y-20, f"Total: ${total}")
        p.showPage()
        p.save()
        buffer.seek(0)
        request.session['carrito'] = {}
        request.session.modified = True
        messages.success(request, "¡Compra realizada con éxito! Se descargará tu comprobante.")
        return FileResponse(buffer, as_attachment=True, filename='comprobante.pdf')
    return render(request, 'Carrito_app/checkout.html', {
        'paquetes': paquetes,
        'total': total
    })

class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class TerminosView(TemplateView):
    template_name = 'Carrito_app/termino_condiciones.html'

class PrivacidadView(TemplateView):
    template_name = 'Carrito_app/politica_privacidad.html'

@login_required
def edit_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        messages.success(request, '¡Tu perfil ha sido actualizado!')
        return redirect('home')
    return render(request, 'registration/edit_profile.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def order_history(request):
    orders = []
    return render(request, 'Carrito_app/order_history.html', {'orders': orders})
