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
    return df_analise, mo, system, ui


@app.cell
def _(mo):
    # 1. Definição do Header (Visual Y2K/Moderno)
    header = mo.md(
        """
        <div style='background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); 
                    color: white; padding: 2rem; border-radius: 1.5rem; 
                    text-align: center; margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(79, 70, 229, 0.2);'>
            <h1 style='margin: 0; font-size: 2.2rem; letter-spacing: -1px;'>Specimen Builder <span style='font-weight: 200;'>PRO</span></h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1rem; text-transform: uppercase; letter-spacing: 2px;'>
                Validação Estatística • Método Tracy
            </p>
        </div>
        """
    )

    regras_raw = [
        ('Be', 'He', "B esquerdo = H esquerdo"), ('Ce', 'Oe', "C esquerdo = O esquerdo"),
        ('De', 'He', "D esquerdo = H esquerdo"), ('Dd', 'Od', "D direito = O direito"),
        ('Ee', 'He', "E esquerdo = H esquerdo"), ('Fe', 'He', "F esquerdo = H esquerdo"),
        ('Ge', 'Oe', "G esquerdo = O esquerdo"), ('Ie', 'He', "I esquerdo = H esquerdo"),
        ('Id', 'He', "I direito = H esquerdo"), ('Ke', 'He', "K esquerdo = H esquerdo"),
        ('Le', 'He', "L esquerdo = H esquerdo"), ('Me', 'He', "M esquerdo = H esquerdo"),
        ('Md', 'He', "M direito = H esquerdo"), ('Ne', 'He', "N esquerdo = H esquerdo"),
        ('Nd', 'He', "N direito = H esquerdo"), ('Pe', 'He', "P esquerdo = H esquerdo"),
        ('Qe', 'Oe', "Q esquerdo = O esquerdo"), ('Qd', 'Od', "Q direito = O direito"),
        ('Re', 'He', "R esquerdo = H esquerdo"), ('Ue', 'He', "U esquerdo = H esquerdo"),
        ('bd', 'nd', "b direito = n direito"), ('ce', 'oe', "c esquerdo = o esquerdo"),
        ('de', 'oe', "d esquerdo = o esquerdo"), ('dd', 'nd', "d direito = n direito"),
        ('ee', 'oe', "e esquerdo = o esquerdo"), ('ge', 'oe', "g esquerdo = o esquerdo"),
        ('hd', 'nd', "h direito = n direito"), ('id', 'nd', "i direito = n direito"),
        ('je', 'ne', "j esquerdo = n esquerdo"), ('jd', 'nd', "j direito = n direito"),
        ('ke', 'ne', "k esquerdo = n esquerdo"), ('le', 'ne', "l esquerdo = n esquerdo"),
        ('ld', 'nd', "l direito = n direito"), ('me', 'ne', "m esquerdo = n esquerdo"),
        ('md', 'nd', "m direito = n direito"), ('pd', 'nd', "p direito = n direito"),
        ('qe', 'oe', "q esquerdo = o esquerdo"), ('qd', 'od', "q direito = o direito"),
        ('re', 'ne', "r esquerdo = n esquerdo"), ('ue', 'ne', "u esquerdo = n esquerdo"),
        ('ud', 'nd', "u direito = n direito")
    ]

    dropdown = mo.ui.dropdown(
        options={desc: (a, r) for a, r, desc in sorted(regras_raw, key=lambda x: (x[0].islower(), x[2]))},
        label="🎯 Selecione a Regra para Analisar",
        value=None
    )
    dropdown, header
    return dropdown, header


@app.cell
def _(df_analise, dropdown, header, mo, system, ui):
    # 2. Lógica de Renderização Unificada
    # Se nada estiver selecionado, mostra o Header e o Dropdown com um aviso
    if dropdown.value is None:
        render = mo.vstack([
            header,
            mo.center(dropdown),
            mo.md("### 📊 Aguardando seleção de regra...").center()
        ])
    else:
        alvo, ref = dropdown.value
        df_plot, outliers = system.calcular_desvios(df_analise, alvo, ref)
        media = df_plot['diff'].mean()

        # Chama o componente visual estilizado
        resultado = ui.render_infografico(alvo, ref, df_plot, outliers, media)

        render = mo.vstack([
            header,
            mo.center(dropdown),
            mo.md("---"),
            resultado
        ])

    render
    return


if __name__ == "__main__":
    app.run()
