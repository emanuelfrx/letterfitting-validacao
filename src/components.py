# ─────────────────────────────────────────────────────────────
#  components.py  — Peças de UI reutilizáveis (sem lógica)
# ─────────────────────────────────────────────────────────────
import pandas as pd
import plotly.graph_objects as go
import marimo as mo


from src.analytics import AnalysisResult


# ══════════════════════════════════════════════════════════════
#  SISTEMA DE DESIGN
#  Paleta restrita: 1 accent + slate + semântica de dados
# ══════════════════════════════════════════════════════════════


# Cores base
_INK       = "#111827"
_BODY      = "#374151"
_MUTED     = "#6B7280"
_SUBTLE    = "#94A3B8"
_BG        = "#F6F8FB"
_SURFACE   = "#FFFFFF"
_BORDER    = "#E2E8F0"
_BORDER_SM = "#F1F5F9"

_ACCENT    = "#2563EB"
_ACCENT_BG = "#EFF6FF"

_POS       = "#059669"
_NEG       = "#DC2626"
_ZERO      = "#64748B"
_WARN      = "#D97706"   # amber   — média / outlier leve


# Tipografia
_FONT      = "'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif"
_MONO      = "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace"


# Escala tipográfica
_T_XS  = "0.75rem"    # 11.5px — captions, labels superiores
_T_SM  = "0.875rem"  # 13px   — labels de campo, meta
_T_MD  = "1rem"  # 15px   — body padrão
_T_LG  = "1.25rem"  # 18px   — subtítulos de seção
_T_XL  = "2rem"   # 28px   — valores KPI



# ══════════════════════════════════════════════════════════════
#  UTILITÁRIOS INTERNOS
# ══════════════════════════════════════════════════════════════


def _dot(color: str, size: int = 8) -> str:
    """Indicador circular de cor — substitui emoji como ícone."""
    return (f"<span style='display:inline-block;width:{size}px;height:{size}px;"
            f"border-radius:50%;background:{color};flex-shrink:0'></span>")




def _chip(text: str, color: str = _ACCENT, bg: str = _ACCENT_BG) -> str:
    """Badge/chip de texto — sem emoji, tipografia pura."""
    return (f"<span style='display:inline-flex;align-items:center;"
            f"font-size:{_T_XS};font-weight:600;color:{color};"
            f"background:{bg};border:1px solid {color}22;"
            f"border-radius:999px;padding:.2rem .65rem;"
            f"letter-spacing:.04em;white-space:nowrap'>{text}</span>")




def _kpi(value: str, label: str, caption: str = "",
         color: str = _ACCENT, mono: bool = False) -> str:
    """Card KPI — valor grande, label pequeno, linha accent lateral."""
    vfont = f"font-family:{_MONO};" if mono else ""
    cap_html = ""
    if caption:
        cap_html = (f"<div style='margin-top:.4rem;font-size:{_T_XS};"
                    f"color:{_MUTED};white-space:nowrap;overflow:hidden;"
                    f"text-overflow:ellipsis;max-width:190px'>{caption}</div>")
    return f"""
<div style='
    background:{_SURFACE}; border:1px solid {_BORDER};
    border-radius:.75rem; padding:1.1rem 1.25rem 1rem;
    border-top:4px solid {color}; flex:1; min-width:130px;
'>
    <div style='
        font-size:{_T_XS}; font-weight:600; color:{_MUTED};
        text-transform:uppercase; letter-spacing:.09em; margin-bottom:.55rem;
        display:flex; align-items:center; gap:.4rem;
    '>{label}</div>
    <div style='
        font-size:{_T_XL}; font-weight:700; color:{_INK};
        letter-spacing:-1px; line-height:1; {vfont}
        word-break:break-all;
    '>{value}</div>
    {cap_html}
</div>"""




# ══════════════════════════════════════════════════════════════
#  PLOTLY — TEMA COMPARTILHADO
# ══════════════════════════════════════════════════════════════


def _layout_base(title_text: str, height: int) -> dict:
    return dict(
        title=dict(
            text=title_text,
            font=dict(
                size=18,
                color=_INK,
                family=_FONT,
            ),
            x=0,
            xanchor="left",
        ),

        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        height=height,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=50,
        ),

        font=dict(
            family=_FONT,
            color=_BODY,
            size=12,
        ),

        hoverlabel=dict(
            bgcolor="#111827",
            font_color="white",
            bordercolor="#111827",
            font_family=_FONT,
            font_size=12,
        ),

        showlegend=False,
    )

def _axis_x(title: str = "", show_labels: bool = True) -> dict:
    return dict(
        title=dict(
            text=title,
            font=dict(
                size=12,
                color=_BODY,
            ),
        ),

        tickfont=dict(
            color=_MUTED,
            family=_FONT,
            size=11,
        ),

        gridcolor="#E2E8F0",
        gridwidth=1,

        linecolor="#CBD5E1",
        linewidth=1,

        zeroline=False,

        showticklabels=show_labels,
    )



def _axis_y(title: str = "") -> dict:
    return dict(
        title=dict(
            text=title,
            font=dict(
                size=12,
                color=_BODY,
            ),
        ),

        tickfont=dict(
            color=_MUTED,
            family=_FONT,
            size=11,
        ),

        gridcolor="#E2E8F0",
        gridwidth=1,

        linecolor="#CBD5E1",
        linewidth=1,

        zeroline=False,
    )




# ══════════════════════════════════════════════════════════════
#  COMPONENTES PÚBLICOS
# ══════════════════════════════════════════════════════════════


def header_banner() -> mo.Html:
    return mo.md(f"""
<div style='
    background:{_INK}; color:#F9FAFB;
    padding:1.75rem 2rem; border-radius:1rem;
    margin-bottom:1.75rem;
    display:flex; align-items:center; justify-content:space-between;
    gap:1rem;
'>
    <div>
        <div style='margin-bottom:.6rem'>
            {_chip("● Sistema Ativo", "#34D399", "#022C22")}
        </div>
        <h1 style='
            margin:0; font-size:1.75rem; font-weight:700;
            letter-spacing:-.5px; line-height:1.2; color:#F9FAFB;
        '>Validação Estatística de Espaçamento</h1>
        <p style='
            margin:.4rem 0 0; font-size:{_T_SM}; color:#6B7280;
            letter-spacing:.02em;
        '>Análise de outliers pelo método Walter Tracy · Regressão linear (np.polyfit)</p>
    </div>
    <div style='
        text-align:right; font-size:{_T_XS}; color:#4B5563;
        font-family:{_MONO}; line-height:2; flex-shrink:0;
    '>
        <div style='color:#6366F1'>z-score &gt; 1.0</div>
        <div>polyfit · grau 1</div>
    </div>
</div>""")




def kpi_cards(result: AnalysisResult, alvo: str, ref: str) -> mo.Html:
    """Faixa de 5 KPIs com escala tipográfica coerente."""
    n_out = len(result.outliers)
    pct   = f"{n_out / result.n_fontes * 100:.1f}%" if result.n_fontes else "—"
    formula = f"{alvo} = {result.m:.4f}·{ref} {result.c:+.4f}"


    cards = "".join([
        _kpi(str(result.n_fontes),         "Fontes analisadas",  color=_ACCENT),
        _kpi(f"{result.media:+.3f}",        "Média do desvio",    color=_ZERO),
        _kpi(f"{result.val_maior:+.2f}",    "Maior desvio",
             caption=result.fonte_maior,    color=_NEG),
        _kpi(f"{result.val_menor:+.2f}",    "Menor desvio",
             caption=result.fonte_menor,    color=_POS),
        _kpi(pct,                           f"Outliers  ({n_out})", color=_WARN),
        _kpi(formula, "Regressão linear",
             caption="Ajuste via np.polyfit", color=_ZERO, mono=True),
    ])


    return mo.md(f"""
<div style='
    display:flex; flex-wrap:wrap; gap:.75rem;
    background:{_BG}; border:1px solid {_BORDER};
    border-radius:1rem; padding:1.25rem;
    margin:.25rem 0 2rem;
'>{cards}</div>""")



def chart_scatter(result: AnalysisResult) -> mo.Html:

    df = result.df_plot.sort_values(by='diff').reset_index(drop=True)

    point_colors = []

    for v in df["diff"]:
        if abs(v) > 1:
            point_colors.append(_NEG)
        else:
            point_colors.append("#64748B")

    fig = go.Figure()

    fig.add_hrect(
        y0=-0.5,
        y1=0.5,
        fillcolor="rgba(37,99,235,0.06)",
        line_width=0,
        layer="below",
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["diff"],
            mode="markers",
            marker=dict(
                size=5,
                color=point_colors,
                opacity=0.85,
            ),
            text=df["nome_fonte"],
            hovertemplate="<b>%{text}</b><br>Desvio: %{y:+.3f}<extra></extra>",
        )
    )

    layout = _layout_base(
        "Curva-S dos Desvios",
        500,
    )

    layout.update(
        xaxis=_axis_x(
            "Fontes ordenadas pelo desvio",
            show_labels=False,
        ),
        yaxis=_axis_y("Desvio"),
    )

    fig.update_layout(**layout)

    return mo.as_html(fig)


def chart_histogram(result: AnalysisResult) -> mo.Html:
    df = result.df_plot
    mean = result.media
    
    fig = go.Figure()

    # O bin_size de 0.5 com start de -20.25 coloca o 0 exatamente no centro de um bin
    fig.add_trace(go.Histogram(
        x=df['diff'],
        xbins=dict(
            start=-20.25, 
            size=0.5
        ),
        marker_color='#3B82F6',
        marker_line_color='#FFFFFF',
        marker_line_width=1,
        opacity=0.9,
        hovertemplate="Desvio Central: %{x}<br>Qtd. de Fontes: %{y}<extra></extra>"
    ))

    # Adiciona a linha da média
    fig.add_vline(x=mean, line_dash="solid", line_color="orange", 
                  annotation_text=f"μ={mean:.2f}")

    # Centraliza o eixo X para ter simetria visual
    # Ajuste o range [-20, 20] conforme a necessidade do seu zoom
    fig.update_layout(
        title="Distribuição dos Desvios",
        xaxis=dict(
            title="Desvio",
            range=[-20, 20], 
            dtick=2 # Mostra marcações a cada 2.5 unidades para limpar o gráfico
        ),
        yaxis_title="Qtd. de fontes",
        bargap=0.05,
        template="plotly_white"
    )

    return mo.ui.plotly(fig)
    """Distribuição dos desvios com foco centralizado e barras robustas."""
    df   = result.df_plot
    mean = result.media
    
    # 1. Definimos um intervalo de zoom agressivo para evitar o achatamento
    # Isso foca no "miolo" da distribuição (ex: -10 a 10)
    # Ajuste o range conforme a necessidade dos seus dados reais
    zoom_range = [-10, 20]
    
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=df['diff'], 
        # Aumentamos o tamanho do bin para agrupar melhor os dados
        xbins=dict(start=-0, end=10, size=0.5), 
        marker_color=_ACCENT,
        marker_line_color=_SURFACE,
        marker_line_width=1, # Adiciona uma borda fina para definir a barra
        opacity=0.9,
        hovertemplate="Desvio: %{x:.2f}<br>Fontes: %{y}<extra></extra>",
    ))

    # 2. Linha da média para dar contexto
    fig.add_vline(x=mean, line_color=_WARN, line_width=2)

    layout = _layout_base("Distribuição dos Desvios ", 280)
    layout.update(
        bargap=0.05, # Espaço quase nulo entre barras deixa elas mais largas
        xaxis=dict(
            title="Desvio",
            range=zoom_range, # Força o zoom no centro
            gridcolor=_BORDER_SM
        ),
        yaxis=_axis_y("Qtd. de fontes"),
    )
    fig.update_layout(**layout)
    return mo.as_html(fig)
    df = result.df_plot
    mean = result.media
    std = df["diff"].std()

    fig = go.Figure()

    # Adicionar sombreamento da área central (zona de 1 sigma)
    fig.add_vrect(
        x0=mean - std, x1=mean + std,
        fillcolor="rgba(37, 99, 235, 0.1)", line_width=0, layer="below"
    )

    # Histograma
    fig.add_trace(go.Histogram(
        x=df["diff"],
        marker_color=_ACCENT,
        opacity=0.8,
        # Deixe o Plotly decidir o melhor número de bins ou defina um tamanho fixo
        xbins=dict(size=0.5) 
    ))

    # Apenas a linha da média com anotação clara
    fig.add_vline(x=mean, line_color=_WARN, line_width=2, 
                  annotation_text=f"μ={mean:.2f}", annotation_position="top right")

    # Linhas de sigma sem texto, apenas como referência visual
    fig.add_vline(x=mean + std, line_dash="dash", line_color=_MUTED, line_width=1)
    fig.add_vline(x=mean - std, line_dash="dash", line_color=_MUTED, line_width=1)

    # Configuração de layout limpa
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Desvio da Regra",
        yaxis_title="Fontes",
        bargap=0.05
    )

    return mo.as_html(fig)


def chart_bar_detail(result: AnalysisResult, alvo: str, ref: str) -> mo.Html:
    """Barras horizontais — desvio individual, coloridas por magnitude."""
    df = (result.df_plot
          .sort_values(by='diff', key=abs, ascending=True)
          .pipe(lambda d: d[d['diff'] != 0])
          .reset_index(drop=True))


    abs_max = max(df['diff'].abs().max(), 0.001)


    # Escala contínua de cor: verde (perto de zero) → vermelho (longe)
    def _bar_color(v: float) -> str:
        t = abs(v) / abs_max  # 0 → 1
        if t < 0.4:
            return _POS
        elif t < 0.72:
            return _WARN
        else:
            return _NEG


    colors = [_bar_color(v) for v in df['diff']]


    fig = go.Figure()


    fig.add_trace(go.Bar(
        x=df['diff'], y=df['nome_fonte'],
        orientation='h',
        marker=dict(
            color=colors, opacity=0.95,
            line=dict(width=0),
        ),
        text=df['diff'].apply(lambda v: f"{v:+.2f}"),
        textposition='outside',
        textfont=dict(size=9, color=_MUTED, family=_MONO),
        hovertemplate="<b>%{y}</b><br>Desvio: %{x:+.3f}<extra></extra>",
        name="",
    ))


    # Linha zero — referência Tracy
    fig.add_vline(
        x=0, line_color=_ZERO, line_width=1.5,
        annotation_text="Ideal Tracy",
        annotation_font_color=_ZERO,
        annotation_font_size=10,
        annotation_position="top right",
    )


    # Linha da média
    fig.add_vline(
        x=result.media, line_color=_WARN, line_width=1,
        line_dash="dash",
        annotation_text=f"μ {result.media:+.3f}",
        annotation_font_color=_WARN,
        annotation_font_size=10,
        annotation_position="top left",
    )


    layout = _layout_base(
        f"Desvio Individual por Fonte  ·  {alvo}  vs  {ref}",
        max(460, len(df) * 17),
    )
    layout.update(
        margin=dict(l=12, r=64, t=44, b=36),
        xaxis=_axis_x("Desvio (unidades)"),
        yaxis=dict(
            tickfont=dict(size=9.5, color=_BODY, family=_FONT),
            gridcolor=_BORDER_SM, linecolor=_BORDER,
            zeroline=False,
        ),
    )
    fig.update_layout(**layout)
    return mo.as_html(fig)




def table_typography(result: AnalysisResult, alvo: str, ref: str,
                     df_ff: pd.DataFrame) -> mo.Html:
    """Tabela de dados tipográficos com merge opcional do FontForge."""
    df = (result.df_plot
          .sort_values(by='diff', key=abs, ascending=True)
          [['nome_fonte', alvo, ref, 'ideal']]
          .iloc[::-1]
          .copy())
    df['ideal'] = df['ideal'].round(2)


    has_ff = (df_ff is not None and not df_ff.empty
              and 'nome_fonte' in df_ff.columns and alvo in df_ff.columns)
    if has_ff:
        df = pd.merge(df, df_ff[['nome_fonte', alvo]], on='nome_fonte',
                      how='left', suffixes=('', '_ff'))
        col_ff = f"{alvo}_ff" if f"{alvo}_ff" in df.columns else alvo
        df = df[['nome_fonte', alvo, ref, 'ideal', col_ff]]
        df.columns = ['Fonte', f'{alvo} (Original)', f'{ref} (Referência)',
                      'Ideal Tracy', f'{alvo} (FontForge)']
    else:
        df.columns = ['Fonte', f'{alvo} (Original)', f'{ref} (Referência)', 'Ideal Tracy']


    return mo.ui.table(df, pagination=True).style({
        "font-family": _FONT,
        "font-size": _T_SM,
        "background-color": _SURFACE,
        "border": f"1px solid {_BORDER}",
        "border-radius": ".75rem",
        "overflow": "hidden",
    })




def section_divider(num: str, title: str, subtitle: str = "") -> mo.Html:
    """Cabeçalho de seção com accent lateral — integrado à página."""
    sub_html = ""
    if subtitle:
        sub_html = (f"<p style='margin:.25rem 0 0;font-size:{_T_SM};"
                    f"color:{_MUTED};font-weight:400'>{subtitle}</p>")
    return mo.md(f"""
<div style='
    border-left:5px solid {_ACCENT}; padding:.1rem 0 .1rem 1rem;
    margin:3rem 0 1.5rem;
'>
    <div style='
        font-size:{_T_XS}; font-weight:700; color:{_ACCENT};
        text-transform:uppercase; letter-spacing:.12em; margin-bottom:.3rem;
    '>Seção {num}</div>
    <h3 style='margin:0;font-size:{_T_LG};font-weight:600;color:{_INK}'>{title}</h3>
    {sub_html}
</div>""")




def empty_state(n_regras: int) -> mo.Html:
    """Tela inicial: instrução clara, sem decoração desnecessária."""
    return mo.md(f"""
<div style='
    text-align:center; padding:4rem 2rem;
    background:{_SURFACE}; border:1px solid {_BORDER};
    border-radius:1rem; margin:1rem 0;
    font-family:{_FONT};
'>
    <div style='
        width:48px; height:48px; border-radius:.75rem;
        background:{_ACCENT_BG}; border:1px solid {_ACCENT}33;
        display:flex; align-items:center; justify-content:center;
        margin:0 auto 1.25rem; font-size:1.35rem;
    '>◈</div>
    <h2 style='
        color:{_INK}; font-size:1.2rem; font-weight:600;
        margin:0 0 .5rem; letter-spacing:-.3px;
    '>Selecione uma regra tipográfica</h2>
    <p style='
        color:{_MUTED}; font-size:{_T_MD}; margin:0 0 1.75rem;
        max-width:400px; margin-inline:auto; line-height:1.6;
    '>
        Escolha uma regra para calcular desvios, identificar outliers e visualizar os resultados estatísticos.
    </p>
    {_chip(f"{n_regras} regras disponíveis  ·  maiúsculas e minúsculas")}
</div>""")