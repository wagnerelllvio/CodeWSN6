# visualizacao.py
'''

'''

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from config import RAIO_COBERTURA, AREA_LARGURA, AREA_ALTURA

def plotar_convergencia(historico, melhor_fitness, tempo_exec):
    """
    Plota o gráfico de convergência da cobertura ao longo das gerações.
    """
    plt.figure(figsize=(10, 4))
    plt.plot(historico, marker='o', linestyle='-', color='blue')
    plt.title("Evolução da Cobertura ao Longo das Gerações")
    plt.xlabel("Geração")
    plt.ylabel("Cobertura")
    plt.grid(True)

    info_text = f"Melhor cobertura: {melhor_fitness*100:.2f}%\nTempo de execução: {tempo_exec:.2f} s"
    props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='black')
    plt.gca().text(0.65, 0.05, info_text, transform=plt.gca().transAxes, fontsize=10,
                   verticalalignment='bottom', bbox=props)

    plt.tight_layout()
    plt.show()
'''
def plotar_sensores(individuo, melhor_fitness=None, tempo_exec=None, titulo="Distribuição dos Sensores"):
    """
    Plota a posição dos sensores e suas áreas de cobertura circulares.
    """
    sensores = [(individuo[i], individuo[i + 1]) for i in range(0, len(individuo), 2)]

    fig, ax = plt.subplots(figsize=(6, 6))
    for x, y in sensores:
        circulo = Circle((x, y), RAIO_COBERTURA, color='green', alpha=0.2)
        ax.add_patch(circulo)
        ax.plot(x, y, 'ko', markersize=3)

    ax.set_xlim(0, AREA_LARGURA)
    ax.set_ylim(0, AREA_ALTURA)
    ax.set_title(titulo)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect('equal')
    ax.grid(True)

    # Adiciona a caixa de informação somente se os dados forem fornecidos
    if melhor_fitness is not None and tempo_exec is not None:
        info_text = f"Melhor cobertura: {melhor_fitness * 100:.2f}%\nTempo de execução: {tempo_exec:.2f} s"
        props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='black')
        plt.gca().text(0.65, 0.05, info_text, transform=plt.gca().transAxes, fontsize=10,
                       verticalalignment='bottom', bbox=props)

    plt.tight_layout()
    plt.show()

def plotar_sensores(individuo, melhor_fitness=None, tempo_exec=None, titulo="Distribuição dos Sensores"):
    """
    Plota a posição dos sensores e suas áreas de cobertura circulares.
    Exibe a legenda de cobertura e tempo fora da área de plotagem.
    """
    sensores = [(individuo[i], individuo[i + 1]) for i in range(0, len(individuo), 2)]

    fig, ax = plt.subplots(figsize=(6, 6))
    for x, y in sensores:
        circulo = Circle((x, y), RAIO_COBERTURA, color='green', alpha=0.2)
        ax.add_patch(circulo)
        ax.plot(x, y, 'ko', markersize=3)

    ax.set_xlim(0, AREA_LARGURA)
    ax.set_ylim(0, AREA_ALTURA)
    ax.set_title(titulo)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect('equal')
    ax.grid(True)

    if melhor_fitness is not None and tempo_exec is not None:
        info_text = f"Melhor cobertura: {melhor_fitness * 100:.2f}%\nTempo de execução: {tempo_exec:.2f} s"
        props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='black')

        # Adiciona a legenda fora do gráfico, abaixo do eixo X
        fig.text(0.5, 0.01, info_text, ha='center', va='bottom', fontsize=10, bbox=props)

    plt.tight_layout(rect=[0, 0.05, 1, 1])  # Ajusta layout para acomodar texto fora do eixo
    plt.show()
    '''


'''
  Atualização da função plotar_sensores com conexões entre sensores próximos:
'''
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from config import RAIO_COBERTURA, AREA_LARGURA, AREA_ALTURA
import numpy as np
from itertools import combinations

def plotar_sensores(individuo, melhor_fitness=None, tempo_exec=None, titulo="Distribuição dos Sensores"):
    """
    Plota a posição dos sensores e suas áreas de cobertura circulares.
    Conecta sensores que estão a uma distância menor que 2 * raio de cobertura.
    """
    sensores = [(individuo[i], individuo[i + 1]) for i in range(0, len(individuo), 2)]

    fig, ax = plt.subplots(figsize=(6, 6))

    # Desenha conexões entre sensores próximos
    for (x1, y1), (x2, y2) in combinations(sensores, 2):
        distancia = np.hypot(x2 - x1, y2 - y1)
        if distancia < 2 * RAIO_COBERTURA:
            #ax.plot([x1, x2], [y1, y2], 'gray', linewidth=0.5, alpha=0.4)
            ax.plot([x1, x2], [y1, y2], 'red', linewidth=2.5, alpha=0.4)

    # Desenha sensores e suas áreas de cobertura
    for x, y in sensores:
        circulo = Circle((x, y), RAIO_COBERTURA, color='green', alpha=0.2)
        ax.add_patch(circulo)
        ax.plot(x, y, 'ko', markersize=3)

    ax.set_xlim(0, AREA_LARGURA)
    ax.set_ylim(0, AREA_ALTURA)
    ax.set_title(titulo)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect('equal')
    ax.grid(True)

    # Informações de cobertura e tempo abaixo do gráfico
    if melhor_fitness is not None and tempo_exec is not None:
        info_text = f"Melhor cobertura: {melhor_fitness * 100:.2f}%\nTempo de execução: {tempo_exec:.2f} s"
        props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='black')
        fig.text(0.5, 0.01, info_text, ha='center', va='bottom', fontsize=10, bbox=props)

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.show()

'''
'''
def plotar_grafo_conectividade(individuo, titulo="Conectividade entre Sensores", tempo_exec=None, melhor_fitness=None):
    """
    Plota apenas os centros dos sensores e as linhas entre sensores próximos.
    """
    import matplotlib.pyplot as plt
    from math import sqrt

    sensores = [(individuo[i], individuo[i + 1]) for i in range(0, len(individuo), 2)]
    limiar_conexao = 2 * RAIO_COBERTURA

    fig, ax = plt.subplots(figsize=(6, 6))

    # Conexões entre sensores próximos
    for i in range(len(sensores)):
        for j in range(i + 1, len(sensores)):
            x1, y1 = sensores[i]
            x2, y2 = sensores[j]
            distancia = sqrt((x1 - x2)**2 + (y1 - y2)**2)
            if distancia <= limiar_conexao:
                ax.plot([x1, x2], [y1, y2], color='red', linewidth=1.2, alpha=0.7)

    # Centros dos sensores
    for x, y in sensores:
        ax.plot(x, y, 'ko', markersize=3)

    ax.set_xlim(0, AREA_LARGURA)
    ax.set_ylim(0, AREA_ALTURA)
    ax.set_title(titulo)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect('equal')
    ax.grid(True)

    if melhor_fitness is not None and tempo_exec is not None:
        info_text = f"Melhor cobertura: {melhor_fitness * 100:.2f}%\nTempo de execução: {tempo_exec:.2f} s"
        props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='black')
        plt.gca().text(0.5, -0.1, info_text, transform=plt.gca().transAxes, fontsize=10,
                       verticalalignment='top', horizontalalignment='center', bbox=props)

    plt.tight_layout()
    plt.show()
