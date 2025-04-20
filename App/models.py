# Importación del sistema de modelos de Django
from django.db import models

# Importamos validadores para campos numéricos
from django.core.validators import MinValueValidator, MaxValueValidator

# Funciones para encriptar y verificar contraseñas
from django.contrib.auth.hashers import make_password, check_password

# Definimos una lista de colores permitidos para los tanques de agua
COLORES_TANQUE = [
    ('azul', 'Azul'),
    ('blanco', 'Blanco'),
    ('negro', 'Negro'),
]

# ------------------------
# Modelo: Dispositivo
# ------------------------
class Dispositivo(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del dispositivo
    descripcion = models.TextField()  # Descripción general
    tipo = models.CharField(max_length=50)  # Tipo del sensor o dispositivo
    fecha_instalacion = models.DateField()  # Fecha de instalación
    ubicacion = models.CharField(max_length=100)  # Ubicación física del dispositivo
    fecha_mantenimiento = models.DateField()  # Última fecha de mantenimiento
    historial_mantenimiento = models.TextField(blank=True, null=True)  # Registro libre de mantenimientos anteriores

    # Datos de monitoreo de agua con validaciones
    ph = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(14.0)])  # pH entre 0 y 14
    temperatura = models.FloatField(help_text="Temperatura en °C")  # Temperatura del agua
    conductividad = models.FloatField(help_text="Conductividad eléctrica en µS/cm")  # Conductividad del agua
    turbidez = models.FloatField(help_text="Turbidez en NTU")  # Claridad del agua
    nivel_del_agua = models.FloatField(help_text="Nivel del agua en cm o %")  # Nivel del agua en el tanque

    historial_datos = models.TextField(blank=True, null=True)  # Datos de lecturas anteriores

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"  # Representación legible en admin o shell

    class Meta:
        db_table = 'dispositivos'  # Nombre de la tabla en la base de datos


# ------------------------
# Modelo: Tanque de Agua
# ------------------------
class TanqueAgua(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Nombre único del tanque
    modelo = models.CharField(max_length=100)  # Modelo del tanque
    capacidad = models.FloatField(help_text="Capacidad en litros")  # Capacidad total en litros
    color = models.CharField(max_length=50, choices=COLORES_TANQUE)  # Color del tanque limitado a 3 opciones
    fecha_instalacion = models.DateField()  # Fecha de instalación
    ubicacion = models.CharField(max_length=100)  # Ubicación del tanque
    fecha_mantenimiento = models.DateField()  # Última revisión técnica
    historial_mantenimiento = models.TextField(blank=True, null=True)  # Historial opcional de mantenimiento

    dispositivo = models.ForeignKey(
        Dispositivo,  # Relación con el modelo Dispositivo
        on_delete=models.CASCADE,  # Si se elimina el dispositivo, se eliminan los tanques asociados
        related_name='tanques'  # Permite acceder a los tanques desde un dispositivo con .tanques.all()
    )

    def __str__(self):
        return f"{self.nombre} ({self.modelo})"

    class Meta:
        db_table = 'tanques_agua'


# ------------------------
# Modelo: Usuario
# ------------------------
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre completo del usuario
    email = models.EmailField(unique=True)  # Correo electrónico único para login
    contrasena = models.CharField(max_length=128)  # Contraseña encriptada

    tanque_agua = models.ForeignKey(
        TanqueAgua,  # Relación con tanque asignado
        on_delete=models.CASCADE,  # Si el tanque se borra, se elimina el usuario asociado
        related_name='usuarios'  # Permite acceder desde tanque.usuarios.all()
    )

    def __str__(self):
        return self.nombre  # Para mostrar nombre en el admin

    # Encripta la contraseña antes de guardarla
    def set_password(self, raw_password):
        self.contrasena = make_password(raw_password)

    # Verifica si la contraseña ingresada coincide con la guardada
    def check_password(self, raw_password):
        return check_password(raw_password, self.contrasena)

    class Meta:
        db_table = 'usuarios'  # Nombre personalizado de la tabla
