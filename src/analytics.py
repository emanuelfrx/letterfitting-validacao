import pandas as pd
import numpy as np

class AnalyticsSystem:
    @staticmethod
    def calcular_desvios(df, alvo, ref):
        """Calcula os desvios, identifica outliers e cria estimativas de regressão de alta precisão."""
        # 1. Limpeza e Cálculo de Diferença
        data = df.dropna(subset=[alvo, ref, 'nome_fonte']).copy()
        data['diff'] = data[alvo] - data[ref]
        
        if data.empty:
            data['ideal'] = 0.0
            return data, data, 0.0, 0.0

        # 2. Identificação Contextual de Outliers (Z-Score)
        mean = data['diff'].mean()
        std = data['diff'].std()
        
        if std == 0:
            data['ideal'] = data[ref].astype(float)
            return data, pd.DataFrame(), 1.0, 0.0

        data['z_score'] = (data['diff'] - mean) / std
        outliers = data[data['z_score'].abs() > 1.0]
        
        # 3. Cálculo de Regressão Linear com np.polyfit (Alta Precisão)
        try:
            # Garante que os dados são float64 para máxima precisão no cálculo matricial do polyfit
            x = data[ref].values.astype(float)
            y = data[alvo].values.astype(float)
            
            # m = slope (a), c = intercept (b)
            m, c = np.polyfit(x, y, 1)
        except Exception:
            m, c = 1.0, 0.0
        
        # 4. Cálculo do Espaçamento Ideal com os coeficientes precisos
        data['ideal'] = (data[ref] * m) + c
        
        return data, outliers.sort_values(by='diff', key=abs, ascending=False), m, c