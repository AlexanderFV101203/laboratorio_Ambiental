
from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.lista_solicitudes,
        name="lista_solicitudes"
    ),

    path(
        "nueva/",
        views.crear_solicitud,
        name="crear_solicitud"
    ),

    path(
        "<int:solicitud_id>/",
        views.detalle_solicitud,
        name="detalle_solicitud"
    ),

    path(
        "<int:solicitud_id>/iniciar-revision/",
        views.iniciar_revision,
        name="iniciar_revision"
    ),

    path(
        "<int:solicitud_id>/aceptar/",
        views.aceptar_solicitud,
        name="aceptar_solicitud"
    ),

    path(
        "<int:solicitud_id>/solicitar-informacion/",
        views.solicitar_informacion,
        name="solicitar_informacion"
    ),

    path(
        "<int:solicitud_id>/responder-informacion/",
        views.responder_informacion,
        name="responder_informacion"
    ),
]
