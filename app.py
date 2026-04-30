import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    import sys
    import os

    # Ajuste de caminho para o Codespace
    sys.path.append(os.getcwd())

    from src.engine import DataEngine
    from src.analytics import AnalyticsSystem
    from src.components import UIComponents

    # Inicialização das classes
    engine = DataEngine("data/dados.csv")
    system = AnalyticsSystem()
    ui = UIComponents()
    
    df_analise = engine.get_analise_subset()
    df_ff = engine.get_fontforge_data()
    
    return df_analise, df_ff, engine, mo, os, sys, system, ui


@app.cell
def _(mo):
    # 1. Definição do Header (Visual Y2K/Moderno)
    header = mo.md(
    """
    <div style='background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); 
                color: white; padding: 2rem; border-radius: 1.5rem; margin: 0.5rem 0 0 0; margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(79, 70, 229, 0.2);'>
        <h1 style='margin: 0; font-size: 2.2rem; letter-spacing: -1px; font-weight: 800; color: white'>Validação Estatistica </h1>
        <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1rem; text-transform: uppercase; letter-spacing: 2px;'>
            Outliers • Método Tracy
        </p>
    </div>
    """
    )

    regras_raw = [
        # --- MAIÚSCULAS ---
        ('Be', 'He', "B esquerdo = H esquerdo"), 
        ('Ce', 'Oe', "C esquerdo = O esquerdo"),
        ('De', 'He', "D esquerdo = H esquerdo"), 
        ('Dd', 'Od', "D direito = O direito"),
        ('Ee', 'He', "E esquerdo = H esquerdo"), 
        ('Fe', 'He', "F esquerdo = H esquerdo"),
        ('Ge', 'Oe', "G esquerdo = O esquerdo"), 
        ('Ie', 'He', "I esquerdo = H esquerdo"),
        ('Id', 'Hd', "I direito = H direito"), 
        ('Jd', 'Hd', "J direito = H direito"), 
        ('Ke', 'He', "K esquerdo = H esquerdo"),
        ('Le', 'He', "L esquerdo = H esquerdo"), 
        ('Md', 'Hd', "M direito = H direito"), 
        ('Pe', 'He', "P esquerdo = H esquerdo"),
        ('Pd', 'Od', "P direito = O direito"), 
        ('Qe', 'Oe', "Q esquerdo = O esquerdo"), 
        ('Qd', 'Od', "Q direito = O direito"),
        ('Re', 'He', "R esquerdo = H esquerdo"), 
        ('Ue', 'He', "U esquerdo = H esquerdo"),

        # --- MINÚSCULAS ---
        ('be', 'ne', "b esquerdo = n esquerdo"), 
        ('bd', 'oe', "b direito = o direito"),   
        ('ce', 'oe', "c esquerdo = o esquerdo"),
        ('de', 'oe', "d esquerdo = o esquerdo"), 
        ('dd', 'ne', "d direito = n esquerdo"), 
        ('ee', 'oe', "e esquerdo = o esquerdo"),
        ('id', 'ne', "i direito = n esquerdo"), 
        ('jd', 'ne', "j direito = n esquerdo"), 
        ('je', 'ne', "j esquerdo = n esquerdo"), 
        ('ke', 'ne', "k esquerdo = n esquerdo"), 
        ('ld', 'ne', "l direito = n esquerdo"), 
        ('md', 'ne', "m direito = n esquerdo"), 
        ('me', 'ne', "m esquerdo = n esquerdo"), 
        ('pd', 'od', "p direito = o direito"),  
        ('qe', 'oe', "q esquerdo = o esquerdo"), 
        ('qd', 'ne', "q direito = n esquerdo"), 
        ('re', 'ne', "r esquerdo = n esquerdo"),
        ('ue', 'nd', "u esquerdo = n direito"),  
        ('ud', 'nd', "u direito = n direito")  
    ]

    dropdown = mo.ui.dropdown(
        options={desc: (a, r) for a, r, desc in sorted(regras_raw, key=lambda x: (x[0].islower(), x[2]))},
        label="🎯 Selecione a Regra para Analisar",
        value=None
    )
    
    return dropdown, header, regras_raw


@app.cell
def _(df_analise, df_ff, dropdown, header, mo, system, ui):
    # 2. Lógica de Renderização Unificada
    if dropdown.value is None:
        render = mo.vstack([
            header,
            mo.center(dropdown),
            mo.md("### 📊 Aguardando seleção de regra...").center()
        ])
    else:
        alvo, ref = dropdown.value
        
        # Recebendo os dados de regressão (m, c)
        df_plot, outliers, m, c = system.calcular_desvios(df_analise, alvo, ref)
        media = df_plot['diff'].mean()

        # Renderização do Dashboard com o df_ff adicionado nos parâmetros
        resultado = ui.render_infografico(alvo, ref, df_plot, outliers, media, m, c, df_ff)

        render = mo.vstack([
            header,
            mo.center(dropdown),
            mo.md("---"),
            resultado
        ])

    render
    return alvo, df_plot, media, outliers, ref, render


if __name__ == "__main__":
    app.run()