from django.shortcuts import render
from rest_framework import generics

from .serializers import PartidaSerializer, JogadorSerializer
from principal.models import Partida, Jogador

class JogadorList(generics.ListCreateAPIView):
    queryset = Jogador.objects.all()
    serializer_class = JogadorSerializer

class JogadorDetail(generics.RetrieveAPIView):
    queryset = Jogador.objects.all()
    serializer_class = JogadorSerializer

class PartidaList(generics.ListCreateAPIView):
    queryset = Partida.objects.all()
    serializer_class = PartidaSerializer

class PartidaDetail(generics.RetrieveAPIView):
    queryset = Partida.objects.all()
    serializer_class = PartidaSerializer