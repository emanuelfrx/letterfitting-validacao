import plotly.graph_objects as go
import plotly.express as px
import marimo as mo

class UIComponents:
    @staticmethod
    def render_infografico(alvo, ref, df_plot, outliers, media, m, c):
        # 1. Identificação dos extremos reais
        idx_maior = df_plot['diff'].idxmax()
        fonte_maior = df_plot.loc[idx_maior, 'nome_fonte']
        val_maior = df_plot.loc[idx_maior, 'diff']

        idx_menor = df_plot['diff'].idxmin()
        fonte_menor = df_plot.loc[idx_menor, 'nome_fonte']
        val_menor = df_plot.loc[idx_menor, 'diff']

        # 2. Preparação para a Visão Micro e Tabela (Sincronizados)
        df_sorted_bar = df_plot.sort_values(by='diff', key=abs, ascending=True)
        df_display = df_sorted_bar.tail(150) if len(df_sorted_bar) > 150 else df_sorted_bar

        # 3. Curva em S (Dispersão Ordenada)
        df_scatter = df_plot.sort_values(by='diff')
        fig_scatter = px.scatter(
            df_scatter,
            x='nome_fonte',
            y='diff',
            title="Dispersão de Desvios: Real vs Tracy",
            labels={'diff': 'Diferença (Real - Tracy)', 'nome_fonte': 'Fonte'},
            color=df_scatter['diff'].abs(),
            color_continuous_scale=px.colors.diverging.RdYlGn_r,
            range_color=[0, df_scatter['diff'].abs().max()]

        )

        

        # Linhas de referência na dispersão
        fig_scatter.add_hline(y=0, line_width=3, line_color="#6EBEA3", annotation_text="Padrão Tracy (0)", annotation_position="top left")
        fig_scatter.add_hline(y=media, line_width=2, line_dash="dash", line_color="#8A1E1E", annotation_text=f"Média: {media:.2f}")

        # Ajustes de hover (tooltip) e visual das bolinhas
        fig_scatter.update_traces(
            marker=dict(size=5, opacity=0.8, line=dict(width=1, color='rgba(0,0,0,0.2)')),
            hovertemplate="<b>Fonte:</b> %{x}<br><b>Desvio:</b> %{y:.2f} unidades<extra></extra>"

        )
        fig_scatter.update_layout(
            template="plotly_white",
            height=400,
            margin=dict(l=10, r=10, t=50, b=40),

            # Ocultamos os nomes no eixo X para não virar uma mancha preta, o hover resolve isso
            xaxis=dict(showticklabels=False, title="Fontes (ordenadas pelo desvio)", gridcolor='#f0f0f0', zeroline=False),
            yaxis=dict(gridcolor='#f0f0f0', title="Desvio (unidades)"),
            coloraxis_showscale=False

        )
        # 4. Histograma de Frequência (Posicionado abaixo no vstack)
        fig_hist = px.histogram(
            df_plot, x='diff', nbins=20,
            title="Distribuição dos Desvios",
            labels={'diff': 'Desvio', 'count': 'Qtd de Fontes'},
            color_discrete_sequence=['#8A1E1E']
        )
        fig_hist.update_layout(template="plotly_white", height=350)
        
       # 4. Gráfico de Barras Interativo (Visão Micro)

        fig_bar = px.bar(
            df_display, x='diff', y='nome_fonte', orientation='h',
            title=f"Desvio Detalhado por Fonte ({alvo} vs {ref})",
            color=df_display['diff'].abs(), color_continuous_scale=px.colors.diverging.RdYlGn_r,
            range_color=[0, df_display['diff'].abs().max()]
        )

        fig_bar.update_traces(
            hovertemplate="<b>Fonte:</b> %{y}<br><b>Desvio:</b> %{x:.2f} unidades<extra></extra>",
            marker_line_color='rgba(255,255,255,0.5)', marker_line_width=1
        )

        fig_bar.add_vline(x=0, line_width=4, line_color="#10B981")
        fig_bar.add_vline(x=media, line_width=2, line_dash="dash", line_color="#EF4444")
        fig_bar.update_layout(
            template="plotly_white", height=max(500, len(df_display) * 15),
            margin=dict(l=10, r=10, t=60, b=40), xaxis=dict(gridcolor='#f0f0f0', zeroline=False),
            yaxis=dict(tickfont=dict(size=10), gridcolor='#f8fafc'), coloraxis_showscale=False)
        # 6. Tabela Extraída (Invertida para bater com o topo do gráfico de barras)
        df_table = df_display[['nome_fonte', alvo, ref, 'diff']].iloc[::-1].copy()
        df_table.columns = ['Fonte', f'{alvo} (Real)', f'{ref} (Tracy)', 'Desvio']

        # 7. Montagem do Dashboard
        return mo.vstack([
            mo.md(f"## 🛠️ Diagnóstico de Espaçamento").center(),
            mo.md(f"Análise de coerência baseada na Regra de Walter Tracy").center(),
            
            mo.hstack([
                mo.stat(value=f"{media:.2f}", label="Média Aritmética"),
                mo.stat(value=f"{val_maior:.2f}", label="Maior Desvio", caption=fonte_maior),
                mo.stat(value=f"{val_menor:.2f}", label="Menor Desvio", caption=fonte_menor),
                # FORMULA ATUALIZADA: Exibe nomes reais como Fe e He conforme o menu
                mo.stat(
                    # Usamos o símbolo '·' diretamente ou o formato LaTeX padrão
                    value=f"{alvo} = {m:.2f} · {ref} {c:+.2f}", 
                    label="Fórmula de Regressão",
                    caption="Ajuste Linear (y = ax + b)"
                )
            ], justify="space-around", wrap=True).style({
                "background-color": "#f8fafc", "padding": "25px", "border-radius": "1rem",
                "border": "1px solid #e2e8f0", "margin": "1rem 0"
            }),

            mo.md("### 📈 Visão Macro: Curva e Distribuição"),
            mo.md("*Passe o mouse sobre os pontos fora da linha verde central para identificar as fontes que fogem à regra de Tracy.*"),
            mo.as_html(fig_scatter),
            mo.as_html(fig_hist),

            mo.md("---").style({"margin": "2rem 0", "opacity": "0.3"}),

            mo.md("### 📊 Visão Micro: Análise Individual"),
            mo.md("*Passe o mouse sobre as barras para identificar ao desvio das fontes que mais divergem de Tracy.*"),
            mo.as_html(fig_bar),

            mo.md("---").style({"margin": "2rem 0", "opacity": "0.3"}),
            mo.md("### 🗃️ Dados Tipográficos Extraídos (Sincronizados)"),
            mo.ui.table(df_table, pagination=True).style({
                "background-color": "#ffffff", "border-top": "4px solid #8A1E1E", "padding": "10px"
            })
            
        ]).style({
            "background": "#ffffff", "padding": "40px", "border-radius": "2rem",
            "box-shadow": "0 25px 50px -12px rgba(0, 0, 0, 0.08)", "font-family": "'Inter', sans-serif"
        })