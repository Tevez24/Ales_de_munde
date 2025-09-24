from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
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
    actividades = Actividad.objects.all()  # Se obtienen todas las actividades
    return render(request, 'Carrito_app/actividades.html', {'actividades': actividades})

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

# --- Vistas de Autenticación ---
def register_view(request):
    if request.method == "POST":
        form = CustomUser_CreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso! Ya puedes empezar a comprar.")
            return redirect("home")
    else:
        form = CustomUser_CreationForm()
    return render(request, "registration/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirige al home del usuario logueado
                return redirect("home") 
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect("inicio")

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Actualiza los datos del usuario
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        messages.success(request, '¡Tu perfil ha sido actualizado!')
        return redirect('home')
    return render(request, 'registration/edit_profile.html')

@login_required
def order_history(request):
    # Lógica para obtener el historial de pedidos del usuario
    # orders = request.user.orders.all()  # Suponiendo que tienes una relación
    orders = [] # Placeholder
    return render(request, 'registration/order_history.html', {'orders': orders})
