"""
Configurações do projeto
Autor: Bruno Ferreira de Abreu Arruda
Data: 2024
"""

import os
from pathlib import Path

# Diretórios do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'
DASHBOARD_DIR = BASE_DIR / 'dashboard'

# Configurações de arquivos
SALES_DATA_FILE = DATA_DIR / 'vendas.csv'
LOG_FILE = LOGS_DIR / 'sales_analytics.log'

# Configurações de análise
FORECAST_DAYS = 7
ALERT_THRESHOLDS = {
    'vendas_minimas': 1000,
    'ticket_medio_minimo': 50
}

# Configurações de notificação
NOTIFICATION_TIME = "08:00"
NOTIFICATION_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday"]

# Configurações de banco de dados
DB_TABLES = {
    'vendas': 'vendas',
    'previsoes': 'previsoes_vendas',
    'kpis': 'kpis_diarios'
}

# Cria diretórios se não existirem
for directory in [DATA_DIR, LOGS_DIR, DASHBOARD_DIR]:
    directory.mkdir(parents=True, exist_ok=True) 