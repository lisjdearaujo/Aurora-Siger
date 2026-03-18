# Missão Aurora Siger — Relatório Operacional de Pré-Decolagem

Projeto desenvolvido como atividade integradora da Fase 1 do curso de Ciência 
da Computação na FIAP, por Lisandra Araujo e Yury Alexander.

## Sobre o projeto

O objetivo foi simular o sistema de verificação pré-decolagem da nave Aurora Siger.
O script realiza a leitura dos dados de telemetria, executa as verificações de 
segurança em sequência e determina se a nave está apta para decolar ou se o 
lançamento deve ser abortado.

Os parâmetros verificados são:
- Temperatura interna (faixa segura: 18°C a 27°C)
- Temperatura externa (faixa segura: -50°C a 60°C)
- Integridade estrutural (1 = OK, 0 = FALHA)
- Nível de energia (mínimo 95%)
- Pressão dos tanques (faixa segura: 300 a 350 kPa)
- Módulos críticos (1 = todos online, 0 = falha)

## Como executar

1. Certifique-se de ter o Python 3 instalado
2. Clone este repositório:
   git clone https://github.com/lisjdearaujo/Aurora-Siger.git
3. Acesse a pasta do projeto
4. Execute o script:
   python aurora_siger.py
5. Informe os valores de telemetria quando solicitado

## Prints da execução

### Cenário 1 — Decolagem autorizada
[INSERIR PRINT]

### Cenário 2 — Decolagem abortada
[INSERIR PRINT]

## Estrutura do repositório

- aurora_siger.ipynb — Notebook Python com o script e a execução
- aurora_siger.py — Script Python isolado
- README.md — Documentação do projeto

## Tecnologias utilizadas

- Python 3
- Google Colab / Jupyter Notebook

## Instituição

FIAP — Fase 1 — Ciência da Computação — Março de 2026
