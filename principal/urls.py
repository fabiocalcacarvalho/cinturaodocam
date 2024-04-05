from django.urls import path
from . import views

urlpatterns = [
    path('', views.estatisticas, name='estatisticas'),
    path('regulamento/', views.regulamento, name='regulamento'),
    path('cadastrar_partida/', views.cadastrar_partida, name='cadastrar_partida'),
    path('cadastrar_jogador/', views.CreateJogadorView.as_view(), name='cadastrar_jogador'),
]
