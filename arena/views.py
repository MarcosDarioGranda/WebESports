from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from .models import Videojuego, Equipo, Torneo


class PortadaView(TemplateView):
    template_name = 'arena/portada.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        destacados = []
        for juego in Videojuego.objects.all():
            torneos = juego.torneos.all() #type:ignore
            torneo = (torneos.filter(fecha_fin__gte=hoy)
                      .order_by('fecha_inicio').first()
                      or torneos.order_by('-fecha_inicio').first())
            if torneo:
                destacados.append(torneo)
        ctx['destacados'] = destacados
        return ctx


class TorneoListView(ListView):
    model = Torneo
    queryset = Torneo.objects.select_related('videojuego')


class TorneoDetailView(DetailView):
    model = Torneo


class VideojuegoListView(ListView):
    model = Videojuego


class VideojuegoDetailView(DetailView):
    model = Videojuego


class EquipoListView(ListView):
    model = Equipo


class EquipoDetailView(DetailView):
    model = Equipo

class TorneoEquiposView(View):
    
    def get(self, request, pk):
        torneo = get_object_or_404(Torneo, pk=pk)
        equipos = [
            {'nombre': e.nombre,
             'url': reverse('arena:equipo_detail', args=[e.pk])}
            for e in torneo.equipos.all()
        ]
        return JsonResponse({'torneo': torneo.nombre, 'equipos': equipos})