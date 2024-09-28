from django.shortcuts import render, redirect
from .models import Partida
from principal.models import Jogador
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import HistoricoConfrontosForm
from django.db.models import Q, F, Sum
def regulamento(request):
    # Lógica para renderizar a página do regulamento
    return render(request, 'principal/regulamento.html')

from django.shortcuts import render, redirect
from .models import Partida, Jogador

from .forms import PartidaForm

def jogadores(request):
    jogadores = Jogador.objects.all()
    jogadores = Jogador.objects.all()
    jogadores_stats = []
    for jogador in jogadores:
        jogadores_stats.append({
            'jogador': jogador,
            'partidas': jogador.quantidade_partidas(),
            'vitorias': jogador.quantidade_vitorias(),
            'porc_vitorias': jogador.porcentagem_vitorias(),
            'partidas_como_detentor': jogador.quantidade_partidas_como_detentor(),
            'vitorias_como_detentor': jogador.quantidade_vitorias_como_detentor(),
            'porc_vitorias_como_detentor': jogador.porcentagem_vitorias_como_detentor(),
            'partidas_como_desafiante': jogador.quantidade_partidas_como_desafiante(),
            'vitorias_como_desafiante': jogador.quantidade_vitorias_como_desafiante(),
            'porc_vitorias_como_desafiante': jogador.porcentagem_vitorias_como_desafiante(),
            'gols_marcados_como_detentor': jogador.gols_marcados_como_detentor(),
            'gols_marcados_como_desafiante': jogador.gols_marcados_como_desafiante(),
            'gols_marcados_por_partida_como_detentor': jogador.gols_marcados_por_partida_como_detentor(),
            'gols_marcados_por_partida_como_desafiante': jogador.gols_marcados_por_partida_como_desafiante(),
            'gols_marcados_por_partida': jogador.gols_marcados_por_partida(),
            'gols_marcados': jogador.gols_marcados(),
            'gols_sofridos_como_detentor': jogador.gols_sofridos_como_detentor(),
            'gols_sofridos_como_desafiante': jogador.gols_sofridos_como_desafiante(),
            'gols_sofridos': jogador.gols_sofridos(),
            'gols_sofridos_por_partida_como_detentor': jogador.gols_sofridos_por_partida_como_detentor(),
            'gols_sofridos_por_partida_como_desafiante': jogador.gols_sofridos_por_partida_como_desafiante(),
            'gols_sofridos_por_partida': jogador.gols_sofridos_por_partida(),
            'saldo_de_gols_como_detentor': jogador.saldo_de_gols_como_detentor(),
            'saldo_de_gols_como_desafiante': jogador.saldo_de_gols_como_desafiante(),
            'saldo_de_gols': jogador.saldo_de_gols(),

        })
    
    context = {
        'jogadores_stats': jogadores_stats
    }
    return render(request, 'principal/jogadores.html', context)

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

def historico_confrontos(request):
    form = HistoricoConfrontosForm()
    partidas = None
    vitorias_jogador_1 = 0
    vitorias_jogador_2 = 0
    gols_marcados_jogador_1 = 0
    gols_marcados_jogador_2 = 0
    porcentagem_jogador_1 = 0
    porcentagem_jogador_2 = 0
    if request.method == 'POST':
        form = HistoricoConfrontosForm(request.POST)
        if form.is_valid():
            jogador_1 = form.cleaned_data['jogador_1']
            jogador_2 = form.cleaned_data['jogador_2']

            # Filtra as partidas entre os dois jogadores, independentemente da ordem
            partidas = Partida.objects.filter(
                Q(detentor_atual=jogador_1) | Q(detentor_atual=jogador_2),
                Q(desafiante=jogador_1) | Q(desafiante=jogador_2)
            ).order_by('-id')
            vitorias_jogador_1 = partidas.filter(Q(detentor_atual=jogador_1, placar_detentor_atual__gt=F('placar_desafiante'))
                                                 | Q(detentor_atual=jogador_1, penaltis_detentor_atual__gt=F('penaltis_desafiante'))
                                                 | Q(desafiante=jogador_1, placar_desafiante__gt=F('placar_detentor_atual')) 
                                                 | Q(desafiante=jogador_1, penaltis_desafiante__gt=F('penaltis_detentor_atual'))).count()
            vitorias_jogador_2 = partidas.filter(Q(detentor_atual=jogador_2, placar_detentor_atual__gt=F('placar_desafiante'))
                                                 | Q(detentor_atual=jogador_2, penaltis_detentor_atual__gt=F('penaltis_desafiante'))
                                                 | Q(desafiante=jogador_2, placar_desafiante__gt=F('placar_detentor_atual'))
                                                 | Q(desafiante=jogador_2, penaltis_desafiante__gt=F('penaltis_detentor_atual'))).count()
            gols_marcados_jogador_1 = partidas.filter(Q(detentor_atual=jogador_1)).aggregate(Sum('placar_detentor_atual'))['placar_detentor_atual__sum'] or 0
            gols_marcados_jogador_1 += partidas.filter(Q(desafiante=jogador_1)).aggregate(Sum('placar_desafiante'))['placar_desafiante__sum'] or 0
            gols_marcados_jogador_2 = partidas.filter(Q(detentor_atual=jogador_2)).aggregate(Sum('placar_detentor_atual'))['placar_detentor_atual__sum'] or 0
            gols_marcados_jogador_2 += partidas.filter(Q(desafiante=jogador_2)).aggregate(Sum('placar_desafiante'))['placar_desafiante__sum'] or 0

            # Cálculo das porcentagens
            total_gols = gols_marcados_jogador_1 + gols_marcados_jogador_2
            if total_gols > 0:
                porcentagem_jogador_1 = (gols_marcados_jogador_1 / total_gols) * 100
                porcentagem_jogador_2 = (gols_marcados_jogador_2 / total_gols) * 100
            else:
                porcentagem_jogador_1 = 0
                porcentagem_jogador_2 = 0
              
    context = {'form': form, 
               'partidas': partidas,
               'vitorias_jogador_1': vitorias_jogador_1,
               'vitorias_jogador_2': vitorias_jogador_2,
               'gols_marcados_jogador_1': gols_marcados_jogador_1,
               'gols_marcados_jogador_2': gols_marcados_jogador_2,
               'porcentagem_jogador_1': porcentagem_jogador_1,
               'porcentagem_jogador_2': porcentagem_jogador_2
               }

    return render(request, 'principal/historico_confrontos.html', context)

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
    data_inicial = None
    data_final = None
    sequencia = []
    for partida in partidas:
        jogador = partida.detentor_atual
        if partida.detentor_atual == partida.determinar_vencedor():
            sequencia.append(partida)
            if len(sequencia) > maior_sequencia:
                maior_sequencia = len(sequencia)
                jogador_maior_sequencia = jogador
                data_inicial = sequencia[0].data
                data_final = sequencia[-1].data
        else:
            sequencia = []
    maior_sequencia = str(jogador_maior_sequencia) + ' (' + str(maior_sequencia) + ' defesas)'
    data_maior_sequencia = data_inicial.strftime('%d/%m/%Y') + ' a ' + data_final.strftime('%d/%m/%Y')
    
    # Streak (sequência de defesas) do detentor atual
    streak = 0
    for partida in partidas:
        if partida.detentor_atual == partida.determinar_vencedor():
            streak += 1
            data_final = partida.data
        else:
            streak = 0
            data_inicial = partida.data
    data_streak = data_inicial.strftime('%d/%m/%Y') + ' a ' + data_final.strftime('%d/%m/%Y')
    # ultimas 20 partidas
    ultimas_partidas = partidas.order_by('-id')[:20]
    # Criar o contexto
    context = {'detentor_atual': detentor_atual, 
               'ultimas_partidas': ultimas_partidas, 
               'defesas_cinturao': defesas_cinturao,
               'partida_maior_goleada': partida_maior_goleada,
               'maior_goleada': maior_goleada,
               'maior_sequencia': maior_sequencia,
               'data_maior_sequencia': data_maior_sequencia,
               'total_partidas': len(partidas),
               'streak': streak,
               'data_streak': data_streak,
               }

    return render(request, 'principal/index.html', context)

class PartidaListView(ListView):
    model = Partida
    template_name = 'principal/todas_partidas.html'
    def get_queryset(self):
        return Partida.objects.all()