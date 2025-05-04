# visualizacao.py

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
