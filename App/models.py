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
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)

    tanque_agua = models.ForeignKey(
        'TanqueAgua',
        on_delete=models.CASCADE,
        related_name='usuarios',
        null=True,              # Permitir que esté vacío
        blank=True              # Permitir que no se envíe desde formularios
    )

    def __str__(self):
        return self.nombre

    def set_password(self, raw_password):
        self.contrasena = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.contrasena)

    class Meta:
        db_table = 'usuarios'


# ------------------------
# Modelo: Tanque de Agua
# ------------------------
class TanqueAgua(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    modelo = models.CharField(max_length=100)
    capacidad = models.FloatField(help_text="Capacidad en litros")
    color = models.CharField(max_length=50, choices=COLORES_TANQUE)
    fecha_instalacion = models.DateField()
    ubicacion = models.CharField(max_length=100)
    fecha_mantenimiento = models.DateField()
    historial_mantenimiento = models.TextField(blank=True, null=True)

    dispositivo = models.ForeignKey(
        'Dispositivo',
        on_delete=models.CASCADE,
        related_name='tanques'
    )

    def __str__(self):
        return f"{self.nombre} ({self.modelo})"

    class Meta:
        db_table = 'tanques_agua'


# ------------------------
# Modelo: Dispositivo
# ------------------------
class Dispositivo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50)
    fecha_instalacion = models.DateField()
    ubicacion = models.CharField(max_length=100)
    fecha_mantenimiento = models.DateField()
    historial_mantenimiento = models.TextField(blank=True, null=True)

    ph = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(14.0)])
    temperatura = models.FloatField(help_text="Temperatura en °C")
    conductividad = models.FloatField(help_text="Conductividad eléctrica en µS/cm")
    turbidez = models.FloatField(help_text="Turbidez en NTU")
    nivel_del_agua = models.FloatField(help_text="Nivel del agua en cm o %")

    historial_datos = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"

    class Meta:
        db_table = 'dispositivos'
