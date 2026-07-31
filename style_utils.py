import streamlit as st
import pandas as pd
import numpy as np

CSS_STYLES = """
<style>
    /* Global Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300..800;1,300..800&family=Archivo+Narrow:ital,wght@0,400..700;1,400..700&family=JetBrains+Mono:ital,wght@0,400..700;1,400..700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #fff9f0;
    }
    
    /* Top Hero Banner / Container */
    .hero-container {
        background: #001f29;
        color: #ffffff;
        padding: 28px 36px;
        border-radius: 16px;
        margin-bottom: 24px;
        border: 1px solid rgba(231, 111, 81, 0.2);
        box-shadow: 0 10px 25px -5px rgba(0, 31, 41, 0.25);
    }
    .hero-title {
        font-family: 'Archivo Narrow', 'Plus Jakarta Sans', sans-serif;
        font-size: 32px;
        font-weight: 700;
        margin: 0 0 8px 0;
        letter-spacing: -0.02em;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 15px;
        color: #abcbdb;
        margin: 0;
        max-width: 850px;
        line-height: 1.6;
    }
    
    /* Metric Cards Grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin-top: 20px;
        margin-bottom: 24px;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #d3daea;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(231, 111, 81, 0.12);
    }
    .metric-card-dark {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 16px 20px;
    }
    .metric-label {
        font-size: 12px;
        font-weight: 600;
        color: #436370;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-label-dark {
        font-size: 12px;
        font-weight: 600;
        color: #abcbdb;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #001f29;
        margin: 0;
    }
    .metric-value-dark {
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }
    .metric-delta {
        font-size: 12px;
        font-weight: 500;
        margin-top: 4px;
        display: inline-block;
    }
    .delta-positive { color: #35b779; }
    .delta-neutral { color: #e76f51; }
    
    /* Section Headers */
    .section-header-title {
        font-family: 'Archivo Narrow', sans-serif;
        font-size: 22px;
        font-weight: 700;
        color: #001f29;
        margin: 24px 0 6px 0;
    }
    .section-subtitle {
        font-size: 14px;
        color: #436370;
        margin-bottom: 20px;
    }

    /* Custom Styled Table Container - Literal Stitch Port */
    .table-card {
        background: #ffffff;
        border-radius: 12px;
        border: 1px solid #d3daea;
        overflow-x: auto;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        text-align: left;
        font-size: 14px;
        color: #001f29;
    }
    .custom-table th {
        background-color: #f8fafc;
        color: #436370;
        font-weight: 600;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 12px 18px;
        border-bottom: 1px solid #d3daea;
        white-space: nowrap;
    }
    .custom-table td {
        padding: 12px 18px;
        border-bottom: 1px solid #f1f5f9;
        white-space: nowrap;
    }
    .custom-table tr:nth-child(even) {
        background-color: #f8fafc;
    }
    .custom-table tr:hover {
        background-color: #f0f3ff;
    }
    .custom-table .text-right {
        text-align: right;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Streamlit Sidebar & Tab Overrides */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #d3daea;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 2px solid #d3daea;
        padding-bottom: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 8px 8px 0 0;
        padding: 0 16px;
        font-weight: 600;
        font-size: 14px;
        color: #436370;
        background-color: transparent;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e76f51 !important;
        color: #ffffff !important;
    }
</style>
"""

def inject_styles():
    st.markdown(CSS_STYLES, unsafe_allow_html=True)

def render_hero_banner(title, subtitle, metrics_list=None):
    metrics_html = ""
    if metrics_list:
        metrics_html = '<div class="metric-grid">'
        for m in metrics_list:
            metrics_html += f"""
            <div class="metric-card-dark">
                <div class="metric-label-dark">{m['label']}</div>
                <div class="metric-value-dark">{m['value']}</div>
            </div>
            """
        metrics_html += '</div>'

    html = f"""
    <div class="hero-container">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
        {metrics_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_metric_cards(metrics):
    """
    metrics: list of dicts [{'label': 'Matches', 'value': '950', 'delta': '+12%'}]
    """
    html = '<div class="metric-grid">'
    for m in metrics:
        delta_html = ""
        if 'delta' in m and m['delta']:
            delta_class = "delta-positive" if not str(m['delta']).startswith('-') else "delta-neutral"
            delta_html = f'<div class="metric-delta {delta_class}">{m["delta"]}</div>'
            
        html += f"""
        <div class="metric-card">
            <div class="metric-label">{m['label']}</div>
            <div class="metric-value">{m['value']}</div>
            {delta_html}
        </div>
        """
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def render_styled_table(df, align_right_cols=None, format_specs=None):
    """
    Renders a pandas DataFrame as a styled HTML table with white card background,
    light grey header, zebra-striped rows, right-aligned monospace numeric columns, and proper formatting.
    """
    if df.empty:
        st.info("No data available to display.")
        return

    df_display = df.copy()
    align_right_cols = align_right_cols or []
    format_specs = format_specs or {}

    # Auto detect numeric columns for right alignment
    for col in df_display.columns:
        if pd.api.types.is_numeric_dtype(df_display[col]) and col not in align_right_cols:
            align_right_cols.append(col)

    # Format values based on format_specs or default rules
    for col in df_display.columns:
        if col in format_specs:
            spec = format_specs[col]
            if spec == 'pct':
                df_display[col] = df_display[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "-")
            elif spec == 'int':
                df_display[col] = df_display[col].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "-")
            elif spec == 'decimal':
                df_display[col] = df_display[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "-")
            elif callable(spec):
                df_display[col] = df_display[col].apply(spec)
        else:
            # Default formatting rules
            if pd.api.types.is_float_dtype(df_display[col]):
                if 'rate' in col.lower() or 'pct' in col.lower() or '%' in col or 'wr' in col.lower() or 'sr' in col.lower():
                    df_display[col] = df_display[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "-")
                else:
                    df_display[col] = df_display[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "-")
            elif pd.api.types.is_integer_dtype(df_display[col]):
                df_display[col] = df_display[col].apply(lambda x: f"{x:,}" if pd.notnull(x) else "-")

    # Build HTML table
    headers_html = "".join([
        f'<th class="{"text-right" if col in align_right_cols else ""}">{col}</th>'
        for col in df_display.columns
    ])

    rows_html = ""
    for idx, row in df_display.iterrows():
        cells_html = ""
        for col in df_display.columns:
            val = str(row[col]) if pd.notnull(row[col]) else "-"
            align_cls = "text-right" if col in align_right_cols else ""
            cells_html += f'<td class="{align_cls}">{val}</td>'
        rows_html += f'<tr>{cells_html}</tr>'

    table_html = f"""
    <div class="table-card">
        <table class="custom-table">
            <thead>
                <tr>{headers_html}</tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)

def apply_plotly_layout(fig, **kwargs):
    """
    Applies exact Stitch color tokens to Plotly figures.
    """
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#001f29"),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=True, gridcolor="#e2e8f0"),
        yaxis=dict(showgrid=True, gridcolor="#e2e8f0")
    )
    for k, v in kwargs.items():
        if k in layout and isinstance(layout[k], dict) and isinstance(v, dict):
            layout[k].update(v)
        else:
            layout[k] = v
    fig.update_layout(**layout)
