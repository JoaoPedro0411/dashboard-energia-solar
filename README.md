# Dashboard de Energia Solar

Dashboard interativo para explorar indicadores de energia solar por estado dos Estados Unidos, construído com Python, pandas e Plotly Dash.

## O que demonstra

- Leitura e preparação de dados tabulares com pandas
- Visualização interativa com Plotly
- Interface web responsiva com Dash e Bootstrap
- Tabela pesquisável, filtrável e ordenável com Dash AG Grid
- Organização simples entre aplicação, dados e dependências

## Funcionalidades

- Seletor para comparar quantidade de usinas, capacidade instalada, média por usina e geração
- Gráfico de barras ordenado pelo indicador selecionado
- Indicadores resumidos calculados a partir dos dados carregados
- Tabela com filtro, ordenação e paginação
- Layout responsivo para telas menores

## Dados e limitações

O arquivo `data/solar.csv` contém oito registros estaduais e cinco colunas. O repositório de origem não informava a fonte nem a data de referência do conjunto. Por isso, este projeto é apresentado como demonstração técnica de exploração e visualização, e os números não devem ser tratados como um retrato completo ou atual da geração solar nos Estados Unidos.

## Tecnologias

- Python 3.11 ou superior
- pandas
- Plotly
- Dash
- Dash Bootstrap Components
- Dash AG Grid

## Como executar

1. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

   Linux/macOS:

   ```bash
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Inicie o dashboard:

   ```bash
   python app.py
   ```

4. Abra o endereço local exibido no terminal.

## Estrutura

```text
.
├── app.py
├── data/
│   └── solar.csv
├── requirements.txt
└── README.md
```

## Próximas melhorias

- Registrar a fonte, a licença e o período de referência dos dados
- Ampliar o conjunto de dados e validar os valores na ingestão
- Acrescentar testes para agregações e leitura do CSV
- Publicar uma demonstração hospedada

## Contexto

Projeto acadêmico de visualização e análise exploratória de dados.
