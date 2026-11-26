from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from .forms import ResenaForm
from .models import Videojuego, Equipo, Torneo


class PortadaView(TemplateView):
    template_name = 'arena/portada.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        destacados = []
        # prefetch_related: 2 consultas en total en vez de 1 por videojuego
        for juego in Videojuego.objects.prefetch_related('torneos'):
            torneos = list(juego.torneos.all())  # type:ignore
            proximos = [t for t in torneos if t.fecha_fin >= hoy]
            if proximos:
                # el más próximo en el tiempo
                destacados.append(min(proximos, key=lambda t: t.fecha_inicio))
            elif torneos:
                # si no hay futuros, el más reciente
                destacados.append(max(torneos, key=lambda t: t.fecha_inicio))
        ctx['destacados'] = destacados
        return ctx


class TorneoListView(ListView):
    model = Torneo
    queryset = Torneo.objects.select_related('videojuego')


class TorneoDetailView(DetailView):
    model = Torneo
    queryset = (Torneo.objects.select_related('videojuego').prefetch_related('equipos', 'resenas'))


class VideojuegoListView(ListView):
    model = Videojuego


class VideojuegoDetailView(DetailView):
    model = Videojuego
    queryset = Videojuego.objects.prefetch_related('torneos')


class EquipoListView(ListView):
    model = Equipo


class EquipoDetailView(DetailView):
    model = Equipo
    queryset = Equipo.objects.prefetch_related('torneos__videojuego')


class TorneoEquiposView(View):
    """Devuelve en JSON los equipos de un torneo (para la petición AJAX)."""

    def get(self, request, pk):
        torneo = get_object_or_404(Torneo, pk=pk)
        equipos = [
            {'nombre': e.nombre,
             'url': reverse('arena:equipo_detail', args=[e.pk])}
            for e in torneo.equipos.all()
        ]
        return JsonResponse({'torneo': torneo.nombre, 'equipos': equipos})

def crear_resena(request):
    if request.method == 'POST':
        # 1. Se reciben los datos
        form = ResenaForm(request.POST)
        # 2. Se validan
        if form.is_valid():
            # 3. Se guardan y se redirige al torneo
            resena = form.save()
            return redirect('arena:torneo_detail', pk=resena.torneo.pk)
    else:
        # GET: formulario vacío
        form = ResenaForm(initial={'torneo': request.GET.get('torneo')})
    return render(request, 'arena/resena.html', {'form': form})