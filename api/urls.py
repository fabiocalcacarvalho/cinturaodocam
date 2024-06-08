from django.urls import path
from . import views

urlpatterns = [
    path('partidas/<int:pk>', views.PartidaDetail.as_view()),
    path('partidas/', views.PartidaList.as_view()),
    path('jogadores/<int:pk>', views.JogadorDetail.as_view()),
    path('jogadores/', views.JogadorList.as_view()),
]