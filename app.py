import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px

    # 1. Carregamento e Preparação
    df = pd.read_csv("dados.csv")

    # Colunas necessárias conforme sua revisão
    colunas_iguais = [
        'Be', 'He', 'Ce', 'Oe', 'Cd', 'Od', 'De', 'Dd', 'Ee', 'Fe', 'Ge', 'Ie', 'Id', 'Ke', 'Le', 'Me', 'Md', 'Ne', 'Nd', 'Pe', 'Qe', 'Qd', 'Re', 'Ue',
        'bd', 'ne', 'ce', 'oe', 'de', 'dd', 'ee', 'ge', 'hd', 'id', 'je', 'jd', 'ke', 'le', 'ld', 'me', 'md', 'nd', 'pd', 'qe', 'qd', 're', 'ue', 'ud'
    ]

    for col in colunas_iguais:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df_analise = df[df['manter_na_analise?'] == 'Sim'].copy()

    # 2. Definição das Regras de IGUALDADE (Revisão estrita das minúsculas)
    regras_raw = [
        # MAIÚSCULAS (Ref: He=H esq, Oe=O esq, Od=O dir)
        ('Be', 'He', "B esquerdo = H esquerdo"),
        ('Ce', 'Oe', "C esquerdo = O esquerdo"),
        ('De', 'He', "D esquerdo = H esquerdo"),
        ('Dd', 'Od', "D direito = O direito"),
        ('Ee', 'He', "E esquerdo = H esquerdo"),
        ('Fe', 'He', "F esquerdo = H esquerdo"),
        ('Ge', 'Oe', "G esquerdo = O esquerdo"),
        ('Ie', 'He', "I esquerdo = H esquerdo"),
        ('Id', 'He', "I direito = H esquerdo"),
        ('Ke', 'He', "K esquerdo = H esquerdo"),
        ('Le', 'He', "L esquerdo = H esquerdo"),
        ('Me', 'He', "M esquerdo = H esquerdo"),
        ('Md', 'He', "M direito = H esquerdo"),
        ('Ne', 'He', "N esquerdo = H esquerdo"),
        ('Nd', 'He', "N direito = H esquerdo"),
        ('Pe', 'He', "P esquerdo = H esquerdo"),
        ('Qe', 'Oe', "Q esquerdo = O esquerdo"),
        ('Qd', 'Od', "Q direito = O direito"),
        ('Re', 'He', "R esquerdo = H esquerdo"),
        ('Ue', 'He', "U esquerdo = H esquerdo"),

        # MINÚSCULAS (Ref: ne=n esq, nd=n dir, oe=o esq, od=o dir)
        ('bd', 'nd', "b direito = n direito"),
        ('ce', 'oe', "c esquerdo = o esquerdo"),
        ('de', 'oe', "d esquerdo = o esquerdo"),
        ('dd', 'nd', "d direito = n direito"),
        ('ee', 'oe', "e esquerdo = o esquerdo"),
        ('ge', 'oe', "g esquerdo = o esquerdo"),
        ('hd', 'nd', "h direito = n direito"),
        ('id', 'nd', "i direito = n direito"),
        ('je', 'ne', "j esquerdo = n esquerdo"), # j segue a curva do o na base em algumas construções
        ('jd', 'nd', "j direito = n direito"),
        ('ke', 'ne', "k esquerdo = n esquerdo"),
        ('le', 'ne', "l esquerdo = n esquerdo"),
        ('ld', 'nd', "l direito = n direito"),
        ('me', 'ne', "m esquerdo = n esquerdo"),
        ('md', 'nd', "m direito = n direito"),
        ('pd', 'nd', "p direito = n direito"), # pd no lugar de pe como solicitado
        ('qe', 'oe', "q esquerdo = o esquerdo"),
        ('qd', 'od', "q direito = o direito"),
        ('re', 'ne', "r esquerdo = n esquerdo"),
        ('ue', 'ne', "u esquerdo = n esquerdo"),
        ('ud', 'nd', "u direito = n direito")
    ]

    # Ordenação: Maiúsculas (A-Z) -> Minúsculas (A-Z)
    regras_ordenadas = sorted(regras_raw, key=lambda x: (x[0].islower(), x[2]))

    selecao = mo.ui.dropdown(
        options={desc: (alvo, ref) for alvo, ref, desc in regras_ordenadas},
        label="Regras de Igualdade (Tracy)",
        value=None
    )


    return df_analise, mo, px, selecao


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _(df_analise, mo, px, selecao):
    mo.stop(selecao.value is None, mo.md("Selecione uma regra no menu acima."))

    # 1. Extração dos dados da seleção
    # selecao.value retorna o par (alvo, ref)
    alvo_col, ref_col = selecao.value

    # Para recuperar o texto amigável do dropdown, podemos fazer uma busca reversa ou 
    # simplesmente formatar uma string nova para o título
    titulo_regra = f"Análise: {alvo_col} deve ser igual a {ref_col}"

    # 2. Preparação dos Dados
    df_clean = df_analise.dropna(subset=[alvo_col, ref_col])
    diferencas = df_clean[alvo_col] - df_clean[ref_col]
    media_simples = diferencas.mean()

    # 3. Histograma Centrado
    fig = px.histogram(
        diferencas[diferencas != 0],
        nbins=30,
        labels={'value': 'Desvio (unidades)', 'count': 'Qtd. Fontes'},
        color_discrete_sequence=['#4F46E5'],
        opacity=0.8
    )

    # Escala Simétrica para o Zero ficar no meio
    max_val = max(abs(diferencas.min() if not diferencas.empty else 0), 
                  abs(diferencas.max() if not diferencas.empty else 0), 20)

    fig.update_layout(
        xaxis=dict(range=[-max_val, max_val], zeroline=True, zerolinecolor='black'),
        plot_bgcolor='white',
        height=450,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    fig.add_vline(x=0, line_width=2, line_color="#10B981") # Tracy (Ideal)
    fig.add_vline(x=media_simples, line_width=2, line_color="#EF4444", line_dash="dash") # Média Real

    # 4. Interface de Saída (Corrigida sem acessar .label)
    mo.vstack([
        mo.md(f"### {titulo_regra}"),
        mo.hstack([
            mo.stat(value=f"{media_simples:.2f}", label="Média das Diferenças"),
            mo.stat(value=f"{len(df_clean)}", label="Fontes Analisadas"),
        ], justify="start"),
        mo.as_html(fig),
        mo.md(f"**Legenda:** Linha verde = Padrão Tracy (0). Linha vermelha tracejada = Média real das fontes.")
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
