# Sistema de Análise de Vendas e Previsão de Demanda para Varejo

Sistema avançado de análise de vendas e previsão de demanda para varejo, utilizando técnicas de OLAP, análise preditiva e visualização de dados.

## Arquitetura do Sistema

```
retail-analytics/
├── data/
│   ├── raw/                 # Dados brutos
│   ├── processed/           # Dados processados
│   └── warehouse/           # Data Warehouse
├── etl/
│   ├── extractors/         # Scripts de extração
│   ├── transformers/       # Scripts de transformação
│   └── loaders/            # Scripts de carga
├── models/
│   ├── olap/              # Modelos OLAP
│   ├── ml/                # Modelos de Machine Learning
│   └── forecasting/       # Modelos de previsão
├── api/                   # API REST
├── dashboard/             # Interface de visualização
└── docs/                  # Documentação
```

## Funcionalidades Principais

1. **Análise OLAP**
   - Cubos de dados multidimensionais
   - Análise de vendas por dimensões (tempo, produto, região)
   - Drill-down e roll-up
   - Análise de tendências

2. **Previsão de Demanda**
   - Modelos de séries temporais
   - Análise de sazonalidade
   - Previsão de vendas
   - Análise de tendências

3. **Visualização de Dados**
   - Dashboards interativos
   - Relatórios automatizados
   - Análise exploratória
   - KPIs em tempo real

4. **Integração de Dados**
   - ETL automatizado
   - Integração com múltiplas fontes
   - Pipeline de dados em tempo real
   - Governança de dados

## Tecnologias Utilizadas

- **Backend**: Python, FastAPI, SQLAlchemy
- **Banco de Dados**: PostgreSQL, ClickHouse
- **ETL**: Apache Airflow, dbt
- **OLAP**: Apache Druid, Apache Kylin
- **ML**: scikit-learn, Prophet, TensorFlow
- **Visualização**: Dash, Plotly
- **Infraestrutura**: Docker, Kubernetes
- **Cloud**: AWS (Redshift, S3, EMR)

## Instalação e Configuração

1. Clone o repositório:
```bash
git clone https://github.com/brunoxabreu/retail-analytics.git
cd retail-analytics
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
- Cliente
- Região
- Loja
- Promoção

### Fatos
- Vendas
- Estoque
- Devoluções
- Custos

## Modelos de Previsão

1. **Séries Temporais**
   - ARIMA
   - Prophet
   - LSTM

2. **Análise de Demanda**
   - Regressão
   - Random Forest
   - XGBoost

3. **Análise de Sazonalidade**
   - Decomposição
   - Análise de tendências
   - Detecção de padrões

## API Endpoints

### Análise OLAP
- `/api/v1/olap/sales`
- `/api/v1/olap/inventory`
- `/api/v1/olap/forecast`

### Previsão
- `/api/v1/forecast/demand`
- `/api/v1/forecast/trends`
- `/api/v1/forecast/seasonality`

### Relatórios
- `/api/v1/reports/sales`
- `/api/v1/reports/inventory`
- `/api/v1/reports/performance`

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 