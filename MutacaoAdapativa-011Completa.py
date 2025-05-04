import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Configurações iniciais
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

DIM = 10
POP_SIZE = 50
GENERATIONS = 100
SIGMA_INIT = 1.0
SIGMA_MIN = 0.01
ADAPT_RATE = 0.03

def sphere(individual):
    return sum(x**2 for x in individual),

def adaptive_sigma(gen):
    return max(SIGMA_INIT * np.exp(-ADAPT_RATE * gen), SIGMA_MIN)

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

def population_diversity(pop):
    distances = []
    for i in range(len(pop)):
        for j in range(i + 1, len(pop)):
            dist = np.linalg.norm(np.array(pop[i]) - np.array(pop[j]))
            distances.append(dist)
    return np.mean(distances) if distances else 0.0

def run_ga(label, sigma_func):
    toolbox = setup_toolbox(sigma_func)
    pop = toolbox.population(n=POP_SIZE)
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    best_fits, mean_fits, diversities, sigmas = [], [], [], []

    for gen in range(GENERATIONS):
        sigma = sigma_func(gen)
        sigmas.append(sigma)
        toolbox.unregister("mutate")
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=sigma, indpb=1.0/DIM)

        offspring = algorithms.varAnd(pop, toolbox, cxpb=0.5, mutpb=0.2)
        for ind in offspring:
            ind.fitness.values = toolbox.evaluate(ind)

        pop = toolbox.select(offspring, k=len(pop))
        fits = [ind.fitness.values[0] for ind in pop]

        best_fits.append(min(fits))
        mean_fits.append(np.mean(fits))
        diversities.append(population_diversity(pop))

    return best_fits, mean_fits, diversities, sigmas

# Execução
best_fits, mean_fits, diversities, sigmas = run_ga("σ adaptativo", adaptive_sigma)

# Visualização
plt.figure(figsize=(15, 8))

plt.subplot(2, 2, 1)
plt.plot(best_fits, label="Melhor Fitness")
plt.plot(mean_fits, label="Fitness Médio")
plt.xlabel("Geração")
plt.ylabel("Fitness")
plt.title("Fitness da População")
plt.grid(True)
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(sigmas, color='orange')
plt.xlabel("Geração")
plt.ylabel("σ")
plt.title("Evolução do σ Adaptativo")
plt.grid(True)

plt.subplot(2, 2, 3)
plt.plot(diversities, color='green')
plt.xlabel("Geração")
plt.ylabel("Diversidade Média")
plt.title("Diversidade Populacional")
plt.grid(True)

plt.tight_layout()
plt.show()
