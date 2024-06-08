from rest_framework import serializers
from principal.models import Partida, Jogador

class PartidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partida
        fields = '__all__'

class JogadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jogador
        fields = '__all__'