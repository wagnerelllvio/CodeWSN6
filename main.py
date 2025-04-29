# main.py
'''
Versao 1.0

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
from visualizacao import plotar_convergencia, plotar_sensores

if __name__ == '__main__':
    melhor_solucao, melhor_fitness, tempo_exec, historico = executar_ga()

    print(f"\nMelhor cobertura encontrada: {melhor_fitness:.4f}")
    print(f"Tempo de execução: {tempo_exec:.2f} segundos")

    plotar_convergencia(historico, melhor_fitness, tempo_exec)
    plotar_sensores(melhor_solucao, titulo="Melhor Distribuição de Sensores")



# main.py
''' 
from genetico import executar_ga
from visualizacao import plotar_convergencia, plotar_sensores

if __name__ == '__main__':
    melhor_solucao, melhor_fitness, tempo_exec, historico = executar_ga()

    print(f"\nMelhor cobertura encontrada: {melhor_fitness:.4f}")
    print(f"Tempo de execução: {tempo_exec:.2f} segundos")

    plotar_convergencia(historico, melhor_fitness, tempo_exec)
    plotar_sensores(melhor_solucao, titulo="Melhor Distribuição de Sensores")

'''
