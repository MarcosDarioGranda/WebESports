from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView
from .models import Videojuego, Equipo, Torneo


class PortadaView(TemplateView):
    template_name = 'arena/portada.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        destacados = []
        for juego in Videojuego.objects.all():
            torneo = (Torneo.objects.filter(videojuego=juego, fecha_fin__gte=hoy)
                      .order_by('fecha_inicio').first()
                      or Torneo.objects.filter(videojuego=juego).order_by('-fecha_inicio').first())
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
