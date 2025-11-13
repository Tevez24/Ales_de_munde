from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

# Formulario personalizado para la creación de usuarios con email obligatorio
class CustomUser_CreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# Formulario de registro de usuario
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Formulario para editar perfil
class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}))
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border rounded-md'}))
    country = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}))
    city = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}))
    document_type = forms.ChoiceField(choices=[
        ('', 'Seleccione un tipo'),
        ('DNI', 'DNI'),
        ('Pasaporte', 'Pasaporte'),
        ('Cedula', 'Cédula de Identidad')
    ], required=False, widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-md'}))
    document_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

# Formulario de cambio de contraseña (opcional)
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña actual'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseña'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repetir nueva contraseña'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

# Formulario para el proceso de pago (puede ser extendido según necesidades)
class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Número de tarjeta'}))
    expiration_date = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'placeholder': 'MM/AA'}))
    cvv = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'placeholder': 'CVV'}))
    cardholder_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre del titular'}))
    billing_address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Dirección de facturación'}))
    postal_code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Código postal'}))
    country = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'País'}))
    city = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Ciudad'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}))
    agree_terms = forms.BooleanField(required=True, label="Acepto los términos y condiciones")
    agree_privacy = forms.BooleanField(required=True, label="He leído y acepto la política de privacidad")
    agree_refund = forms.BooleanField(required=True, label="He leído y acepto la política de arrepentimiento y reembolso")
    agree_data = forms.BooleanField(required=True, label="Acepto el tratamiento de mis datos personales")
    agree_marketing = forms.BooleanField(required=False, label="Acepto recibir comunicaciones comerciales y de marketing")
    agree_cookies = forms.BooleanField(required=True, label="Acepto el uso de cookies según la política de cookies")
    agree_age = forms.BooleanField(required=True, label="Confirmo que soy mayor de edad")
    agree_responsibility = forms.BooleanField(required=True, label="Acepto las responsabilidades y condiciones del servicio")
    agree_travel_conditions = forms.BooleanField(required=True, label="He leído y acepto las condiciones específicas de viaje")
    agree_health_safety = forms.BooleanField(required=True, label="Acepto cumplir con las normativas de salud y seguridad vigentes")
    agree_cancellation = forms.BooleanField(required=True, label="He leído y acepto la política de cancelación")
    agree_additional = forms.BooleanField(required=False, label="Acepto los términos adicionales específicos del servicio contratado")
    agree_insurance = forms.BooleanField(required=False, label="Acepto los términos y condiciones del seguro de viaje")
    agree_loyalty = forms.BooleanField(required=False, label="Acepto los términos y condiciones del programa de fidelidad")
    agree_updates = forms.BooleanField(required=False, label="Acepto recibir actualizaciones sobre mi reserva y servicios relacionados")
    agree_feedback = forms.BooleanField(required=False, label="Acepto ser contactado para encuestas de satisfacción y feedback")
    agree_promotions = forms.BooleanField(required=False, label="Acepto recibir promociones y ofertas especiales")
    agree_newsletter = forms.BooleanField(required=False, label="Acepto suscribirme al boletín informativo")
    agree_social_media = forms.BooleanField(required=False, label="Acepto ser contactado a través de redes sociales")
    agree_third_party = forms.BooleanField(required=False, label="Acepto el intercambio de mis datos con terceros según la política de privacidad")
    agree_custom_terms = forms.BooleanField(required=False, label="Acepto los términos y condiciones personalizados aplicables a mi reserva")
    agree_event_notifications = forms.BooleanField(required=False, label="Acepto recibir notificaciones sobre eventos y actividades relacionadas con mi reserva")
    agree_travel_alerts = forms.BooleanField(required=False, label="Acepto recibir alertas de viaje y avisos importantes")
    agree_service_changes = forms.BooleanField(required=False, label="Acepto ser informado sobre cambios en los servicios contratados")
    agree_sustainability = forms.BooleanField(required=False, label="Acepto participar en iniciativas de sostenibilidad y turismo responsable")
    agree_community_guidelines = forms.BooleanField(required=False, label="Acepto cumplir con las directrices de la comunidad establecidas por la empresa")
    agree_legal_compliance = forms.BooleanField(required=True, label="Confirmo que cumpliré con todas las leyes y regulaciones aplicables durante el uso de los servicios contratados")
    agree_final = forms.BooleanField(required=True, label="He leído y acepto todos los términos y condiciones anteriores")
    # Campos adicionales pueden ser añadidos según los requisitos del negocio
