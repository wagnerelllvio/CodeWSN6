'''
Código Python com DEAP: comparação entre σ constante e adaptativo

'''

import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Parâmetros gerais
DIM = 10
POP_SIZE = 50
GENERATIONS = 100
SIGMA_CONST = 1.0
SIGMA_INIT = 1.0
SIGMA_MIN = 0.01
ADAPT_RATE = 0.03  # Taxa de decaimento do sigma adaptativo

# Função objetivo: esfera
def sphere(individual):
    return sum(x**2 for x in individual),

# Estratégia de decaimento exponencial para sigma
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

# Executa o algoritmo genético com mutação customizada
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

# Execução das duas variantes
toolbox = setup_toolbox(lambda gen: SIGMA_CONST)
const_results = run_ga("σ constante", lambda gen: SIGMA_CONST)

toolbox = setup_toolbox(adaptive_sigma)
adapt_results = run_ga("σ adaptativo", adaptive_sigma)

# Plot dos resultados
plt.plot(const_results, label="σ constante")
plt.plot(adapt_results, label="σ adaptativo")
plt.xlabel("Geração")
plt.ylabel("Melhor Fitness")
plt.title("Comparação: σ constante vs σ adaptativo")
plt.legend()
plt.grid(True)
plt.show()
