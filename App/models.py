from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password, check_password

# Colores permitidos para los tanques de agua
COLORES_TANQUE = [
    ('azul', 'Azul'),
    ('blanco', 'Blanco'),
    ('negro', 'Negro'),
]

# ------------------------
# Modelo: Usuario
# ------------------------
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre completo del usuario
    email = models.EmailField(unique=True)  # Correo electrónico único
    contrasena = models.CharField(max_length=128)  # Contraseña cifrada

    tanque_agua = models.ForeignKey(
        'TanqueAgua',  # Relación con el modelo TanqueAgua
        on_delete=models.CASCADE,  # Si se elimina el tanque, se elimina el usuario
        related_name='usuarios'  # Nombre para acceder desde TanqueAgua.usuarios
    )

    def __str__(self):
        return self.nombre  # Muestra el nombre del usuario en el admin

    def set_password(self, raw_password):  # Cifra la contraseña al asignarla
        self.contrasena = make_password(raw_password)

    def check_password(self, raw_password):  # Verifica la contraseña ingresada
        return check_password(raw_password, self.contrasena)

    class Meta:
        db_table = 'usuarios'  # Nombre personalizado para la tabla


# ------------------------
# Modelo: Tanque de Agua
# ------------------------
class TanqueAgua(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Nombre del tanque
    modelo = models.CharField(max_length=100)  # Modelo del tanque
    capacidad = models.FloatField(help_text="Capacidad en litros")  # Capacidad
    color = models.CharField(max_length=50, choices=COLORES_TANQUE)  # Color válido
    fecha_instalacion = models.DateField()  # Fecha de instalación
    ubicacion = models.CharField(max_length=100)  # Ubicación física
    fecha_mantenimiento = models.DateField()  # Último mantenimiento
    historial_mantenimiento = models.TextField(blank=True, null=True)  # Registro histórico

    dispositivo = models.ForeignKey(
        'Dispositivo',  # Relación con el dispositivo conectado
        on_delete=models.CASCADE,  # Si se elimina el dispositivo, se elimina el tanque
        related_name='tanques'  # Nombre para acceder desde Dispositivo.tanques
    )

    def __str__(self):
        return f"{self.nombre} ({self.modelo})"

    class Meta:
        db_table = 'tanques_agua'


# ------------------------
# Modelo: Dispositivo
# ------------------------
class Dispositivo(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del dispositivo
    descripcion = models.TextField()  # Descripción general
    tipo = models.CharField(max_length=50)  # Tipo (sensor, medidor, etc.)
    fecha_instalacion = models.DateField()  # Fecha en que se instaló
    ubicacion = models.CharField(max_length=100)  # Dónde se encuentra
    fecha_mantenimiento = models.DateField()  # Fecha del último mantenimiento
    historial_mantenimiento = models.TextField(blank=True, null=True)  # Histórico de mantenimientos

    ph = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(14.0)])  # pH del agua
    temperatura = models.FloatField(help_text="Temperatura en °C")  # Temperatura del agua
    conductividad = models.FloatField(help_text="Conductividad eléctrica en µS/cm")  # Conductividad
    turbidez = models.FloatField(help_text="Turbidez en NTU")  # Nivel de turbidez
    nivel_del_agua = models.FloatField(help_text="Nivel del agua en cm o %")  # Nivel del líquido

    historial_datos = models.TextField(blank=True, null=True)  # Datos históricos de sensores

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"

    class Meta:
        db_table = 'dispositivos'
