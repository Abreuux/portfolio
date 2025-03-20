# Painel Corporativo

Sistema de dashboard corporativo desenvolvido com Dash e Flask, integrando múltiplas fontes de dados através de ETL com Apache Airflow.

## Funcionalidades

- Dashboard interativo com KPIs e métricas
- Integração com múltiplas fontes de dados:
  - Facebook Ads
  - Google Ads
  - CRM Bitrix24
  - Protheus
  - Intercom
  - Stripe
- Processamento ETL automatizado
- Visualizações de dados em tempo real
- Monitoramento de campanhas
- Análise de performance
- Gestão de clientes
- Suporte ao cliente

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- Apache Airflow 2.8+
- Contas e chaves de API para:
  - Facebook Ads
  - Google Ads
  - Bitrix24
  - Protheus
  - Intercom
  - Stripe

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/corporate-dashboard.git
cd corporate-dashboard
```

2. Crie um ambiente virtual:
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

5. Configure o banco de dados:
```sql
CREATE DATABASE corporate_dashboard;
```

6. Configure o Apache Airflow:
```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init
airflow users create
```

7. Inicie o Airflow:
```bash
airflow webserver
airflow scheduler
```

8. Inicie a aplicação Dash:
```bash
python app.py
```

## Configuração

### Variáveis de Ambiente

- `FACEBOOK_ACCESS_TOKEN`: Token de acesso da API do Facebook
- `GOOGLE_ADS_CLIENT_ID`: ID do cliente do Google Ads
- `BITRIX24_WEBHOOK_URL`: URL do webhook do Bitrix24
- `PROTHEUS_API_KEY`: Chave de API do Protheus
- `INTERCOM_ACCESS_TOKEN`: Token de acesso do Intercom
- `STRIPE_SECRET_KEY`: Chave secreta do Stripe
- `DATABASE_URL`: URL de conexão com o banco de dados

### ETL Process

O sistema utiliza Apache Airflow para orquestrar o processo ETL:

1. Extração de dados das fontes
2. Transformação e limpeza dos dados
3. Carregamento no banco de dados
4. Atualização do dashboard

## Estrutura do Projeto

```
corporate-dashboard/
├── app.py                 # Aplicação principal Dash
├── requirements.txt       # Dependências do projeto
├── dags/                 # DAGs do Airflow
│   └── corporate_etl.py  # DAG principal
├── templates/            # Templates HTML
│   └── index.html       # Template principal
├── static/              # Arquivos estáticos
└── data/               # Dados processados
```

## API Endpoints

- `GET /api/kpis`: Retorna KPIs principais
- `GET /api/revenue`: Dados de receita
- `GET /api/customers`: Dados de clientes
- `GET /api/campaigns`: Dados de campanhas
- `GET /api/support`: Dados de suporte

## Monitoramento

O sistema inclui:

- Logs detalhados do ETL
- Monitoramento de performance
- Alertas de erro
- Métricas de uso

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 