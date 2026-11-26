from django import forms
from .models import Resena


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['torneo', 'autor', 'puntuacion', 'comentario']
        labels = {
            'torneo': 'Torneo',
            'autor': 'Tu nombre',
            'puntuacion': 'Puntuación (1-5)',
            'comentario': 'Comentario',
        }