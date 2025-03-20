"""
Funções utilitárias para o projeto
Autor: Bruno Ferreira de Abreu Arruda
Data: 2024
"""

import pandas as pd
from datetime import datetime
from loguru import logger

def format_currency(value):
    """Formata valor para moeda brasileira"""
    try:
        return f"R$ {value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    except Exception as e:
        logger.error(f"Erro ao formatar moeda: {e}")
        return str(value)

def calculate_growth_rate(current, previous):
    """Calcula taxa de crescimento entre dois valores"""
    try:
        if previous == 0:
            return 0
        return ((current - previous) / previous) * 100
    except Exception as e:
        logger.error(f"Erro ao calcular taxa de crescimento: {e}")
        return 0

def get_date_range(df, date_column='data_venda'):
    """Retorna período dos dados"""
    try:
        min_date = df[date_column].min()
        max_date = df[date_column].max()
        return f"{min_date.strftime('%d/%m/%Y')} até {max_date.strftime('%d/%m/%Y')}"
    except Exception as e:
        logger.error(f"Erro ao obter período: {e}")
        return "Período não disponível"

def clean_dataframe(df):
    """Realiza limpeza básica no DataFrame"""
    try:
        # Remove linhas com valores nulos
        df = df.dropna()
        
        # Remove duplicatas
        df = df.drop_duplicates()
        
        # Remove espaços em branco
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()
            
        return df
    except Exception as e:
        logger.error(f"Erro ao limpar DataFrame: {e}")
        return df 