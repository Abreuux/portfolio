"""
Módulo de previsão de vendas
Autor: Bruno Ferreira de Abreu Arruda
Data: 2024
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from loguru import logger
from datetime import datetime, timedelta

class SalesForecast:
    def __init__(self, df):
        """
        Inicializa o modelo de previsão
        df: DataFrame com dados históricos de vendas
        """
        self.df = df
        self.model = LinearRegression()
        
    def prepare_data(self):
        """Prepara dados para o modelo"""
        try:
            # Agrupa vendas por dia
            daily_sales = self.df.groupby('data_venda')['valor_venda'].sum().reset_index()
            
            # Cria features numéricas
            daily_sales['dia_semana'] = daily_sales['data_venda'].dt.dayofweek
            daily_sales['dia_mes'] = daily_sales['data_venda'].dt.day
            daily_sales['mes'] = daily_sales['data_venda'].dt.month
            
            # Cria target (vendas do próximo dia)
            daily_sales['target'] = daily_sales['valor_venda'].shift(-1)
            
            # Remove última linha (sem target)
            daily_sales = daily_sales.dropna()
            
            return daily_sales
            
        except Exception as e:
            logger.error(f"Erro ao preparar dados: {e}")
            raise
    
    def train_model(self):
        """Treina o modelo de previsão"""
        try:
            data = self.prepare_data()
            
            # Features para treino
            X = data[['dia_semana', 'dia_mes', 'mes']]
            y = data['target']
            
            # Treina modelo
            self.model.fit(X, y)
            logger.info("Modelo treinado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao treinar modelo: {e}")
            raise
    
    def predict_next_days(self, days=7):
        """
        Faz previsão para os próximos dias
        days: número de dias para prever
        """
        try:
            last_date = self.df['data_venda'].max()
            predictions = []
            
            for i in range(days):
                next_date = last_date + timedelta(days=i+1)
                
                # Prepara features para previsão
                X_pred = pd.DataFrame({
                    'dia_semana': [next_date.dayofweek],
                    'dia_mes': [next_date.day],
                    'mes': [next_date.month]
                })
                
                # Faz previsão
                pred = self.model.predict(X_pred)[0]
                
                predictions.append({
                    'data': next_date,
                    'previsao': pred
                })
            
            return pd.DataFrame(predictions)
            
        except Exception as e:
            logger.error(f"Erro ao fazer previsões: {e}")
            raise 