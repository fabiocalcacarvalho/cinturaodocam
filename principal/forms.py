from django import forms
from .models import Partida, Jogador
class PartidaForm(forms.ModelForm):
    class Meta:
        model = Partida
        fields = ['detentor_atual', 'desafiante', 'data', 'placar_detentor_atual', 'placar_desafiante', 'penaltis_detentor_atual', 'penaltis_desafiante']    
    def clean_placar_detentor_atual(self):
        placar = self.cleaned_data['placar_detentor_atual']
        if placar < 0:
            raise forms.ValidationError('O placar deve ser positivo')
        return placar

    def clean_placar_desafiante(self):
        placar = self.cleaned_data['placar_desafiante']
        if placar < 0:
            raise forms.ValidationError('O placar deve ser positivo')
        return placar
    
    def __init__(self, *args, **kwargs):
        super(PartidaForm, self).__init__(*args, **kwargs)
        ultima_partida = Partida.objects.last()
        if ultima_partida:
            ultimo_vencedor = ultima_partida.determinar_vencedor().nome
            self.fields['detentor_atual'].initial = Jogador.objects.filter(nome=ultimo_vencedor).first()

class HistoricoConfrontosForm(forms.Form):
    jogador_1 = forms.ModelChoiceField(queryset=Jogador.objects.all(), label='Jogador 1')
    jogador_2 = forms.ModelChoiceField(queryset=Jogador.objects.all(), label='Jogador 2')