# ─────────────────────────────────────────────────────────────
#  analytics.py  — Cálculos estatísticos (sem UI)
# ─────────────────────────────────────────────────────────────
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class AnalysisResult:
    """Resultado imutável de uma análise de desvio."""
    df_plot: pd.DataFrame       # DataFrame com colunas diff, z_score, ideal
    outliers: pd.DataFrame      # Subconjunto dos outliers
    m: float                    # coeficiente angular (slope)
    c: float                    # intercepto
    media: float                # média aritmética de diff
    n_fontes: int               # total de fontes analisadas
    fonte_maior: str            # nome da fonte com maior desvio
    val_maior: float
    fonte_menor: str            # nome da fonte com menor desvio
    val_menor: float


def calcular_desvios(df: pd.DataFrame, alvo: str, ref: str) -> AnalysisResult:
    """
    Calcula desvios, identifica outliers (z-score > 1.0) e
    ajusta regressão linear (alvo ~ ref) via np.polyfit.
    """
    data = df.dropna(subset=[alvo, ref, 'nome_fonte']).copy()
    data['diff'] = data[alvo] - data[ref]

    if data.empty:
        empty = pd.DataFrame()
        return AnalysisResult(empty, empty, 1.0, 0.0, 0.0, 0, "—", 0.0, "—", 0.0)

    mean = data['diff'].mean()
    std = data['diff'].std()

    if std == 0:
        data['ideal'] = data[ref].astype(float)
        data['z_score'] = 0.0
    else:
        data['z_score'] = (data['diff'] - mean) / std
        try:
            m, c = np.polyfit(data[ref].values.astype(float),
                              data[alvo].values.astype(float), 1)
        except Exception:
            m, c = 1.0, 0.0
        data['ideal'] = data[ref] * m + c

    m = m if std != 0 else 1.0
    c = c if std != 0 else 0.0

    outliers = (
        data[data['z_score'].abs() > 1.0]
        .sort_values(by='diff', key=abs, ascending=False)
    )

    idx_maior = data['diff'].idxmax()
    idx_menor = data['diff'].idxmin()

    return AnalysisResult(
        df_plot=data,
        outliers=outliers,
        m=m,
        c=c,
        media=mean,
        n_fontes=len(data),
        fonte_maior=data.loc[idx_maior, 'nome_fonte'],
        val_maior=data.loc[idx_maior, 'diff'],
        fonte_menor=data.loc[idx_menor, 'nome_fonte'],
        val_menor=data.loc[idx_menor, 'diff'],
    )