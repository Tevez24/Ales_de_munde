from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Formulario personalizado para la creaciÃ³n de usuarios con email obligatorio y validaciÃ³n de username
class CustomUser_CreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Provide a valid email address for verification.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya estÃ¡ en uso. Por favor, elige otro.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# Formulario para editar perfil
class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# Formulario de cambio de contraseÃ±a (opcional)
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'ContraseÃ±a actual'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseÃ±a'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repetir nueva contraseÃ±a'}))
