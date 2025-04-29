# testes/test_utils.py

import pytest
from utils import criar_individuo, avaliar_individuo, calcular_cobertura, penalidade_distancia_minima
from config import NUM_SENSORES, AREA_LARGURA, AREA_ALTURA, DISTANCIA_MINIMA

# Teste de criação de indivíduo
def test_criar_individuo_valido():
    individuo = criar_individuo()
    assert isinstance(individuo, list)
    assert len(individuo) == 2 * NUM_SENSORES
    for i in range(0, len(individuo), 2):
        x = individuo[i]
        y = individuo[i + 1]
        assert 0 <= x <= AREA_LARGURA
        assert 0 <= y <= AREA_ALTURA

# Teste de avaliação de indivíduo (fitness)
def test_avaliar_individuo_valido():
    individuo = criar_individuo()
    fitness = avaliar_individuo(individuo)
    assert isinstance(fitness, tuple)
    assert isinstance(fitness[0], float)
    assert -1.0 <= fitness[0] <= 1.0  # cobertura - penalidade

# Teste de penalidade por distância mínima
def test_penalidade_distancia_minima():
    sensores_proximos = [(0, 0), (0, 1)]  # muito próximos
    penalidade = penalidade_distancia_minima(sensores_proximos)
    assert penalidade > 0

    sensores_distantes = [(0, 0), (DISTANCIA_MINIMA + 5, 0)]
    penalidade = penalidade_distancia_minima(sensores_distantes)
    assert penalidade == 0

# Teste de cálculo de cobertura
def test_calcular_cobertura_limites():
    sensores = [(AREA_LARGURA / 2, AREA_ALTURA / 2)]
    cobertura = calcular_cobertura(sensores)
    assert isinstance(cobertura, float)
    assert 0 <= cobertura <= 1
