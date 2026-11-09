from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Solicitud(models.Model):

    class Estado(models.TextChoices):
        RECIBIDA = "RECIBIDA", "Recibida"
        EN_REVISION = "EN_REVISION", "En revisión"
        ACEPTADA = "ACEPTADA", "Aceptada"
        PENDIENTE = "PENDIENTE", "Pendiente de información"
        PROGRAMADA = "PROGRAMADA", "Programada"
        EN_PROCESO = "EN_PROCESO", "En proceso"
        TERMINADA = "TERMINADA", "Prueba terminada"
        CERRADA = "CERRADA", "Cerrada"
        CANCELADA = "CANCELADA", "Cancelada"

    orden_laboratorio = models.CharField(
        max_length=30,
        blank=True
    )

    modelo = models.CharField(max_length=100)

    resistencia = models.CharField(
        max_length=100,
        blank=True
    )

    tolerancia = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name="Tolerancia (%)"
    )

    orden_trabajo = models.CharField(
        max_length=100,
        blank=True
    )

    codigo_fecha = models.CharField(
        max_length=50,
        blank=True
    )

    lote = models.CharField(
        max_length=100,
        blank=True
    )

    cantidad_piezas = models.PositiveIntegerField()

    originador = models.CharField(max_length=150)

    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="solicitudes_creadas",
        null=True,
        blank=True
    )

    comentarios = models.TextField( blank=True )

    informacion_requerida = models.TextField( blank=True )

    respuesta_informacion = models.TextField(
        blank=True,
        verbose_name="Respuesta del solicitante"
    )
    
    pruebas = models.ManyToManyField(
        "Prueba",
        related_name="solicitudes",
        blank=True
    )

    # Seguimiento
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.RECIBIDA
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    informacion_requerida = models.TextField(
    blank=True
    )

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"

    def __str__(self):
        return f"Solicitud {self.id} - {self.modelo}"


class Prueba(models.Model):

    nombre = models.CharField(
        max_length=150,
        unique=True
    )

    descripcion = models.TextField(blank=True)

    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Prueba"
        verbose_name_plural = "Pruebas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
