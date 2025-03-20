# Sistema de Análise de Crédito e Risco Financeiro

Sistema avançado de análise de crédito e avaliação de risco financeiro, utilizando técnicas de machine learning, análise preditiva e visualização de dados.

## Arquitetura do Sistema

```
credit-risk-analytics/
├── data/
│   ├── raw/                 # Dados brutos
│   ├── processed/           # Dados processados
│   └── warehouse/           # Data Warehouse
├── etl/
│   ├── extractors/         # Scripts de extração
│   ├── transformers/       # Scripts de transformação
│   └── loaders/            # Scripts de carga
├── models/
│   ├── risk/              # Modelos de risco
│   ├── credit/            # Modelos de crédito
│   └── fraud/             # Detecção de fraude
├── api/                   # API REST
├── dashboard/             # Interface de visualização
└── docs/                  # Documentação
```

## Funcionalidades Principais

1. **Análise de Risco**
   - Scoring de crédito
   - Avaliação de risco
   - Análise de inadimplência
   - Monitoramento de carteira

2. **Previsão de Crédito**
   - Modelos de default
   - Análise de tendências
   - Previsão de inadimplência
   - Análise de recuperação

3. **Detecção de Fraude**
   - Análise de padrões
   - Detecção de anomalias
   - Monitoramento em tempo real
   - Alertas automáticos

4. **Visualização de Dados**
   - Dashboards interativos
   - Relatórios automatizados
   - Análise exploratória
   - KPIs em tempo real

## Tecnologias Utilizadas

- **Backend**: Python, FastAPI, SQLAlchemy
- **Banco de Dados**: PostgreSQL, ClickHouse
- **ETL**: Apache Airflow, dbt
- **ML**: scikit-learn, XGBoost, LightGBM
- **Visualização**: Dash, Plotly
- **Infraestrutura**: Docker, Kubernetes
- **Cloud**: AWS (Redshift, S3, EMR)
- **Segurança**: OAuth2, JWT

## Instalação e Configuração

1. Clone o repositório:
```bash
git clone https://github.com/brunoxabreu/credit-risk-analytics.git
cd credit-risk-analytics
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
- Cliente
- Produto
- Tempo
- Região
- Agência
- Canal

### Fatos
- Operações
- Pagamentos
- Inadimplência
- Recuperação
- Fraude

## Modelos de Risco

1. **Scoring de Crédito**
   - Random Forest
   - XGBoost
   - LightGBM
   - Ensemble Methods

2. **Previsão de Default**
   - Survival Analysis
   - Time Series
   - Deep Learning

3. **Detecção de Fraude**
   - Isolation Forest
   - Autoencoders
   - Anomaly Detection

## API Endpoints

### Análise de Risco
- `/api/v1/risk/score`
- `/api/v1/risk/portfolio`
- `/api/v1/risk/trends`

### Crédito
- `/api/v1/credit/analysis`
- `/api/v1/credit/forecast`
- `/api/v1/credit/recovery`

### Fraude
- `/api/v1/fraud/detection`
- `/api/v1/fraud/alerts`
- `/api/v1/fraud/patterns`

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 