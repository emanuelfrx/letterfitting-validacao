import plotly.graph_objects as go
import plotly.express as px
import marimo as mo

class UIComponents:
    @staticmethod
    def render_infografico(alvo, ref, df_plot, outliers, media):
        # 1. Preparação de Dados para o Gráfico
        # Ordenamos para que os maiores erros fiquem no topo
        df_sorted = df_plot.sort_values(by='diff', key=abs, ascending=True)
        
        # Limitamos a visualização se houver muitas fontes para manter a performance
        if len(df_sorted) > 150:
            df_display = df_sorted.tail(150) # Mostra apenas as 150 com mais desvio
        else:
            df_display = df_sorted

        # 2. Criação do Gráfico Interativo (Plotly Express)
        fig = px.bar(
            df_display,
            x='diff',
            y='nome_fonte',
            orientation='h',
            title=f"Desvio Individual por Fonte ({alvo} vs {ref})",
            # Escala de cor divergente: Verde (0) -> Vermelho (Erro Alto)
            color=df_display['diff'].abs(), 
            color_continuous_scale=px.colors.diverging.RdYlGn_r, # Reverso para Verde=Bom
            range_color=[0, df_display['diff'].abs().max()], # Define o limite da escala
            labels={'diff': 'Desvio Teórico (un)', 'nome_fonte': 'Fonte', 'color': 'Magnitude do Erro'}
        )

        # 3. Interatividade e Estilização Avançada (Hover customizado)
        fig.update_traces(
            hovertemplate="<b>Fonte:</b> %{y}<br><b>Desvio Exato:</b> %{x:.2f} unidades<extra></extra>",
            marker_line_color='rgba(255,255,255,0.5)',
            marker_line_width=1
        )

        # 4. Linhas de Contexto (Tracy e Média)
        fig.add_vline(x=0, line_width=4, line_color="#10B981", annotation_text="Padrão Tracy (0)", annotation_position="top left")
        fig.add_vline(x=media, line_width=2, line_dash="dash", line_color="#EF4444", annotation_text=f"Média Atual: {media:.2f}")

        # 5. Layout do Gráfico (Clean e Responsivo)
        # Altura dinâmica para acomodar os nomes das fontes
        chart_height = max(500, len(df_display) * 15)
        
        fig.update_layout(
            template="plotly_white",
            height=chart_height,
            margin=dict(l=10, r=10, t=60, b=40),
            xaxis=dict(gridcolor='#f0f0f0', zeroline=False),
            yaxis=dict(tickfont=dict(size=10), gridcolor='#f8fafc'),
            coloraxis_showscale=False # Esconde a barra de cor lateral para limpar o visual
        )

        # 6. Montagem do Dashboard Card (Marimo vstack com CSS)
        return mo.vstack([
            # Cabeçalho de Contexto
            mo.md(f"## 🛠️ Diagnóstico de Espaçamento").center(),
            mo.md(f"Análise de coerência teórica para a regra: **`{alvo}`** deve ser igual a **`{ref}`**.").center(),
            
            # Cards de Estatísticas Rápidas
            mo.hstack([
                mo.stat(value=f"{media:.2f}", label="Tendência Central", caption="Desvio médio da família (ideal é 0)"),
                mo.stat(value=f"{len(outliers)}", label="Fontes Críticas", caption="Exigem correção manual urgente"),
                mo.stat(value=f"{len(df_plot)}", label="Amostra Analisada", caption="Total de fontes no set atual")
            ], justify="space-around").style({
                "background-color": "#f8fafc",
                "padding": "25px",
                "border-radius": "1rem",
                "border": "1px solid #e2e8f0",
                "margin": "1rem 0"
            }),

            # O Gráfico Interativo
            mo.md("### 📊 Mapa de Coerência Teórica (Passe o mouse nas barras)"),
            mo.as_html(fig),

            # Tabela de Correção (Contexto de ação)
            mo.md("---"),
            mo.md("### 🚨 Relatório de Ação: Prioridades de Ajuste"),
            mo.md("Abaixo estão as fontes que estão 'quebrando' a regra teórica com maior intensidade, ordenadas pelo tamanho do erro:"),
            mo.ui.table(
                outliers[['nome_fonte', 'diff']].head(12),
                label="Top 12 Outliers (Ajustes Prioritários)"
            )
        ]).style({
            "background": "#ffffff",
            "padding": "40px",
            "border-radius": "2rem",
            "box-shadow": "0 25px 50px -12px rgba(0, 0, 0, 0.08)",
            "font-family": "'Inter', 'Segoe UI', sans-serif"
        })