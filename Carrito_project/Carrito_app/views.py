from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUser_CreationForm
# Se importa el modelo Actividad
from .models import Paquete, Destino, Transporte, Actividad

# Vistas de páginas estáticas
def inicio(request):
    return render(request, 'Carrito_app/inicio.html')

@login_required
def home(request):
    return render(request, 'registration/home.html')

def acerca(request):
    return render(request, 'Carrito_app/acerca.html')

def arrepentimiento(request):
    return render(request, 'Carrito_app/arrepentimiento.html')

# Vista para mostrar las actividades
def actividades(request):
    actividades = Actividad.objects.all()
    # Obtiene solo los destinos que tienen al menos una actividad.
    destinos = Destino.objects.filter(actividades__isnull=False).distinct()

    # Lógica de filtrado por destino
    destino_id = request.GET.get('destino')
    if destino_id:
        actividades = actividades.filter(destino_id=destino_id)
        
    return render(request, 'Carrito_app/actividades.html', {
        'actividades': actividades,
        'destinos': destinos
    })

def alojamiento(request):
    return render(request, 'Carrito_app/alojamiento.html')

def alquileres(request):
    return render(request, 'Carrito_app/alquileres.html')

def vuelos(request):
    return render(request, 'Carrito_app/vuelos.html')

def transporte(request):
    transportes = Transporte.objects.all()
    return render(request, 'Carrito_app/transporte.html', {'transportes': transportes})

def transporte_detalle(request, transporte_id):
    transporte = get_object_or_404(Transporte, id=transporte_id)
    return render(request, 'Carrito_app/transporte_detalle.html', {'transporte': transporte})

def contacto(request):
    return render(request, 'Carrito_app/contacto.html')

def medios_pago(request):
    return render(request, 'Carrito_app/medios_pago.html')  

def soporte_pago(request):
    return render(request, 'Carrito_app/soporte_pago.html')

def preguntas_frecuentes(request):
    return render(request, 'Carrito_app/preguntas_frecuentes.html')
 
# Vista principal de paquetes (Home)
def paquetes(request):
    paquetes = Paquete.objects.all()
    destinos = Destino.objects.all()
    
    # Lógica de filtrado por destino
    destino_id = request.GET.get('destino')
    if destino_id:
        paquetes = paquetes.filter(destino_id=destino_id)
        
    # Lógica de filtrado por precio máximo
    precio_max = request.GET.get('precio_max')
    if precio_max:
        try:
            # Filtra los paquetes cuyo precio es menor o igual al máximo
            paquetes = paquetes.filter(precio__lte=float(precio_max))
        except (ValueError, TypeError):
            # Ignora el filtro si el valor no es un número válido
            pass

    return render(request, 'Carrito_app/paquetes.html', {
        'paquetes': paquetes,
        'destinos': destinos
    })

# Vista de detalle del paquete
def paquete_detalle(request, paquete_id):
    paquete = get_object_or_404(Paquete, id=paquete_id)
    return render(request, 'Carrito_app/paquete_detalle.html', {'paquete': paquete})

# --- Vistas del Carrito ---
def carrito(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for item_id, item_data in cart.items():
        paquete = get_object_or_404(Paquete, id=item_id)
        item_total = paquete.precio * item_data['quantity']
        
        # Genera la URL de la imagen, si existe
        imagen_url = ''
        if paquete.imagen:
            imagen_url = paquete.imagen.url
            
        items.append({
            'id': item_id,
            'nombre': paquete.nombre,
            'precio': paquete.precio,
            'quantity': item_data['quantity'],
            'imagen_url': imagen_url,  # Pasamos la URL a la plantilla
            'total': item_total
        })
        total += item_total
    
    return render(request, 'Carrito_app/carrito.html', {'items': items, 'total': total})

def password_change(request):
    return render(request, 'Carrito_app/password_change.html')  

def pago(request):
    return render(request, 'Carrito_app/pago.html')

def support(request):
    return render(request, 'Carrito_app/support.html')
  
@login_required
def add_to_cart(request, paquete_id):
    paquete = get_object_or_404(Paquete, id=paquete_id)
    cart = request.session.get('cart', {})
    
    item_id = str(paquete_id)
    
    if item_id in cart:
        messages.info(request, f'"{paquete.nombre}" ya está en tu carrito.')
    else:
        cart[item_id] = {'quantity': 1}
        messages.success(request, f'"{paquete.nombre}" ha sido añadido a tu carrito.')
        
    request.session['cart'] = cart
    return redirect('carrito')

@login_required
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)

    if item_id_str in cart:
        del cart[item_id_str]
        request.session['cart'] = cart
        messages.success(request, "El producto fue eliminado de tu carrito.")
        
    return redirect('carrito')

@login_required
def checkout(request):
    request.session['cart'] = {}
    return render(request, 'Carrito_app/checkout_success.html')

# --- Formulario para editar perfil ---
class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# --- Vistas de Autenticación ---

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'Carrito_app/login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'Carrito_app/login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Registro
def register_view(request):
    if request.method == 'POST':
        form = CustomUser_CreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUser_CreationForm()
    return render(request, 'Carrito_app/register.html', {'form': form})

# Editar perfil
@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = user.profile
    except:
        profile = None  # Por si no existe perfil relacionado

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Actualizar datos de perfil si existe
            if profile:
                profile.phone = request.POST.get('phone')
                profile.birth_date = request.POST.get('birth_date')
                profile.country = request.POST.get('country')
                profile.city = request.POST.get('city')
                profile.document_type = request.POST.get('document_type')
                profile.document_number = request.POST.get('document_number')
                profile.save()
            return redirect('home')
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'Carrito_app/edit_profile.html', {'form': form, 'profile': profile})

# Historial de órdenes
@login_required
def order_history(request):
    # Acá podes traer tus órdenes desde tu modelo
    return render(request, 'Carrito_app/order_history.html')
