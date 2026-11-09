
from django import forms

from .models import Solicitud, Prueba


class SolicitudForm(forms.ModelForm):

    pruebas = forms.ModelMultipleChoiceField(
        queryset=Prueba.objects.filter(activa=True).order_by("-id"),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Pruebas solicitadas",
        error_messages={
            "required": "Debes seleccionar al menos una prueba."
        }
    )

    class Meta:
        model = Solicitud

        fields = [
            "modelo",
            "resistencia",
            "tolerancia",
            "orden_trabajo",
            "codigo_fecha",
            "lote",
            "cantidad_piezas",
            "pruebas",
            "comentarios",
        ]

    def clean_cantidad_piezas(self):
        cantidad = self.cleaned_data["cantidad_piezas"]

        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError(
                "La cantidad de piezas debe ser mayor que cero."
            )

        return cantidad
    
    def clean_tolerancia(self):
        tolerancia = self.cleaned_data["tolerancia"]

        if tolerancia is None:
            return tolerancia

        if tolerancia < 0 or tolerancia > 100:
            raise forms.ValidationError(
                "La tolerancia debe estar entre 0 y 100%."
            )

        return tolerancia

class SolicitarInformacionForm(forms.Form):

    motivo = forms.CharField(
        label="Información requerida",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": (
                    "Describe qué información necesita "
                    "proporcionar el solicitante."
                ),
            }
        ),
        required=True,
        min_length=10,
        error_messages={
            "required": "Debes indicar qué información falta.",
            "min_length": "Escribe al menos 10 caracteres.",
        }
    )


class ResponderInformacionForm(forms.ModelForm):

    class Meta:
        model = Solicitud

        fields = [
            "respuesta_informacion",
        ]

        labels = {
            "respuesta_informacion": "Respuesta del solicitante",
        }

        widgets = {
            "respuesta_informacion": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": (
                        "Escribe la información solicitada "
                        "por el laboratorio."
                    ),
                }
            ),
        }

    def clean_respuesta_informacion(self):
        respuesta = self.cleaned_data["respuesta_informacion"].strip()

        if len(respuesta) < 10:
            raise forms.ValidationError(
                "Escribe una respuesta de al menos 10 caracteres."
            )

        return respuesta
