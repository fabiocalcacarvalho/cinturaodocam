from django.db import models
from datetime import date
class Jogador(models.Model):
    nome = models.CharField(max_length=100)
    imagem_url = models.URLField(max_length=800, null=True, blank=True)
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