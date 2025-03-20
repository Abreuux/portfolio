# Sistema de Análise de Logística e Supply Chain

Sistema avançado de análise de logística e cadeia de suprimentos, utilizando técnicas de otimização, análise preditiva e visualização de dados.

## Arquitetura do Sistema

```
supply-chain-analytics/
├── data/
│   ├── raw/                 # Dados brutos
│   ├── processed/           # Dados processados
│   └── warehouse/           # Data Warehouse
├── etl/
│   ├── extractors/         # Scripts de extração
│   ├── transformers/       # Scripts de transformação
│   └── loaders/            # Scripts de carga
├── models/
│   ├── optimization/       # Modelos de otimização
│   ├── forecasting/        # Modelos de previsão
│   └── analytics/          # Análise de dados
├── api/                   # API REST
├── dashboard/             # Interface de visualização
└── docs/                  # Documentação
```

## Funcionalidades Principais

1. **Otimização de Operações**
   - Roteirização
   - Gestão de estoque
   - Planejamento de capacidade
   - Otimização de custos

2. **Previsão de Demanda**
   - Modelos de séries temporais
   - Análise de sazonalidade
   - Previsão de vendas
   - Análise de tendências

3. **Gestão de Supply Chain**
   - Análise de fornecedores
   - Gestão de pedidos
   - Monitoramento de entregas
   - Análise de performance

4. **Visualização de Dados**
   - Dashboards interativos
   - Relatórios automatizados
   - Análise exploratória
   - KPIs em tempo real

## Tecnologias Utilizadas

- **Backend**: Python, FastAPI, SQLAlchemy
- **Banco de Dados**: PostgreSQL, ClickHouse
- **ETL**: Apache Airflow, dbt
- **ML**: scikit-learn, Prophet, TensorFlow
- **Otimização**: OR-Tools, PuLP
- **Visualização**: Dash, Plotly
- **Infraestrutura**: Docker, Kubernetes
- **Cloud**: AWS (Redshift, S3, EMR)

## Instalação e Configuração

1. Clone o repositório:
```bash
git clone https://github.com/brunoxabreu/supply-chain-analytics.git
cd supply-chain-analytics
```

2. Configure o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicie os serviços:
```bash
docker-compose up -d
```

## Estrutura do Data Warehouse

### Dimensões
- Tempo
- Produto
- Fornecedor
- Cliente
- Região
- Centro de Distribuição

### Fatos
- Pedidos
- Entregas
- Estoque
- Custos
- Performance

## Modelos de Otimização

1. **Roteirização**
   - Vehicle Routing Problem (VRP)
   - Traveling Salesman Problem (TSP)
   - Capacitated VRP
   - Time Windows VRP

2. **Gestão de Estoque**
   - Economic Order Quantity (EOQ)
   - Reorder Point
   - Safety Stock
   - ABC Analysis

3. **Previsão de Demanda**
   - ARIMA
   - Prophet
   - LSTM
   - Ensemble Methods

## API Endpoints

### Otimização
- `/api/v1/optimization/routes`
- `/api/v1/optimization/inventory`
- `/api/v1/optimization/capacity`

### Previsão
- `/api/v1/forecast/demand`
- `/api/v1/forecast/trends`
- `/api/v1/forecast/seasonality`

### Supply Chain
- `/api/v1/supply/orders`
- `/api/v1/supply/deliveries`
- `/api/v1/supply/performance`

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 