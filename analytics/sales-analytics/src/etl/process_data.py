"""
Script de processamento de dados de vendas
Autor: Bruno Ferreira de Abreu Arruda
Data: 2024
"""

import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
from loguru import logger
import schedule
import time

# Importa módulos de análise
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.analysis.sales_forecast import SalesForecast
from src.analysis.kpi_monitor import KPIMonitor

# Carrega variáveis de ambiente
load_dotenv()

# Configura logging
logger.add(
    "logs/sales_analytics.log",
    rotation="1 day",
    retention="7 days",
    level=os.getenv('LOG_LEVEL', 'INFO')
)

def connect_to_db():
    """Estabelece conexão com o banco de dados"""
    try:
        # Pega credenciais do .env
        db_url = os.getenv('DATABASE_URL')
        engine = create_engine(db_url)
        return engine
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco: {e}")
        raise

def load_sales_data(file_path):
    """
    Carrega dados de vendas do arquivo CSV
    Retorna DataFrame com dados limpos
    """
    try:
        df = pd.read_csv(file_path)
        
        # Limpeza básica
        df['data_venda'] = pd.to_datetime(df['data_venda'])
        df['valor_venda'] = df['valor_venda'].astype(float)
        
        return df
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}")
        raise

def calculate_metrics(df):
    """
    Calcula métricas principais
    """
    metrics = {
        'total_vendas': df['valor_venda'].sum(),
        'ticket_medio': df['valor_venda'].mean(),
        'total_pedidos': len(df),
        'data_atualizacao': datetime.now()
    }
    return metrics

def save_to_database(df, engine):
    """
    Salva dados processados no banco
    """
    try:
        df.to_sql('vendas', engine, if_exists='append', index=False)
        logger.info("Dados salvos com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
        raise

def run_analysis(df):
    """
    Executa análises e previsões
    """
    try:
        # Inicializa previsão
        forecast = SalesForecast(df)
        forecast.train_model()
        
        # Gera previsão para próximos 7 dias
        predictions = forecast.predict_next_days(days=7)
        logger.info("Previsões geradas com sucesso")
        
        # Inicializa monitor de KPIs
        monitor = KPIMonitor(df)
        monitor.generate_daily_report()
        
    except Exception as e:
        logger.error(f"Erro nas análises: {e}")
        raise

def main():
    """
    Função principal que orquestra o processo
    """
    try:
        logger.info("Iniciando processamento de dados")
        
        # Conecta ao banco
        engine = connect_to_db()
        
        # Carrega dados
        df = load_sales_data('data/vendas.csv')
        
        # Calcula métricas
        metrics = calculate_metrics(df)
        
        # Salva no banco
        save_to_database(df, engine)
        
        # Executa análises
        run_analysis(df)
        
        logger.info("Processo finalizado com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro no processo: {e}")
        raise

def schedule_jobs():
    """
    Agenda tarefas automáticas
    """
    # Agenda processamento diário às 8h
    schedule.every().day.at("08:00").do(main)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        schedule_jobs()
    else:
        main() 