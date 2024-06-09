from rest_framework import serializers
from principal.models import Partida, Jogador

class PartidaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    detentor_atual = serializers.CharField(max_length=100)
    desafiante = serializers.CharField(max_length=100)
    data = serializers.DateField()
    placar_detentor_atual = serializers.IntegerField()
    placar_desafiante = serializers.IntegerField()
    penaltis_detentor_atual = serializers.IntegerField()
    penaltis_desafiante = serializers.IntegerField()
    class Meta:
        model = Partida

class JogadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jogador
        fields = '__all__'