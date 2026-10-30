from datetime import date
from django.core.management.base import BaseCommand
from arena.models import Videojuego, Equipo, Torneo


class Command(BaseCommand):
    help = 'Carga datos de ejemplo'

    def handle(self, *args, **options):
        juegos = {n: Videojuego.objects.get_or_create(
            nombre=n, defaults=dict(desarrolladora=d, genero=g,
                                    anio_lanzamiento=a, descripcion=desc))[0]
                  for n, d, g, a, desc in [
            ('League of Legends', 'Riot Games', 'MOBA', 2009, 'Juego de estrategia por equipos 5v5.'),
            ('Valorant', 'Riot Games', 'Shooter táctico', 2020, 'Shooter 5v5 con agentes y habilidades.'),
            ('Counter-Strike 2', 'Valve', 'Shooter táctico', 2023, 'Clásico shooter competitivo.'),
            ('EA FC', 'EA Sports', 'Deportes', 2023, 'Simulador de fútbol.'),
            ('Rocket League', 'Psyonix', 'Deportes', 2015, 'Fútbol con coches.'),
        ]}
        equipos = {n: Equipo.objects.get_or_create(
            nombre=n, defaults=dict(pais=p, anio_fundacion=a, descripcion=desc))[0]
                   for n, p, a, desc in [
            ('G2 Esports', 'Alemania', 2014, 'Organización europea multititular.'),
            ('Fnatic', 'Reino Unido', 2004, 'Una de las más veteranas de Europa.'),
            ('Team Heretics', 'España', 2016, 'Club español de esports.'),
            ('KOI', 'España', 2022, 'Organización fundada por Ibai y Piqué.'),
            ('Team Vitality', 'Francia', 2013, 'Organización francesa.'),
        ]}
        torneos = [
            ('LEC Primavera 2027', 'League of Legends', date(2027, 3, 1), date(2027, 4, 20), 'Berlín', 100000),
            ('VCT EMEA Stage 1', 'Valorant', date(2027, 2, 10), date(2027, 3, 30), 'Berlín', 250000),
            ('IEM Katowice 2027', 'Counter-Strike 2', date(2027, 1, 28), date(2027, 2, 8), 'Katowice', 1000000),
            ('FC Pro Open', 'EA FC', date(2027, 5, 5), date(2027, 5, 9), 'Madrid', 50000),
            ('RLCS Open 2027', 'Rocket League', date(2027, 4, 2), date(2027, 4, 6), 'París', 150000),
            ('Worlds 2026', 'League of Legends', date(2026, 10, 1), date(2026, 11, 2), 'Londres', 2000000),
        ]
        nombres = list(equipos)
        for i, (n, j, ini, fin, sede, premio) in enumerate(torneos):
            t, _ = Torneo.objects.get_or_create(
                nombre=n, defaults=dict(videojuego=juegos[j], fecha_inicio=ini,
                                        fecha_fin=fin, sede=sede, premio=premio,
                                        descripcion=f'Torneo oficial de {j}.'))
            t.equipos.set([equipos[nombres[(i + k) % 5]] for k in range(3)])
        self.stdout.write(self.style.SUCCESS('Datos cargados'))