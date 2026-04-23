import pandas as pd
import numpy as np

class AnalyticsSystem:
    @staticmethod
    def calcular_desvios(df, alvo, ref):
        """Calcula os desvios, identifica outliers e cria estimativas de regressão."""
        # 1. Limpeza e Cálculo de Diferença (Real - Previsto Tracy)
        data = df.dropna(subset=[alvo, ref, 'nome_fonte']).copy()
        data['diff'] = data[alvo] - data[ref]
        
        if data.empty:
            return data, data, 0, 0

        # 2. Identificação Contextual de Outliers (Z-Score)
        mean = data['diff'].mean()
        std = data['diff'].std()
        
        if std == 0:
            return data, pd.DataFrame(), 1, 0

        data['z_score'] = (data['diff'] - mean) / std
        outliers = data[data['z_score'].abs() > 1.0]
        
        # 3. Cálculo de Regressão Linear Simples seguindo: y = ax + b
        try:
            # m = coeficiente angular (a), c = coeficiente linear (b)
            # Seguindo a lógica da imagem: alvo = a * ref + b
            m, c = np.polyfit(data[ref], data[alvo], 1)
        except Exception:
            m, c = 1, 0
        
        return data, outliers.sort_values(by='diff', key=abs, ascending=False), m, c