from django.contrib import admin
from .models import Videojuego, Equipo, Torneo


@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'desarrolladora', 'genero', 'anio_lanzamiento')
    search_fields = ('nombre',)


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'anio_fundacion')
    search_fields = ('nombre',)


@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'videojuego', 'fecha_inicio', 'fecha_fin', 'sede')
    list_filter = ('videojuego',)
    filter_horizontal = ('equipos',)
