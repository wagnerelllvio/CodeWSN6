'''

'''

import random
import numpy as np
from config import AREA_LARGURA, AREA_ALTURA, NUM_SENSORES, RAIO_COBERTURA, DISTANCIA_MINIMA

# Gera uma posição aleatória dentro da área
def gerar_sensor():
    return [random.uniform(0, AREA_LARGURA), random.uniform(0, AREA_ALTURA)]

# Cria um indivíduo com NUM_SENSORES sensores
def criar_individuo():
    return [coord for _ in range(NUM_SENSORES) for coord in gerar_sensor()]

# Calcula cobertura da área pelos sensores (grid booleano)
def calcular_cobertura(sensores):
    x = np.arange(AREA_LARGURA)
    y = np.arange(AREA_ALTURA)
    xx, yy = np.meshgrid(x, y, indexing='ij')

    grid = np.zeros((AREA_LARGURA, AREA_ALTURA), dtype=bool)
    for sx, sy in sensores:
        distancia = (xx - sx) ** 2 + (yy - sy) ** 2
        grid |= distancia <= RAIO_COBERTURA ** 2  # Marca células cobertas

    area_coberta = np.sum(grid)
    area_total = AREA_LARGURA * AREA_ALTURA
    return area_coberta / area_total

# Penalidade se sensores estiverem muito próximos
def penalidade_distancia_minima(sensores):
    penalidade = 0
    n = len(sensores)
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.hypot(sensores[i][0] - sensores[j][0], sensores[i][1] - sensores[j][1])
            if dist < DISTANCIA_MINIMA:
                penalidade += (DISTANCIA_MINIMA - dist)
    return penalidade / (n * (n - 1) / 2)

# Avaliação: cobertura menos penalidade
def avaliar_individuo(individuo):
    sensores = [(individuo[i], individuo[i + 1]) for i in range(0, len(individuo), 2)]
    cobertura = calcular_cobertura(sensores)
    penalidade = penalidade_distancia_minima(sensores)
    return cobertura - penalidade,
