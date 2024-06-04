from django.db import models
from datetime import date
from django.db.models import Q, F
class Jogador(models.Model):
    nome = models.CharField(max_length=100)
    imagem_url = models.URLField(max_length=800, null=True, blank=True)
    def quantidade_partidas(self):
        return Partida.objects.filter(Q(detentor_atual=self) | Q(desafiante=self)).count()
    def quantidade_vitorias(self):
        return Partida.objects.filter(
            Q(detentor_atual=self, placar_detentor_atual__gt=F('placar_desafiante')) |
            Q(desafiante=self, placar_desafiante__gt=F('placar_detentor_atual')) |
            Q(detentor_atual=self, placar_detentor_atual=F('placar_desafiante'), penaltis_detentor_atual__gt=F('penaltis_desafiante')) |
            Q(desafiante=self, placar_desafiante=F('placar_detentor_atual'), penaltis_desafiante__gt=F('penaltis_detentor_atual'))
        ).count()
    def porcentagem_vitorias(self):
        if self.quantidade_partidas() == 0:
            return 0
        return round((self.quantidade_vitorias() / self.quantidade_partidas()) * 100,2)
    def quantidade_partidas_como_detentor(self):
        return Partida.objects.filter(
            Q(detentor_atual=self)).count()
    def quantidade_vitorias_como_detentor(self):
        return Partida.objects.filter(
            Q(detentor_atual=self, placar_detentor_atual__gt=F('placar_desafiante')) |
            Q(detentor_atual=self, penaltis_detentor_atual__gt=F('penaltis_desafiante'))
            ).count()
    def porcentagem_vitorias_como_detentor(self):
        if self.quantidade_partidas_como_detentor() == 0:
            return 0
        return round((self.quantidade_vitorias_como_detentor() / self.quantidade_partidas_como_detentor()) * 100, 2)
    
    def quantidade_partidas_como_desafiante(self):
        return Partida.objects.filter(
            Q(desafiante=self)).count()
    def quantidade_vitorias_como_desafiante(self):
        return Partida.objects.filter(
            Q(desafiante=self, placar_desafiante__gt=F('placar_detentor_atual')) |
            Q(desafiante=self, penaltis_desafiante__gt=F('penaltis_detentor_atual'))
            ).count()
    def porcentagem_vitorias_como_desafiante(self):
        if self.quantidade_partidas_como_desafiante() == 0:
            return 0
        return round((self.quantidade_vitorias_como_desafiante() / self.quantidade_partidas_como_desafiante()) * 100, 2)
    def __str__(self):
        return self.nome
    
class Partida(models.Model):
    detentor_atual = models.ForeignKey(Jogador, related_name='partidas_detentor', on_delete=models.CASCADE)
    desafiante = models.ForeignKey(Jogador, related_name='partidas_desafiante', on_delete=models.CASCADE)
    data = models.DateField(default=date.today)
    placar_detentor_atual = models.PositiveIntegerField(default=0)
    placar_desafiante = models.PositiveIntegerField(default=0)
    penaltis_detentor_atual = models.PositiveIntegerField(default=0)
    penaltis_desafiante = models.PositiveIntegerField(default=0)

    def determinar_vencedor(self):
        if self.placar_detentor_atual > self.placar_desafiante:
            return self.detentor_atual
        elif self.placar_detentor_atual < self.placar_desafiante:
            return self.desafiante
        else:
            if self.penaltis_detentor_atual > self.penaltis_desafiante:
                return self.detentor_atual
            elif self.penaltis_detentor_atual < self.penaltis_desafiante:
                return self.desafiante
            else:
                return None
    def __str__(self):
        return str(self.detentor_atual) + ' x ' + str(self.desafiante) + ' (' + str(self.data) + ')' 