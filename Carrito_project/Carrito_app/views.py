from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from .forms import CustomUser_CreationForm
def home_view(request):
    return render(request, 'home.html')
@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})
# Inicio
def inicio(request):
    return render(request, 'Carrito_app/inicio.html')
def home(request):
    return render(request, 'Carrito_app/home.html')
# Base
def base(request):
    return render(request, 'Carrito_app/base.html')
# Acerca
def acerca(request):
    return render(request, 'Carrito_app/acerca.html')
# Arrepentimiento
def arrepentimiento(request):
    return render(request, 'Carrito_app/arrepentimiento.html')
# Actividades
def actividades(request):
    return render(request, 'Carrito_app/actividades.html')
# Alojamientos
def alojamiento(request):
    return render(request, 'Carrito_app/alojamiento.html')
# Alquileres
def alquileres(request):
    return render(request, 'Carrito_app/alquileres.html')
# Carrito
def carrito(request):
    return render(request, 'Carrito_app/carrito.html')
# Paquetes
def paquetes(request):
    return render(request, 'Carrito_app/paquetes.html')
# Vuelos
def vuelos(request):
    return render(request, 'Carrito_app/vuelos.html')
# Transporte
def transporte(request):
    return render(request, 'Carrito_app/transporte.html')
#Contacto
def contacto(request):
    return render(request, 'Carrito_app/contacto.html')
# Registro
def register_view(request):
    if request.method == "POST":
        form = CustomUser_CreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomUser_CreationForm()
    return render(request, "Carrito_app/register.html", {"form": form})

# Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, "Carrito_app/login.html", {"form": form})

# Logout
def logout_view(request):
    logout(request)
    return redirect("inicio")
def cart_view(request):
    cart = request.session.get('cart', [])
    cart_items = []  # Populate with actual data
    for item_id in cart:
        # Example: Fetch package details from database or static data
        cart_items.append({
            'package_id': item_id,
            'name': 'Combo Sudamérica Aventura',  # Replace with actual data
            'price': 2800,  # Replace with actual data
            'image': static('Carrito_app/img/aventura patagonica.jpg')  # Replace with actual path
        })
    return render(request, 'Carrito_app/carrito.html', {'cart_items': cart_items})
