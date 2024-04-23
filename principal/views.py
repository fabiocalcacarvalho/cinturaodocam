from django.shortcuts import render, redirect
from .models import Partida
from principal.models import Jogador
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
def regulamento(request):
    # Lógica para renderizar a página do regulamento
    return render(request, 'principal/regulamento.html')

from django.shortcuts import render, redirect
from .models import Partida, Jogador

from .forms import PartidaForm

def cadastrar_partida(request):
    if request.method == 'POST':
        form = PartidaForm(request.POST)
        if form.is_valid():
            nova_partida = form.save(commit=False)
            nova_partida.placar_detentor_atual = form.cleaned_data['placar_detentor_atual']
            nova_partida.placar_desafiante = form.cleaned_data['placar_desafiante']

            # Verificar se há empate
            if nova_partida.placar_detentor_atual == nova_partida.placar_desafiante:
                # Empate: Decidir nos pênaltis
                nova_partida.penaltis_detentor_atual = form.cleaned_data['penaltis_detentor_atual']
                nova_partida.penaltis_desafiante = form.cleaned_data['penaltis_desafiante']

            # Determinar o vencedor
            nova_partida.vencedor = nova_partida.determinar_vencedor()

            nova_partida.save()
            return redirect('estatisticas')
    else:
        form = PartidaForm()

    return render(request, 'principal/cadastrar_partida.html', {'form': form})
class CreateJogadorView(CreateView):
    model = Jogador
    fields = ['nome', 'imagem_url']

    def form_valid(self, form):
        form.save()
        return redirect('estatisticas')
    # nome do arquivo de template de criar
    def get_template_names(self):
        return 'principal/cadastrar_jogador.html'

def estatisticas(request):
    # Obtenha o detentor atual
    ultima_partida = Partida.objects.last()
    if ultima_partida:
        detentor_atual = ultima_partida.determinar_vencedor()
    else:
        detentor_atual = None

    # Obtenha todas as partidas
    partidas = Partida.objects.all()
    
    # Contagem de defesas de cinturão por jogador
    defesas_cinturao = {}
    for partida in partidas:
        detentor_nome = partida.detentor_atual.nome
        if detentor_nome in defesas_cinturao:
            # Se o detentor atual vencer a partida, incrementamos a contagem de defesas
            if partida.detentor_atual == partida.determinar_vencedor():
                defesas_cinturao[detentor_nome] += 1
        else:
            # Inicializamos a contagem com 1 se o detentor venceu a partida
            if partida.detentor_atual == partida.determinar_vencedor():
                defesas_cinturao[detentor_nome] = 1
            else:
                defesas_cinturao[detentor_nome] = 0

    # Encontre a maior diferença de gols
    maior_goleada = 0
    partida_maior_goleada = []
    for partida in partidas:
        diferenca_gols = abs(partida.placar_detentor_atual - partida.placar_desafiante)
        if diferenca_gols > maior_goleada:
            maior_goleada = diferenca_gols
            partida_maior_goleada = [partida]
        elif diferenca_gols == maior_goleada:
            partida_maior_goleada.append(partida)

    # Maior numero de defesas consecutivas de cinturão
    maior_sequencia = 0
    jogador_maior_sequencia = None
    defesas = 0
    data_inicial = None
    data_final = None
    for partida in partidas:
        jogador = partida.detentor_atual
        if partida.detentor_atual == partida.determinar_vencedor():
            defesas +=1
        else:
            defesas = 0
            data_inicial = partida.data
        if defesas > maior_sequencia:
            maior_sequencia = defesas
            jogador_maior_sequencia = jogador
            data_final = partida.data
    maior_sequencia = str(jogador_maior_sequencia) + ' (' + str(maior_sequencia) + ' defesas)'
    data_maior_sequencia = data_inicial.strftime('%d/%m/%Y') + ' a ' + data_final.strftime('%d/%m/%Y')
    context = {'detentor_atual': detentor_atual, 
               'partidas': partidas, 
               'defesas_cinturao': defesas_cinturao,
               'partida_maior_goleada': partida_maior_goleada,
               'maior_goleada': maior_goleada,
               'maior_sequencia': maior_sequencia,
               'data_maior_sequencia': data_maior_sequencia,
               'total_partidas': len(partidas)
               }

    return render(request, 'principal/index.html', context)