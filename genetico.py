# genetico.py

import random
from deap import base, creator, tools
from multiprocessing import Pool, cpu_count
from tqdm import trange
import numpy as np
import time

# Importações internas
from utils import criar_individuo, avaliar_individuo
from config import AREA_LARGURA, AREA_ALTURA

# === Configuração da DEAP ===

# Define o tipo de problema (Maximização)
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
# Define o indivíduo como uma lista com um atributo de fitness
creator.create("Individual", list, fitness=creator.FitnessMax)

# Configurações do toolbox
toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, criar_individuo)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", avaliar_individuo)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("select", tools.selTournament, tournsize=3)

# === Função de mutação adaptativa ===
def mutar_com_limites_adaptativo(individual, mu=0, sigma=5, indpb=0.2, geracao=0, max_geracoes=100):
    """
    Aplica uma mutação gaussiana com adaptação da intensidade ao longo das gerações.
    """
    size = len(individual)
    sigma_atual = sigma * (1 - geracao / max_geracoes)
    sigma_atual = max(sigma_atual, 0.5)  # Garante um mínimo de perturbação

    for i in range(size):
        if random.random() < indpb:
            individual[i] += random.gauss(mu, sigma_atual)
            # Clamping: mantém o gene dentro dos limites da área
            if i % 2 == 0:  # coordenada x
                individual[i] = np.clip(individual[i], 0, AREA_LARGURA)
            else:           # coordenada y
                individual[i] = np.clip(individual[i], 0, AREA_ALTURA)

    return individual,

# === Melhoramento local via Hill Climbing ===
def hill_climb(individual, passos=20, intensidade=0.5):
    """
    Aplica hill climbing no melhor indivíduo encontrado pelo GA.
    """
    melhor = creator.Individual(individual[:])
    melhor_fit = avaliar_individuo(melhor)[0]

    for _ in range(passos):
        vizinho = creator.Individual(melhor[:])
        mutar_com_limites_adaptativo(vizinho, sigma=intensidade, geracao=100, max_geracoes=100)
        vizinho_fit = avaliar_individuo(vizinho)[0]

        if vizinho_fit > melhor_fit:
            melhor = vizinho
            melhor_fit = vizinho_fit

    return melhor, melhor_fit

# === Execução principal do Algoritmo Genético ===
def executar_ga(n_individuos=50, n_geracoes=100):
    """
    Executa o algoritmo genético com mutação adaptativa, elitismo, paralelismo e pós-processamento via hill climbing.
    """
    # Inicializa pool para paralelizar avaliações de fitness
    pool = Pool(processes=cpu_count())
    toolbox.register("map", pool.map)

    # Cria a população inicial
    populacao = toolbox.population(n=n_individuos)
    historico_cobertura = []

    # Marca o início da execução
    start_time = time.time()

    # Avalia a população inicial
    fitnesses = list(toolbox.map(toolbox.evaluate, populacao))
    for ind, fit in zip(populacao, fitnesses):
        ind.fitness.values = fit

    # Loop principal de evolução
    for gen in trange(n_geracoes, desc="Evoluindo as gerações"):
        filhos = []

        # Elitismo: mantém o melhor indivíduo da geração anterior
        elite = tools.selBest(populacao, 1)[0]
        filhos.append(toolbox.clone(elite))

        # Crossover e mutação
        for ind1, ind2 in zip(populacao[::2], populacao[1::2]):
            child1, child2 = toolbox.clone(ind1), toolbox.clone(ind2)
            if random.random() < 0.5:
                toolbox.mate(child1, child2)
            mutar_com_limites_adaptativo(child1, sigma=5, geracao=gen, max_geracoes=n_geracoes)
            mutar_com_limites_adaptativo(child2, sigma=5, geracao=gen, max_geracoes=n_geracoes)
            filhos.append(child1)
            filhos.append(child2)

        # Garante que a nova geração tenha o mesmo tamanho da população original
        filhos = filhos[:len(populacao)]

        # Avalia os filhos
        fitnesses = list(toolbox.map(toolbox.evaluate, filhos))
        for ind, fit in zip(filhos, fitnesses):
            ind.fitness.values = fit

        # Seleciona a nova população com torneio
        populacao[:] = toolbox.select(filhos, k=len(populacao))

        # Salva o melhor indivíduo da geração para análise
        melhor_geracao = tools.selBest(populacao, 1)[0]
        historico_cobertura.append(melhor_geracao.fitness.values[0])

    tempo_execucao = time.time() - start_time

    # Aplica hill climbing no melhor indivíduo após evolução
    melhor = tools.selBest(populacao, 1)[0]
    melhor_aprimorado, melhor_fitness = hill_climb(melhor)

    # Finaliza os processos do pool
    pool.close()
    pool.join()

    # Retorna melhor indivíduo, fitness, tempo de execução e histórico
    return melhor_aprimorado, melhor_fitness, tempo_execucao, historico_cobertura
