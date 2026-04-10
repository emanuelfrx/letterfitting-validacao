import plotly.graph_objects as go
import plotly.express as px
import marimo as mo

class UIComponents:
    @staticmethod
    def render_infografico(alvo, ref, df_plot, outliers, media):
        # 1. Cálculos Adicionais: Maior e Menor Desvio Absoluto
        idx_maior = df_plot['diff'].abs().idxmax()
        fonte_maior = df_plot.loc[idx_maior, 'nome_fonte']
        val_maior = df_plot.loc[idx_maior, 'diff']

        idx_menor = df_plot['diff'].abs().idxmin()
        fonte_menor = df_plot.loc[idx_menor, 'nome_fonte']
        val_menor = df_plot.loc[idx_menor, 'diff']

        # 2. Preparação para a Visão Micro (Gráfico de Barras)
        df_sorted_bar = df_plot.sort_values(by='diff', key=abs, ascending=True)
        df_display = df_sorted_bar.tail(150) if len(df_sorted_bar) > 150 else df_sorted_bar


        # --- GRÁFICO 1: DISPERSÃO SEQUENCIAL (ITERATIVO) ---
        # Mantém a ordem original do DataFrame (ordem dos dados/CSV)
        fig_normal = px.scatter(
            df_plot,
            x='nome_fonte',
            y='diff',
            title="Dispersão Sequencial (Passe o mouse)",
            labels={'diff': 'Desvio', 'nome_fonte': 'Fonte'},
            hover_name='nome_fonte',  # Torna iterativo exibindo o nome no topo do card
            color=df_plot['diff'].abs(),
            color_continuous_scale=px.colors.diverging.RdYlGn_r,
            range_color=[0, df_plot['diff'].abs().max()]
        )
        
        fig_normal.add_hline(y=0, line_width=2, line_color="#10B981", opacity=0.5)
        fig_normal.add_hline(y=media, line_width=1, line_dash="dash", line_color="#EF4444", opacity=0.5)
        
        fig_normal.update_traces(
            marker=dict(size=5, opacity=0.7, line=dict(width=1, color='rgba(255,255,255,0.3)')),
            hovertemplate="<b>%{hovertext}</b><br>Desvio: %{y:.2f}<extra></extra>"
        )
        
        fig_normal.update_layout(
            template="plotly_white", 
            height=400, 
            xaxis_showticklabels=False, # Esconde nomes no eixo X para evitar poluição
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=50, b=10)
        )
        # 3. NOVO: Criação do Gráfico de Dispersão (Visão Macro Interativa)
        # Ordenamos pelo desvio para formar uma curva "S" suave e facilitar a leitura
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
            yaxis=dict(tickfont=dict(size=10), gridcolor='#f8fafc'), coloraxis_showscale=False
        )

        # 5. Montagem do Dashboard
        return mo.vstack([
            mo.md(f"## 🛠️ Diagnóstico de Espaçamento").center(),
            mo.md(f"Análise de coerência: A regra exige que **`{alvo}`** seja igual a **`{ref}`**.").center(),
            
            # Cards de Estatísticas Atualizados
            mo.hstack([
                mo.stat(value=f"{media:.2f}", label="Média Aritmética", caption="Desvio médio da família"),
                mo.stat(value=f"{val_maior:.2f}", label="Maior Desvio", caption=f"Fonte: {fonte_maior}"),
                mo.stat(value=f"{val_menor:.2f}", label="Menor Desvio", caption=f"Fonte: {fonte_menor}"),
                mo.stat(value=f"{len(outliers)}", label="Outliers Críticos", caption="Fora da curva estatística")
            ], justify="space-around", wrap=True).style({
                "background-color": "#f8fafc", "padding": "25px", "border-radius": "1rem",
                "border": "1px solid #e2e8f0", "margin": "1rem 0"
            }),

            # Dispersão
            mo.md("### 📈 Visão Macro: Dispersão dos Desvios"),
            mo.md("*Passe o mouse sobre os pontos fora da linha verde central para identificar as fontes que fogem à regra de Tracy.*"),
            mo.as_html(fig_scatter),
            mo.as_html(fig_normal),

            mo.md("---").style({"margin": "2rem 0", "opacity": "0.3"}),

            # Barras
            mo.md("### 📊 Visão Micro: Análise Individual"),
            mo.as_html(fig_bar),

            mo.md("---").style({"margin": "2rem 0", "opacity": "0.3"}),
            mo.md("### 🚨 Relatório de Ação: Prioridades de Ajuste"),
            mo.ui.table(outliers[['nome_fonte', 'diff']].head(12), label="Top 12 Outliers (Ajustes Prioritários)")
        ]).style({
            "background": "#ffffff", "padding": "40px", "border-radius": "2rem",
            "box-shadow": "0 25px 50px -12px rgba(0, 0, 0, 0.08)", "font-family": "'Inter', sans-serif"
        })