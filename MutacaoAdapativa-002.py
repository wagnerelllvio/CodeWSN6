'''
Código Python com DEAP (σ alto, σ baixo, σ adaptativo)

Interpretação:
Sigma alto: tende a oscilar sem convergir.
Sigma baixo: converge rápido, mas pode ficar preso.
Sigma adaptativo: começa com amplitude e termina com refinamento, geralmente obtendo o melhor resultado.
'''

import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Parâmetros gerais
DIM = 10
POP_SIZE = 50
GENERATIONS = 100
SIGMA_HIGH = 1.0       # σ alto (constante)
SIGMA_LOW = 0.01       # σ baixo (constante)
SIGMA_INIT = 1.0       # σ inicial para adaptativo
SIGMA_MIN = 0.01       # σ mínimo para adaptativo
ADAPT_RATE = 0.03      # Taxa de decaimento

# Função objetivo: esfera
def sphere(individual):
    return sum(x**2 for x in individual),

# Estratégia de sigma adaptativo: decaimento exponencial
def adaptive_sigma(gen):
    return max(SIGMA_INIT * np.exp(-ADAPT_RATE * gen), SIGMA_MIN)

# Setup DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

def setup_toolbox(mut_sigma_func):
    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.uniform, -5, 5)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, n=DIM)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", sphere)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=mut_sigma_func(0), indpb=1.0/DIM)
    toolbox.register("select", tools.selTournament, tournsize=3)
    return toolbox

# Executa o algoritmo genético com a função de mutação definida
def run_ga(label, sigma_func):
    pop = toolbox.population(n=POP_SIZE)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    best_fits = []
    for gen in range(GENERATIONS):
        sigma = sigma_func(gen)
        toolbox.unregister("mutate")
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=sigma, indpb=1.0/DIM)

        offspring = algorithms.varAnd(pop, toolbox, cxpb=0.5, mutpb=0.2)

        fitnesses = list(map(toolbox.evaluate, offspring))
        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = fit

        pop = toolbox.select(offspring, k=len(pop))
        best = tools.selBest(pop, k=1)[0]
        best_fits.append(best.fitness.values[0])
    return best_fits

# Roda os três cenários
toolbox = setup_toolbox(lambda gen: SIGMA_HIGH)
high_results = run_ga("σ constante alto", lambda gen: SIGMA_HIGH)

toolbox = setup_toolbox(lambda gen: SIGMA_LOW)
low_results = run_ga("σ constante baixo", lambda gen: SIGMA_LOW)

toolbox = setup_toolbox(adaptive_sigma)
adaptive_results = run_ga("σ adaptativo", adaptive_sigma)

# Plot dos resultados
plt.figure(figsize=(10, 6))
plt.plot(high_results, label="σ constante alto (1.0)")
plt.plot(low_results, label="σ constante baixo (0.01)")
plt.plot(adaptive_results, label="σ adaptativo (1.0 → 0.01)")
plt.xlabel("Geração")
plt.ylabel("Melhor Fitness")
plt.title("Comparação de Estratégias de Mutação com σ Variável")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
