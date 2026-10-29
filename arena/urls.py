from django.urls import path
from . import views

app_name = 'arena'

urlpatterns = [
    path('', views.PortadaView.as_view(), name='portada'),
    path('torneos/', views.TorneoListView.as_view(), name='torneo_list'),
    path('torneos/<int:pk>/', views.TorneoDetailView.as_view(), name='torneo_detail'),
    path('videojuegos/', views.VideojuegoListView.as_view(), name='videojuego_list'),
    path('videojuegos/<int:pk>/', views.VideojuegoDetailView.as_view(), name='videojuego_detail'),
    path('equipos/', views.EquipoListView.as_view(), name='equipo_list'),
    path('equipos/<int:pk>/', views.EquipoDetailView.as_view(), name='equipo_detail'),
]
