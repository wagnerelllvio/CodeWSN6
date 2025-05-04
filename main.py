# main.py
'''
Versao 1.0

02/02/2025

sensor_coverage_ga/
├── config.py                  # Parâmetros padrão do problema (dimensões, sensores, etc.)
├── genetico.py               # Lógica principal do Algoritmo Genético (GA)
├── main.py                   # Execução principal com argparse e integração de módulos
├── utils.py                  # Funções utilitárias (gerar sensores, avaliar, etc.)
├── visualizacao.py           # Gráficos: convergência + distribuição 2D dos sensores
├── registros.py              # Exportação de resultados em JSON, CSV, PNG
├── testes/
│   └── test_utils.py         # Testes unitários para funções críticas com pytest
├── resultados/
│   ├── sensores_melhor_solucao.json
│   ├── sensores_melhor_solucao.csv
│   ├── grafico_convergencia.png
│   └── log_execucao.txt
├── parametros.yaml           # Alternativa ao config.py com parâmetros ajustáveis
├── README.md                 # Descrição do projeto, instruções de uso
└── requirements.txt          # Dependências do projeto

'''
from genetico import executar_ga
from visualizacao import plotar_convergencia, plotar_sensores, plotar_grafo_conectividade

if __name__ == '__main__':
    # Executa o algoritmo genético
    melhor_solucao, melhor_fitness, tempo_exec, historico = executar_ga()

    # Exibe os resultados no terminal
    print(f"\nMelhor cobertura encontrada: {melhor_fitness:.4f}")
    print(f"Tempo de execução: {tempo_exec:.2f} segundos")

    # Plota a curva de convergência
    plotar_convergencia(historico, melhor_fitness, tempo_exec)

    # Plota a melhor solução encontrada com informações
    plotar_sensores(melhor_solucao, melhor_fitness=melhor_fitness, tempo_exec=tempo_exec,
                    titulo="Melhor Distribuição de Sensores")

    # Plota o grafico  plotar_grafo_conectividade
    plotar_grafo_conectividade(melhor_solucao, tempo_exec=tempo_exec, melhor_fitness=melhor_fitness)

