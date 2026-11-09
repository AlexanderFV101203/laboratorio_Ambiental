from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import SolicitudForm, SolicitarInformacionForm, ResponderInformacionForm
from .models import Solicitud

@login_required
def crear_solicitud(request):

    if not request.user.has_perm("solicitudes.add_solicitud"):
        raise PermissionDenied

    if request.method == "POST":

        formulario = SolicitudForm(request.POST)

        if formulario.is_valid():

            nombre = request.user.get_full_name().strip()

            if not nombre:

                formulario.add_error(
                    None,
                    "Tu perfil no tiene nombre completo. "
                    "Contacta al administrador."
                )

            else:

                solicitud = formulario.save(commit=False)

                solicitud.solicitante = request.user
                solicitud.originador = nombre
                solicitud.estado = Solicitud.Estado.RECIBIDA

                solicitud.save()

                # Guardar las pruebas seleccionadas
                formulario.save_m2m()

                return redirect("lista_solicitudes")

    else:
        formulario = SolicitudForm()

    return render(
        request,
        "solicitudes/crear.html",
        {"formulario": formulario}
    )

@login_required
def lista_solicitudes(request):

    if not request.user.has_perm("solicitudes.view_solicitud"):
        raise PermissionDenied

    es_laboratorio = request.user.groups.filter(
        name="Laboratorio"
    ).exists()

    if es_laboratorio or request.user.is_superuser:
        solicitudes = Solicitud.objects.all()

    else:
        solicitudes = Solicitud.objects.filter(
            solicitante=request.user
        )

    return render(
        request,
        "solicitudes/lista.html",
        {"solicitudes": solicitudes}
    )

@login_required
def detalle_solicitud(request, solicitud_id):

    if not request.user.has_perm("solicitudes.view_solicitud"):
        raise PermissionDenied

    solicitud = get_object_or_404(
        Solicitud.objects.prefetch_related("pruebas"),
        id=solicitud_id
    )

    es_laboratorio = request.user.groups.filter(
        name="Laboratorio"
    ).exists()

    if not es_laboratorio and not request.user.is_superuser:

        if solicitud.solicitante_id != request.user.id:
            raise PermissionDenied

    return render(
        request,
        "solicitudes/detalle.html",
        {
            "solicitud": solicitud,
            "es_laboratorio": es_laboratorio,
        }
    )

@login_required
@require_POST
def iniciar_revision(request, solicitud_id):

    if not request.user.has_perm("solicitudes.change_solicitud"):
        raise PermissionDenied

    es_laboratorio = request.user.groups.filter(
        name="Laboratorio"
    ).exists()

    if not es_laboratorio and not request.user.is_superuser:
        raise PermissionDenied

    solicitud = get_object_or_404(
        Solicitud,
        id=solicitud_id
    )

    if solicitud.estado != Solicitud.Estado.RECIBIDA:
        raise PermissionDenied

    solicitud.estado = Solicitud.Estado.EN_REVISION

    solicitud.save(
        update_fields=[
            "estado",
            "fecha_actualizacion",
        ]
    )

    return redirect(
        "detalle_solicitud",
        solicitud_id=solicitud.id
    )

@login_required
@require_POST
def aceptar_solicitud(request, solicitud_id):

    if not request.user.has_perm("solicitudes.change_solicitud"):
        raise PermissionDenied

    es_laboratorio = request.user.groups.filter(
        name="Laboratorio"
    ).exists()

    if not es_laboratorio and not request.user.is_superuser:
        raise PermissionDenied

    solicitud = get_object_or_404(
        Solicitud,
        id=solicitud_id
    )

    if solicitud.estado != Solicitud.Estado.EN_REVISION:
        raise PermissionDenied

    solicitud.estado = Solicitud.Estado.ACEPTADA

    solicitud.save(
        update_fields=[
            "estado",
            "fecha_actualizacion",
        ]
    )

    return redirect(
        "detalle_solicitud",
        solicitud_id=solicitud.id
    )

@login_required
def solicitar_informacion(request, solicitud_id):

    if not request.user.has_perm("solicitudes.change_solicitud"):
        raise PermissionDenied

    es_laboratorio = request.user.groups.filter(
        name="Laboratorio"
    ).exists()

    if not es_laboratorio and not request.user.is_superuser:
        raise PermissionDenied

    solicitud = get_object_or_404(
        Solicitud,
        id=solicitud_id
    )

    if solicitud.estado != Solicitud.Estado.EN_REVISION:
        raise PermissionDenied

    if request.method == "POST":

        formulario = SolicitarInformacionForm(request.POST)

        if formulario.is_valid():

            solicitud.informacion_requerida = (
                formulario.cleaned_data["motivo"]
            )

            solicitud.estado = Solicitud.Estado.PENDIENTE

            solicitud.save(
                update_fields=[
                    "informacion_requerida",
                    "estado",
                    "fecha_actualizacion",
                ]
            )

            return redirect(
                "detalle_solicitud",
                solicitud_id=solicitud.id
            )

    else:

        formulario = SolicitarInformacionForm()

    return render(
        request,
        "solicitudes/solicitar_informacion.html",
        {
            "solicitud": solicitud,
            "formulario": formulario,
        }
    )


@login_required
def responder_informacion(request, solicitud_id):

    # Verificar que el usuario tenga permiso para consultar solicitudes.
    if not request.user.has_perm("solicitudes.view_solicitud"):
        raise PermissionDenied

    # Buscar la solicitud.
    solicitud = get_object_or_404(
        Solicitud,
        id=solicitud_id
    )

    if solicitud.solicitante_id != request.user.id:
        raise PermissionDenied

    if solicitud.estado != Solicitud.Estado.PENDIENTE:
        raise PermissionDenied

    if request.method == "POST":

        formulario = ResponderInformacionForm(
            request.POST,
            instance=solicitud
        )

        if formulario.is_valid():

            solicitud = formulario.save(commit=False)

            solicitud.estado = Solicitud.Estado.EN_REVISION

            solicitud.save(
                update_fields=[
                    "respuesta_informacion",
                    "estado",
                    "fecha_actualizacion",
                ]
            )

            return redirect(
                "detalle_solicitud",
                solicitud_id=solicitud.id
            )

    else:

        formulario = ResponderInformacionForm(
            instance=solicitud
        )

    return render(
        request,
        "solicitudes/responder_informacion.html",
        {
            "solicitud": solicitud,
            "formulario": formulario,
        }
    )

