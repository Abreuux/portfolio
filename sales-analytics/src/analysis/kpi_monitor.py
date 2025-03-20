"""
Módulo de monitoramento de KPIs
Autor: Bruno Ferreira de Abreu Arruda
Data: 2024
"""

import pandas as pd
from datetime import datetime, timedelta
from loguru import logger
import os
from telegram import Bot
from dotenv import load_dotenv

class KPIMonitor:
    def __init__(self, df):
        """
        Inicializa o monitor de KPIs
        df: DataFrame com dados de vendas
        """
        self.df = df
        load_dotenv()
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.bot = Bot(token=self.telegram_token) if self.telegram_token else None
        
    def calculate_daily_kpis(self):
        """Calcula KPIs diários"""
        try:
            today = datetime.now().date()
            yesterday = today - timedelta(days=1)
            
            # Filtra dados do dia anterior
            df_yesterday = self.df[self.df['data_venda'].dt.date == yesterday]
            
            kpis = {
                'data': yesterday,
                'total_vendas': df_yesterday['valor_venda'].sum(),
                'ticket_medio': df_yesterday['valor_venda'].mean(),
                'total_pedidos': len(df_yesterday),
                'categorias_mais_vendidas': df_yesterday.groupby('categoria')['valor_venda'].sum().nlargest(3).to_dict()
            }
            
            return kpis
            
        except Exception as e:
            logger.error(f"Erro ao calcular KPIs: {e}")
            raise
    
    def check_alerts(self, kpis):
        """Verifica se há alertas para enviar"""
        alerts = []
        
        # Alerta de queda nas vendas
        if kpis['total_vendas'] < 1000:  # Exemplo de threshold
            alerts.append(f"⚠️ Alerta: Vendas abaixo do esperado ({kpis['total_vendas']:.2f})")
        
        # Alerta de ticket médio baixo
        if kpis['ticket_medio'] < 50:  # Exemplo de threshold
            alerts.append(f"⚠️ Alerta: Ticket médio baixo ({kpis['ticket_medio']:.2f})")
        
        return alerts
    
    def send_telegram_notification(self, message):
        """Envia notificação via Telegram"""
        try:
            if self.bot and self.telegram_chat_id:
                self.bot.send_message(
                    chat_id=self.telegram_chat_id,
                    text=message
                )
                logger.info("Notificação enviada com sucesso")
            else:
                logger.warning("Telegram não configurado")
                
        except Exception as e:
            logger.error(f"Erro ao enviar notificação: {e}")
    
    def generate_daily_report(self):
        """Gera e envia relatório diário"""
        try:
            kpis = self.calculate_daily_kpis()
            alerts = self.check_alerts(kpis)
            
            # Monta mensagem
            message = f"""
📊 Relatório Diário de Vendas
Data: {kpis['data']}

💰 Total de Vendas: R$ {kpis['total_vendas']:.2f}
🛍️ Total de Pedidos: {kpis['total_pedidos']}
💵 Ticket Médio: R$ {kpis['ticket_medio']:.2f}

🏆 Top 3 Categorias:
"""
            for cat, valor in kpis['categorias_mais_vendidas'].items():
                message += f"- {cat}: R$ {valor:.2f}\n"
            
            if alerts:
                message += "\n⚠️ Alertas:\n"
                for alert in alerts:
                    message += f"- {alert}\n"
            
            # Envia notificação
            self.send_telegram_notification(message)
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            raise 