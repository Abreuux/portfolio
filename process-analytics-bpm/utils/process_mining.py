import pandas as pd
import numpy as np
import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.statistics.variants.log import get as variants_get
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.visualization.dfg import visualizer as dfg_visualizer
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProcessMiningAnalyzer:
    def __init__(self, log_path=None):
        self.log_path = log_path
        self.log = None
        self.net = None
        self.initial_marking = None
        self.final_marking = None

    def load_log(self, log_path=None):
        """Carrega o log de eventos do arquivo XES"""
        try:
            if log_path:
                self.log_path = log_path
            if not self.log_path:
                raise ValueError("Caminho do log não especificado")
            
            self.log = xes_importer.apply(self.log_path)
            logger.info(f"Log carregado com sucesso: {len(self.log)} casos")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar log: {str(e)}")
            return False

    def discover_process_model(self, algorithm='inductive'):
        """Descobre o modelo de processo usando diferentes algoritmos"""
        try:
            if not self.log:
                raise ValueError("Log não carregado")

            if algorithm == 'inductive':
                self.net, self.initial_marking, self.final_marking = inductive_miner.apply(self.log)
            elif algorithm == 'alpha':
                self.net, self.initial_marking, self.final_marking = alpha_miner.apply(self.log)
            elif algorithm == 'heuristics':
                self.net, self.initial_marking, self.final_marking = heuristics_miner.apply(self.log)
            else:
                raise ValueError(f"Algoritmo não suportado: {algorithm}")

            logger.info("Modelo de processo descoberto com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao descobrir modelo: {str(e)}")
            return False

    def analyze_conformance(self):
        """Analisa a conformidade entre o log e o modelo"""
        try:
            if not self.net or not self.log:
                raise ValueError("Modelo ou log não carregado")

            replayed_traces = token_replay.apply(self.log, self.net, self.initial_marking, self.final_marking)
            
            # Calcula métricas de conformidade
            fitness = sum(trace['trace_is_fit'] for trace in replayed_traces) / len(replayed_traces)
            precision = sum(trace['trace_fitness'] for trace in replayed_traces) / len(replayed_traces)
            
            return {
                'fitness': fitness,
                'precision': precision,
                'replayed_traces': replayed_traces
            }
        except Exception as e:
            logger.error(f"Erro na análise de conformidade: {str(e)}")
            return None

    def identify_bottlenecks(self):
        """Identifica gargalos no processo"""
        try:
            if not self.log:
                raise ValueError("Log não carregado")

            # Calcula estatísticas de casos
            case_stats = case_statistics.get_case_statistics(self.log)
            
            # Identifica atividades com maior tempo médio
            activity_stats = {}
            for case in self.log:
                for event in case:
                    activity = event['concept:name']
                    if activity not in activity_stats:
                        activity_stats[activity] = {'count': 0, 'total_time': 0}
                    activity_stats[activity]['count'] += 1
                    if 'time:timestamp' in event:
                        activity_stats[activity]['total_time'] += event['time:timestamp']

            # Calcula médias
            bottlenecks = []
            for activity, stats in activity_stats.items():
                avg_time = stats['total_time'] / stats['count']
                bottlenecks.append({
                    'activity': activity,
                    'avg_time': avg_time,
                    'frequency': stats['count']
                })

            return sorted(bottlenecks, key=lambda x: x['avg_time'], reverse=True)
        except Exception as e:
            logger.error(f"Erro ao identificar gargalos: {str(e)}")
            return None

    def analyze_variants(self):
        """Analisa variantes do processo"""
        try:
            if not self.log:
                raise ValueError("Log não carregado")

            variants = variants_get.get_variants(self.log)
            variant_stats = []
            
            for variant, cases in variants.items():
                variant_stats.append({
                    'variant': variant,
                    'frequency': len(cases),
                    'percentage': len(cases) / len(self.log) * 100
                })

            return sorted(variant_stats, key=lambda x: x['frequency'], reverse=True)
        except Exception as e:
            logger.error(f"Erro ao analisar variantes: {str(e)}")
            return None

    def visualize_process(self, output_path=None):
        """Visualiza o modelo de processo"""
        try:
            if not self.net:
                raise ValueError("Modelo não descoberto")

            # Gera visualização do modelo
            gviz = pn_visualizer.apply(self.net, self.initial_marking, self.final_marking)
            
            if output_path:
                pn_visualizer.save(gviz, output_path)
                logger.info(f"Visualização salva em: {output_path}")
            
            return gviz
        except Exception as e:
            logger.error(f"Erro ao visualizar processo: {str(e)}")
            return None

    def export_model(self, output_path):
        """Exporta o modelo de processo para PNML"""
        try:
            if not self.net:
                raise ValueError("Modelo não descoberto")

            pm4py.objects.petri_net.exporter.exporter.apply(
                self.net, 
                self.initial_marking, 
                output_path
            )
            logger.info(f"Modelo exportado para: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao exportar modelo: {str(e)}")
            return False

def main():
    """Função principal para demonstração"""
    analyzer = ProcessMiningAnalyzer()
    
    # Exemplo de uso
    log_path = "data/process_log.xes"
    if analyzer.load_log(log_path):
        if analyzer.discover_process_model():
            bottlenecks = analyzer.identify_bottlenecks()
            if bottlenecks:
                print("\nGargalos identificados:")
                for b in bottlenecks[:5]:
                    print(f"- {b['activity']}: {b['avg_time']}s (frequência: {b['frequency']})")
            
            variants = analyzer.analyze_variants()
            if variants:
                print("\nTop 5 variantes:")
                for v in variants[:5]:
                    print(f"- {v['variant']}: {v['percentage']:.2f}%")
            
            analyzer.visualize_process("output/process_model.png")

if __name__ == "__main__":
    main() 