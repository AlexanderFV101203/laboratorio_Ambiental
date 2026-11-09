from django.contrib import admin
from .models import Solicitud, Prueba


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "orden_laboratorio",
        "modelo",
        "cantidad_piezas",
        "originador",
        "estado",
        "fecha_creacion",
        "solicitante",
    )

    list_filter = (
        "estado",
        "fecha_creacion",
    )

    search_fields = (
        "orden_laboratorio",
        "modelo",
        "originador",
        "lote",
    )

    readonly_fields = (
        "fecha_creacion",
        "fecha_actualizacion",
    )

    filter_horizontal = ("pruebas",)

    @admin.register(Prueba)
    class PruebaAdmin(admin.ModelAdmin):
        list_display = ("id", "nombre", "activa")
        list_filter = ("activa",)
        search_fields = ("nombre",)

        