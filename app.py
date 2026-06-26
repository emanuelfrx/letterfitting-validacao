import marimo

__generated_with = "0.21.1"
app = marimo.App(width="full")


# ╔══════════════════════════════════════════════════════════════╗
#  IMPORTS
# ╚══════════════════════════════════════════════════════════════╝
@app.cell
def _():
    import marimo as mo
    import sys
    import os

    sys.path.append(os.getcwd())

    from src.engine import DataEngine

    return DataEngine, mo


# ╔══════════════════════════════════════════════════════════════╗
#  DADOS
# ╚══════════════════════════════════════════════════════════════╝
@app.cell
def _(DataEngine):
    engine = DataEngine("data/dados.csv")

    df_analise = engine.get_analise_subset()
    df_ff = engine.get_fontforge_data()

    return df_analise, df_ff


# ╔══════════════════════════════════════════════════════════════╗
#  HEADER
# ╚══════════════════════════════════════════════════════════════╝
@app.cell
def _():
    from src.components import header_banner

    header_banner()


# ╔══════════════════════════════════════════════════════════════╗
#  CONFIGURAÇÃO
# ╚══════════════════════════════════════════════════════════════╝
@app.cell
def _(mo):
    from src.config import REGRAS_MAP

    dropdown = mo.ui.dropdown(
        options=REGRAS_MAP,
        label="Regra tipográfica",
        value=None,
    )

    return REGRAS_MAP, dropdown, mo.md(f"""
<div style="
background:white;
padding:1.5rem;
border:1px solid #E2E8F0;
border-radius:16px;
margin-bottom:1.5rem;
">

<h3 style="
margin:0 0 .5rem 0;
font-size:1.15rem;
font-weight:600;
">
Configuração da análise
</h3>

<p style="
margin:0 0 1rem 0;
color:#64748B;
">
Selecione uma regra de Walter Tracy para executar a validação estatística.
</p>

</div>
""")

@app.cell
def _(dropdown, mo):
    mo.vstack(
        [
            dropdown,
        ]
    )
# ╔══════════════════════════════════════════════════════════════╗
#  PROCESSAMENTO
# ╚══════════════════════════════════════════════════════════════╝
@app.cell
def _(REGRAS_MAP, df_analise, dropdown, mo):
    from src.analytics import calcular_desvios
    from src.components import empty_state

    if dropdown.value is None:
        empty_state(len(REGRAS_MAP))
        mo.stop(True)

    alvo, ref = dropdown.value

    result = calcular_desvios(
        df_analise,
        alvo,
        ref,
    )

    return alvo, ref, result


# ╔══════════════════════════════════════════════════════════════╗
#  RESUMO
# ╚══════════════════════════════════════════════════════════════╝
@app.cell
def _(mo):
    mo.md("""
## Resumo da análise

Indicadores principais da amostra analisada.
""")


@app.cell
def _(alvo, ref, result):
    from src.components import kpi_cards

    kpi_cards(result, alvo, ref)


# ╔══════════════════════════════════════════════════════════════╗
#  DISTRIBUIÇÃO ESTATÍSTICA
# ╚══════════════════════════════════════════════════════════════╝
@app.cell
def _():
    from src.components import section_divider as _sd

    _sd(
        "01",
        "Distribuição Estatística",
        "Comportamento geral dos desvios observados"
    )


@app.cell
def _(mo, result):
    from src.components import (
        chart_boxplot,
        chart_violinplot,
        chart_scatter,
    )

    mo.vstack([
        mo.hstack([
            chart_boxplot(result),
            chart_violinplot(result),
        ]),
        chart_scatter(result),
    ])


# ╔══════════════════════════════════════════════════════════════╗
#  OUTLIERS
# ╚══════════════════════════════════════════════════════════════╝
@app.cell
def _():
    from src.components import section_divider as _sd

    _sd(
        "02",
        "Identificação de Outliers",
        "Análise individual das fontes"
    )


@app.cell
def _(alvo, ref, result):
    from src.components import chart_bar_detail

    chart_bar_detail(
        result,
        alvo,
        ref,
    )


# ╔══════════════════════════════════════════════════════════════╗
#  DADOS DETALHADOS
# ╚══════════════════════════════════════════════════════════════╝
@app.cell
def _():
    from src.components import section_divider as _sd

    _sd(
        "03",
        "Dados Detalhados",
        "Valores originais e cálculo Tracy"
    )


@app.cell
def _(alvo, df_ff, ref, result):
    from src.components import table_typography

    table_typography(
        result,
        alvo,
        ref,
        df_ff,
    )


if __name__ == "__main__":
    app.run()