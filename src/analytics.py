import pandas as pd
import numpy as np

class AnalyticsSystem:
    @staticmethod
    def calcular_desvios(df, alvo, ref):
        """Calcula os desvios e identifica outliers contextualizados."""
        # 1. Limpeza e Cálculo de Diferença
        data = df.dropna(subset=[alvo, ref, 'nome_fonte']).copy()
        data['diff'] = data[alvo] - data[ref]
        
        if data.empty:
            return data, data

        # 2. Identificação Contextual de Outliers (Z-Score)
        # Calculamos quem está muito fora da 'média da família'
        mean = data['diff'].mean()
        std = data['diff'].std()
        
        # Se std for 0 (todas as fontes são iguais), não há outliers
        if std == 0:
            return data, pd.DataFrame()

        # Calculamos o Z-Score para cada fonte
        data['z_score'] = (data['diff'] - mean) / std
        
        # Filtramos quem está a mais de 2.0 desvios padrão (Z-Score > 2.0 ou < -2.0)
        # Isso identifica as fontes que são estatisticamente anômalas
        outliers = data[data['z_score'].abs() > 2.0]
        
        # Retorna os dados para o gráfico e a lista de culpados ordenada pelo erro absoluto
        return data, outliers.sort_values(by='diff', key=abs, ascending=False)