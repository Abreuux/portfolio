import pandas as pd
import numpy as np
import rpy2.robjects as robjects
import rpy2.robjects.pandas2ri as pandas2ri
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SixSigmaAnalyzer:
    def __init__(self, target_sigma=6.0, tolerance=0.1):
        self.target_sigma = target_sigma
        self.tolerance = tolerance
        self.r = robjects.r
        self.setup_r_functions()

    def setup_r_functions(self):
        """Configura funções R para análise Six Sigma"""
        self.r('''
            calculate_sigma <- function(data, target, tolerance) {
                mean_val <- mean(data)
                sd_val <- sd(data)
                usl <- target + tolerance
                lsl <- target - tolerance
                cp <- (usl - lsl)/(6*sd_val)
                cpk <- min((usl - mean_val)/(3*sd_val), (mean_val - lsl)/(3*sd_val))
                sigma_level <- cp * 3
                return(c(cp, cpk, sigma_level, mean_val, sd_val))
            }

            calculate_control_limits <- function(data) {
                mean_val <- mean(data)
                sd_val <- sd(data)
                ucl <- mean_val + 3*sd_val
                lcl <- mean_val - 3*sd_val
                return(c(ucl, lcl))
            }

            calculate_capability <- function(data, target, tolerance) {
                mean_val <- mean(data)
                sd_val <- sd(data)
                usl <- target + tolerance
                lsl <- target - tolerance
                z_upper <- (usl - mean_val)/sd_val
                z_lower <- (mean_val - lsl)/sd_val
                p_upper <- 1 - pnorm(z_upper)
                p_lower <- pnorm(z_lower)
                return(c(p_upper, p_lower))
            }
        ''')

    def calculate_process_capability(self, data, target=None):
        """Calcula métricas de capacidade do processo"""
        try:
            if target is None:
                target = np.mean(data)

            # Converte dados para R
            r_data = robjects.FloatVector(data)
            
            # Calcula métricas
            result = self.r.calculate_sigma(r_data, target, self.tolerance)
            
            return {
                'cp': result[0],
                'cpk': result[1],
                'sigma_level': result[2],
                'mean': result[3],
                'std_dev': result[4]
            }
        except Exception as e:
            logger.error(f"Erro ao calcular capacidade do processo: {str(e)}")
            return None

    def calculate_control_limits(self, data):
        """Calcula limites de controle"""
        try:
            # Converte dados para R
            r_data = robjects.FloatVector(data)
            
            # Calcula limites
            result = self.r.calculate_control_limits(r_data)
            
            return {
                'ucl': result[0],
                'lcl': result[1]
            }
        except Exception as e:
            logger.error(f"Erro ao calcular limites de controle: {str(e)}")
            return None

    def calculate_capability_indices(self, data, target=None):
        """Calcula índices de capacidade"""
        try:
            if target is None:
                target = np.mean(data)

            # Converte dados para R
            r_data = robjects.FloatVector(data)
            
            # Calcula índices
            result = self.r.calculate_capability(r_data, target, self.tolerance)
            
            return {
                'p_upper': result[0],
                'p_lower': result[1],
                'total_defects': (result[0] + result[1]) * len(data)
            }
        except Exception as e:
            logger.error(f"Erro ao calcular índices de capacidade: {str(e)}")
            return None

    def analyze_process_stability(self, data, window_size=10):
        """Analisa a estabilidade do processo"""
        try:
            # Calcula médias móveis
            rolling_mean = pd.Series(data).rolling(window=window_size).mean()
            rolling_std = pd.Series(data).rolling(window=window_size).std()
            
            # Calcula limites de controle
            control_limits = self.calculate_control_limits(data)
            
            # Identifica pontos fora de controle
            out_of_control = (rolling_mean > control_limits['ucl']) | (rolling_mean < control_limits['lcl'])
            
            return {
                'rolling_mean': rolling_mean.tolist(),
                'rolling_std': rolling_std.tolist(),
                'out_of_control': out_of_control.tolist(),
                'control_limits': control_limits
            }
        except Exception as e:
            logger.error(f"Erro ao analisar estabilidade do processo: {str(e)}")
            return None

    def analyze_process_trends(self, data, window_size=10):
        """Analisa tendências do processo"""
        try:
            # Calcula tendências
            x = np.arange(len(data))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)
            
            # Calcula médias móveis
            rolling_mean = pd.Series(data).rolling(window=window_size).mean()
            
            return {
                'slope': slope,
                'r_squared': r_value**2,
                'p_value': p_value,
                'trend_direction': 'Positiva' if slope > 0 else 'Negativa',
                'rolling_mean': rolling_mean.tolist()
            }
        except Exception as e:
            logger.error(f"Erro ao analisar tendências do processo: {str(e)}")
            return None

    def plot_control_chart(self, data, output_path=None):
        """Gera gráfico de controle"""
        try:
            # Calcula limites de controle
            control_limits = self.calculate_control_limits(data)
            
            # Cria gráfico
            plt.figure(figsize=(12, 6))
            plt.plot(data, 'b-', label='Dados')
            plt.axhline(y=control_limits['ucl'], color='r', linestyle='--', label='UCL')
            plt.axhline(y=control_limits['lcl'], color='r', linestyle='--', label='LCL')
            plt.axhline(y=np.mean(data), color='g', linestyle='-', label='Média')
            
            plt.title('Gráfico de Controle')
            plt.xlabel('Amostra')
            plt.ylabel('Valor')
            plt.legend()
            
            if output_path:
                plt.savefig(output_path)
                logger.info(f"Gráfico salvo em: {output_path}")
            
            plt.close()
            return True
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de controle: {str(e)}")
            return False

    def plot_capability_analysis(self, data, output_path=None):
        """Gera gráfico de análise de capacidade"""
        try:
            # Calcula métricas
            capability = self.calculate_process_capability(data)
            
            # Cria gráfico
            plt.figure(figsize=(12, 6))
            sns.histplot(data, kde=True)
            plt.axvline(x=capability['mean'], color='r', linestyle='-', label='Média')
            plt.axvline(x=capability['mean'] + 3*capability['std_dev'], color='g', linestyle='--', label='+3σ')
            plt.axvline(x=capability['mean'] - 3*capability['std_dev'], color='g', linestyle='--', label='-3σ')
            
            plt.title('Análise de Capacidade')
            plt.xlabel('Valor')
            plt.ylabel('Frequência')
            plt.legend()
            
            if output_path:
                plt.savefig(output_path)
                logger.info(f"Gráfico salvo em: {output_path}")
            
            plt.close()
            return True
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de análise de capacidade: {str(e)}")
            return False

def main():
    """Função principal para demonstração"""
    # Gera dados de exemplo
    np.random.seed(42)
    data = np.random.normal(100, 2, 100)
    
    analyzer = SixSigmaAnalyzer(target_sigma=6.0, tolerance=2.0)
    
    # Calcula métricas
    capability = analyzer.calculate_process_capability(data)
    if capability:
        print("\nMétricas de Capacidade:")
        print(f"CP: {capability['cp']:.2f}")
        print(f"CPK: {capability['cpk']:.2f}")
        print(f"Nível Sigma: {capability['sigma_level']:.2f}")
    
    # Analisa estabilidade
    stability = analyzer.analyze_process_stability(data)
    if stability:
        print("\nAnálise de Estabilidade:")
        print(f"Pontos fora de controle: {sum(stability['out_of_control'])}")
    
    # Analisa tendências
    trends = analyzer.analyze_process_trends(data)
    if trends:
        print("\nAnálise de Tendências:")
        print(f"Direção: {trends['trend_direction']}")
        print(f"R²: {trends['r_squared']:.2f}")
    
    # Gera gráficos
    analyzer.plot_control_chart(data, 'output/control_chart.png')
    analyzer.plot_capability_analysis(data, 'output/capability_analysis.png')

if __name__ == "__main__":
    main() 