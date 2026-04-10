import pandas as pd
import numpy as np

class AnalyticsSystem:
    @staticmethod
    def calcular_desvios(df, alvo, ref):
        """Calcula os desvios e identifica outliers contextualizados."""
        # 1. Limpeza e Cálculo de Diferença (Real - Previsto Tracy)
        data = df.dropna(subset=[alvo, ref, 'nome_fonte']).copy()
        data['diff'] = data[alvo] - data[ref]
        
        if data.empty:
            return data, data

        # 2. Identificação Contextual de Outliers (Z-Score)
        mean = data['diff'].mean()
        std = data['diff'].std()
        
        if std == 0:
            return data, pd.DataFrame()

        data['z_score'] = (data['diff'] - mean) / std
        
        # Filtramos quem está a mais de 1.0 desvios padrão
        outliers = data[data['z_score'].abs() > 1.0]
        
        return data, outliers.sort_values(by='diff', key=abs, ascending=False)