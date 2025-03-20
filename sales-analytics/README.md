# Sales Analytics Dashboard

Um dashboard simples e efetivo para análise de vendas, desenvolvido com Python, SQL e Power BI. Este projeto demonstra a implementação de uma solução de BI completa, desde a extração de dados até a visualização.

## Estrutura do Projeto

```
portfolio/
├── data/                  # Dados de exemplo e arquivos CSV
├── src/                   # Código fonte
│   ├── etl/              # Scripts de extração e transformação
│   ├── analysis/         # Análises e previsões
│   └── utils/            # Funções utilitárias e configurações
├── tests/                # Testes unitários
├── docs/                 # Documentação
├── dashboard/           # Arquivos do Power BI
└── logs/                # Arquivos de log
```

## Funcionalidades

- **ETL de Dados**
  - Extração de dados de vendas
  - Limpeza e transformação
  - Armazenamento em banco de dados

- **Análise de Vendas**
  - Cálculo de KPIs diários
  - Previsão de vendas para próximos 7 dias
  - Análise de tendências

- **Monitoramento**
  - Alertas automáticos via Telegram
  - Relatórios diários
  - Logs detalhados

- **Visualização**
  - Dashboard interativo no Power BI
  - Gráficos e métricas em tempo real
  - Relatórios personalizados

## Tecnologias Utilizadas

- Python 3.8+
- PostgreSQL
- Power BI
- Git
- Bibliotecas Python:
  - pandas
  - numpy
  - scikit-learn
  - plotly
  - schedule
  - python-telegram-bot
  - loguru

## Como Executar

1. Clone o repositório:
```bash
git clone https://github.com/brunoxabreu/sales-analytics.git
cd sales-analytics
```

2. Crie um ambiente virtual e ative:
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
```bash
# Execute o script SQL para criar as tabelas
psql -U seu_usuario -d seu_banco -f src/etl/schema.sql
```

6. Execute o processamento:
```bash
# Execução única
python src/etl/process_data.py

# Modo agendado
python src/etl/process_data.py --schedule
```

## Configuração do Telegram

1. Crie um bot no Telegram usando o @BotFather
2. Obtenha o token do bot
3. Adicione o token e o chat_id no arquivo .env

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Autor

Bruno Ferreira de Abreu Arruda
Data Analyst | Business Intelligence | Data Solutions

- Email: brunoxabreu@gmail.com
- LinkedIn: linkedin.com/in/brunoxabreu
- GitHub: github.com/brunoxabreu 