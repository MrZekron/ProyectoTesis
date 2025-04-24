# Importamos el sistema de formularios de Django
from django import forms

# Importamos nuestros modelos
from .models import Dispositivo, TanqueAgua, Usuario

# Para levantar errores personalizados en validaciones
from django.core.exceptions import ValidationError

# ----------------------------------
# FORMULARIO DE REGISTRO DISPOSITIVO
# ----------------------------------
class DispositivoForm(forms.ModelForm):
    # Este formulario se conecta directamente con el modelo Dispositivo
    class Meta:
        model = Dispositivo  # Modelo al que está vinculado
        fields = [
            'nombre',  # Nombre del dispositivo
            'descripcion',  # Descripción general
            'tipo',  # Tipo (sensor, etc.)
            'fecha_instalacion',  # Cuándo se instaló
            'ubicacion',  # Dónde está
            'fecha_mantenimiento',  # Próximo o último mantenimiento
            'historial_mantenimiento',  # Texto con historial
            'ph',  # Medición de pH
            'temperatura',  # Temperatura del agua
            'conductividad',  # Conductividad eléctrica
            'turbidez',  # Turbidez del agua
            'nivel_del_agua',  # Nivel del agua
            'historial_datos',  # Campo libre para datos históricos
        ]
        widgets = {
            # Cambiamos los campos de fecha para usar un input de tipo date (mejor para UX)
            'fecha_instalacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_mantenimiento': forms.DateInput(attrs={'type': 'date'}),
        }

# ----------------------------------
# FORMULARIO DE REGISTRO TANQUE AGUA
# ----------------------------------
class TanqueAguaForm(forms.ModelForm):
    # Conectado al modelo TanqueAgua
    class Meta:
        model = TanqueAgua
        fields = [
            'nombre',  # Nombre único del tanque
            'modelo',  # Modelo específico
            'capacidad',  # Capacidad en litros
            'color',  # Solo puede elegir de los colores definidos
            'fecha_instalacion',  # Fecha en que se instaló
            'ubicacion',  # Ubicación física
            'fecha_mantenimiento',  # Último mantenimiento
            'historial_mantenimiento',  # Registro libre
            'dispositivo',  # Dispositivo vinculado al tanque
        ]
        widgets = {
            'fecha_instalacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_mantenimiento': forms.DateInput(attrs={'type': 'date'}),
        }

# ----------------------------------
# FORMULARIO DE REGISTRO USUARIO
# ----------------------------------
class UsuarioForm(forms.ModelForm):
    # Campo personalizado para contraseña, enmascarado y con validación
    contrasena = forms.CharField(
        widget=forms.PasswordInput,  # El input será de tipo password
        min_length=8,  # Requiere mínimo 8 caracteres
        label="Contraseña",
        help_text="Debe tener al menos 8 caracteres."
    )
    
    # Email validado por Django
    email = forms.EmailField(
        label="Correo electrónico",
        help_text="Ingrese un correo válido."
    )

    class Meta:
        model = Usuario
        fields = [
            'nombre',  # Nombre del usuario
            'email',  # Email único
            'contrasena',  # Contraseña (enmascarada)
              
        ]

    # Validación personalizada de contraseña (opcional, ya está cubierto por min_length)
    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        if len(contrasena) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return contrasena

    # Validación para que el correo no se repita
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está registrado.")
        return email
