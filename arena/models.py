from django.db import models


class Videojuego(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    desarrolladora = models.CharField(max_length=100)
    genero = models.CharField(max_length=60)
    anio_lanzamiento = models.PositiveSmallIntegerField()
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    pais = models.CharField(max_length=60)
    anio_fundacion = models.PositiveSmallIntegerField()
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Torneo(models.Model):
    nombre = models.CharField(max_length=150)
    videojuego = models.ForeignKey(
        Videojuego, on_delete=models.CASCADE, related_name='torneos')
    equipos = models.ManyToManyField(Equipo, related_name='torneos')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    sede = models.CharField(max_length=100)
    premio = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['fecha_inicio']

    def __str__(self):
        return self.nombre
