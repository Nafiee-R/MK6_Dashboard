"""
Global Superstore Analytics Dashboard
Week 3 — Business Analytics | MK6
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Global Superstore Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Theme System
# ─────────────────────────────────────────────
THEMES = {
    "☀️ Light Indigo": {
        "bg": "#F8FAFC",
        "card_bg": "rgba(255,255,255,0.85)",
        "card_border": "rgba(99,102,241,0.15)",
        "text": "#1E293B",
        "text_secondary": "#64748B",
        "accent": "#4F46E5",
        "accent_light": "#EEF2FF",
        "positive": "#10B981",
        "negative": "#EF4444",
        "plotly_template": "plotly_white",
        "plotly_colors": px.colors.qualitative.Pastel,
        "gradient_bar": ["#6366F1", "#818CF8", "#A5B4FC", "#C7D2FE"],
        "sidebar_bg": "#EEF2FF",
    },
    "🌊 Ocean Breeze": {
        "bg": "#F0FDFA",
        "card_bg": "rgba(255,255,255,0.9)",
        "card_border": "rgba(20,184,166,0.2)",
        "text": "#134E4A",
        "text_secondary": "#5EEAD4",
        "accent": "#0D9488",
        "accent_light": "#CCFBF1",
        "positive": "#059669",
        "negative": "#DC2626",
        "plotly_template": "plotly_white",
        "plotly_colors": px.colors.qualitative.Set2,
        "gradient_bar": ["#0D9488", "#14B8A6", "#5EEAD4", "#99F6E4"],
        "sidebar_bg": "#CCFBF1",
    },
    "🌸 Rose Petal": {
        "bg": "#FFF1F2",
        "card_bg": "rgba(255,255,255,0.88)",
        "card_border": "rgba(244,63,94,0.15)",
        "text": "#1C1917",
        "text_secondary": "#78716C",
        "accent": "#E11D48",
        "accent_light": "#FFE4E6",
        "positive": "#16A34A",
        "negative": "#DC2626",
        "plotly_template": "plotly_white",
        "plotly_colors": px.colors.qualitative.Pastel1,
        "gradient_bar": ["#E11D48", "#FB7185", "#FDA4AF", "#FECDD3"],
        "sidebar_bg": "#FFE4E6",
    },
    "🌙 Dark Elegant": {
        "bg": "#0F172A",
        "card_bg": "rgba(30,41,59,0.85)",
        "card_border": "rgba(99,102,241,0.3)",
        "text": "#F1F5F9",
        "text_secondary": "#94A3B8",
        "accent": "#818CF8",
        "accent_light": "#1E293B",
        "positive": "#34D399",
        "negative": "#F87171",
        "plotly_template": "plotly_dark",
        "plotly_colors": px.colors.qualitative.Pastel,
        "gradient_bar": ["#818CF8", "#6366F1", "#4F46E5", "#4338CA"],
        "sidebar_bg": "#1E293B",
    },
}

# ─────────────────────────────────────────────
# CSS Injection
# ─────────────────────────────────────────────
def inject_css(theme):
    t = THEMES[theme]
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Global */
        html, body, .stApp {{
            font-family: 'Inter', sans-serif !important;
            background-color: {t['bg']} !important;
            color: {t['text']} !important;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background: {t['sidebar_bg']} !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown {{
            color: {t['text']} !important;
        }}

        /* Hide default header */
        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}

        /* KPI Card */
        .kpi-card {{
            background: {t['card_bg']};
            backdrop-filter: blur(12px);
            border: 1px solid {t['card_border']};
            border-radius: 16px;
            padding: 24px 20px;
            text-align: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }}
        .kpi-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }}
        .kpi-label {{
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: {t['text_secondary']};
            margin-bottom: 6px;
        }}
        .kpi-value {{
            font-size: 1.85rem;
            font-weight: 800;
            color: {t['accent']};
            line-height: 1.1;
        }}
        .kpi-delta {{
            font-size: 0.82rem;
            font-weight: 600;
            margin-top: 6px;
        }}
        .kpi-delta.positive {{ color: {t['positive']}; }}
        .kpi-delta.negative {{ color: {t['negative']}; }}

        /* Section Title */
        .section-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: {t['text']};
            margin: 28px 0 12px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid {t['accent']};
            display: inline-block;
        }}

        /* Page Title */
        .page-title {{
            font-size: 1.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, {t['accent']}, {t['gradient_bar'][1]});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 4px;
        }}
        .page-subtitle {{
            font-size: 0.92rem;
            color: {t['text_secondary']};
            margin-bottom: 20px;
        }}

        /* Plotly charts bg */
        .stPlotlyChart {{
            border-radius: 12px;
            overflow: hidden;
        }}

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px 8px 0 0;
            font-weight: 600;
        }}

        /* DataFrame */
        .stDataFrame {{
            border-radius: 12px;
            overflow: hidden;
        }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Data Loading (with Parquet auto-cache for speed)
# ─────────────────────────────────────────────
NEEDED_COLS = [
    'Order ID', 'Order Date', 'Ship Mode', 'Segment', 'Country',
    'Market', 'Region', 'Category', 'Sub-Category', 'Sales',
    'Quantity', 'Discount', 'Profit', 'Shipping Cost', 'Order Priority',
]

@st.cache_data(show_spinner="📦 Loading data — first load caches for speed…")
def load_data():
    """Load Global Superstore data. Auto-converts to Parquet on first run for 10-20x faster reloads."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    xlsx_path = os.path.join(base_dir, "Global_Superstore2.xlsx")
    parquet_path = os.path.join(base_dir, ".cache_superstore.parquet")

    # ── Fast path: read from cached Parquet ──
    if os.path.exists(parquet_path):
        xlsx_mtime = os.path.getmtime(xlsx_path) if os.path.exists(xlsx_path) else 0
        parquet_mtime = os.path.getmtime(parquet_path)
        if parquet_mtime >= xlsx_mtime:
            df = pd.read_parquet(parquet_path)
            return _preprocess(df)

    # ── Slow path: read from Excel, then cache ──
    if not os.path.exists(xlsx_path):
        st.error(
            f"❌ Data file not found: `{xlsx_path}`\n\n"
            "Please place `Global_Superstore2.xlsx` in the project directory."
        )
        st.stop()

    # Only read columns we need → faster Excel parse
    df = pd.read_excel(xlsx_path, engine='openpyxl', usecols=lambda c: c in NEEDED_COLS)

    # Parse dates before caching
    if df['Order Date'].dtype == 'object':
        for fmt in ['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
            try:
                df['Order Date'] = pd.to_datetime(df['Order Date'], format=fmt)
                break
            except ValueError:
                continue
        else:
            df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    else:
        df['Order Date'] = pd.to_datetime(df['Order Date'])

    # Save Parquet cache for next time
    try:
        df.to_parquet(parquet_path, index=False)
    except Exception:
        pass  # Non-critical — just means no cache speedup next time

    return _preprocess(df)


def _preprocess(df):
    """Add computed columns needed by all pages."""
    if 'Year' not in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Year'] = df['Order Date'].dt.year
        df['Quarter'] = 'Q' + df['Order Date'].dt.quarter.astype(str)
        df['Month'] = df['Order Date'].dt.month
        df['YearMonth'] = df['Order Date'].dt.to_period('M').astype(str)
        df['Profit_Margin'] = np.where(df['Sales'] != 0, df['Profit'] / df['Sales'], 0)
    return df


# ─────────────────────────────────────────────
# Helper: KPI Card HTML
# ─────────────────────────────────────────────
def kpi_card(label, value, delta=None, prefix="", suffix="", fmt=",.0f"):
    val_str = f"{prefix}{value:{fmt}}{suffix}"
    delta_html = ""
    if delta is not None:
        css_class = "positive" if delta >= 0 else "negative"
        arrow = "▲" if delta >= 0 else "▼"
        delta_html = f'<div class="kpi-delta {css_class}">{arrow} {abs(delta):.1f}%</div>'
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{val_str}</div>
        {delta_html}
    </div>
    """


def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def page_header(title, subtitle):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Helper: Plotly Layout
# ─────────────────────────────────────────────
def apply_layout(fig, theme, height=420, showlegend=True):
    t = THEMES[theme]
    fig.update_layout(
        template=t['plotly_template'],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color=t['text']),
        margin=dict(l=40, r=20, t=50, b=40),
        height=height,
        showlegend=showlegend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    return fig


# ─────────────────────────────────────────────
# Helper: calculate_kpi
# ─────────────────────────────────────────────
def calculate_kpi_table(df, group_cols):
    summary = (
        df.groupby(group_cols)
        .agg(
            Total_Sales=('Sales', 'sum'),
            Total_Profit=('Profit', 'sum'),
            Total_Qty=('Quantity', 'sum'),
            Avg_Discount=('Discount', 'mean'),
            Order_Count=('Order ID', 'nunique'),
        )
        .reset_index()
    )
    summary['Profit_Margin_%'] = (summary['Total_Profit'] / summary['Total_Sales']) * 100
    summary['Avg_Discount_%'] = summary['Avg_Discount'] * 100
    return summary


# ═════════════════════════════════════════════
# PAGE 1: Performance Overview
# ═════════════════════════════════════════════
def page_performance(df, theme):
    t = THEMES[theme]
    page_header("📈 Performance Overview", "Sales, Profit & Margin trends across years and quarters (2011 – 2014)")

    # ── KPI Cards ──
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    overall_margin = (total_profit / total_sales) * 100 if total_sales else 0
    total_orders = df['Order ID'].nunique()

    years_sorted = sorted(df['Year'].unique())
    delta_sales = delta_profit = delta_margin = None
    if len(years_sorted) >= 2:
        last, prev = years_sorted[-1], years_sorted[-2]
        s_last = df[df['Year'] == last]['Sales'].sum()
        s_prev = df[df['Year'] == prev]['Sales'].sum()
        p_last = df[df['Year'] == last]['Profit'].sum()
        p_prev = df[df['Year'] == prev]['Profit'].sum()
        m_last = (p_last / s_last * 100) if s_last else 0
        m_prev = (p_prev / s_prev * 100) if s_prev else 0
        delta_sales = ((s_last - s_prev) / s_prev * 100) if s_prev else 0
        delta_profit = ((p_last - p_prev) / p_prev * 100) if p_prev else 0
        delta_margin = m_last - m_prev

    cols = st.columns(4)
    with cols[0]:
        st.markdown(kpi_card("Total Sales", total_sales), unsafe_allow_html=True)
    with cols[1]:
        st.markdown(kpi_card("Total Profit", total_profit), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(kpi_card("Total Profit Margin", overall_margin, fmt=".2f"), unsafe_allow_html=True)
    with cols[3]:
        st.markdown(kpi_card("Total Orders", total_orders), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Yearly Summary ──
    yearly = (
        df.groupby('Year')
        .agg(Total_Sales=('Sales', 'sum'), Total_Profit=('Profit', 'sum'))
        .reset_index()
    )
    yearly['Profit_Margin'] = (yearly['Total_Profit'] / yearly['Total_Sales']) * 100
    yearly['Sales_YoY'] = yearly['Total_Sales'].pct_change() * 100
    yearly['Profit_YoY'] = yearly['Total_Profit'].pct_change() * 100

    section_title("📊 Yearly Performance")
    c1, c2, c3 = st.columns(3)

    with c1:
        fig = px.bar(yearly, x='Year', y='Total_Sales', text_auto=',.0f',
                     color_discrete_sequence=[t['accent']])
        fig.update_traces(textposition='outside', textfont_size=11)
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Total Sales by Year", xaxis_title="Year", yaxis_title="Sales ($)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(yearly, x='Year', y='Total_Profit', text_auto=',.0f',
                     color_discrete_sequence=[t['gradient_bar'][1]])
        fig.update_traces(textposition='outside', textfont_size=11)
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Total Profit by Year", xaxis_title="Year", yaxis_title="Profit ($)")
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        fig = px.bar(yearly, x='Year', y='Profit_Margin', text=yearly['Profit_Margin'].apply(lambda x: f"{x:.2f}%"),
                     color_discrete_sequence=[t['gradient_bar'][2]])
        fig.update_traces(textposition='outside', textfont_size=11)
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Profit Margin by Year", xaxis_title="Year", yaxis_title="Margin (%)")
        st.plotly_chart(fig, use_container_width=True)

    # ── YoY Growth ──
    yoy = yearly.dropna(subset=['Sales_YoY']).copy()
    yoy['Period'] = [f"{int(y)-1}–{int(y)}" for y in yoy['Year']]

    if not yoy.empty:
        section_title("📈 Year-on-Year Growth")
        c1, c2 = st.columns(2)

        with c1:
            colors = [t['positive'] if v >= 0 else t['negative'] for v in yoy['Sales_YoY']]
            fig = go.Figure(go.Bar(
                x=yoy['Period'], y=yoy['Sales_YoY'],
                text=[f"{v:+.1f}%" for v in yoy['Sales_YoY']],
                textposition='outside', marker_color=colors,
            ))
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            fig = apply_layout(fig, theme, showlegend=False)
            fig.update_layout(title="Sales YoY Growth (%)", xaxis_title="Period", yaxis_title="%")
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            colors = [t['positive'] if v >= 0 else t['negative'] for v in yoy['Profit_YoY']]
            fig = go.Figure(go.Bar(
                x=yoy['Period'], y=yoy['Profit_YoY'],
                text=[f"{v:+.1f}%" for v in yoy['Profit_YoY']],
                textposition='outside', marker_color=colors,
            ))
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            fig = apply_layout(fig, theme, showlegend=False)
            fig.update_layout(title="Profit YoY Growth (%)", xaxis_title="Period", yaxis_title="%")
            st.plotly_chart(fig, use_container_width=True)

    # ── Quarterly Trends ──
    section_title("📅 Quarterly Performance")

    quarterly = (
        df.groupby(['Year', 'Quarter'])
        .agg(Total_Sales=('Sales', 'sum'), Total_Profit=('Profit', 'sum'))
        .reset_index()
    )
    quarterly['Profit_Margin'] = (quarterly['Total_Profit'] / quarterly['Total_Sales']) * 100
    quarterly['Period'] = quarterly['Year'].astype(str) + " " + quarterly['Quarter']
    quarterly = quarterly.sort_values(['Year', 'Quarter'])

    tab_sales, tab_profit, tab_margin = st.tabs(["💰 Sales", "📊 Profit", "📐 Margin"])

    with tab_sales:
        fig = px.line(quarterly, x='Period', y='Total_Sales', markers=True,
                      color_discrete_sequence=[t['accent']])
        fig.update_traces(line_width=3, marker_size=8)
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Quarterly Sales Trend", xaxis_title="", yaxis_title="Sales ($)")
        st.plotly_chart(fig, use_container_width=True)

    with tab_profit:
        fig = px.bar(quarterly, x='Period', y='Total_Profit',
                     color=quarterly['Total_Profit'].apply(lambda x: 'Profit' if x >= 0 else 'Loss'),
                     color_discrete_map={'Profit': t['positive'], 'Loss': t['negative']})
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Quarterly Profit", xaxis_title="", yaxis_title="Profit ($)")
        st.plotly_chart(fig, use_container_width=True)

    with tab_margin:
        fig = px.line(quarterly, x='Period', y='Profit_Margin', markers=True,
                      color_discrete_sequence=[t['gradient_bar'][0]])
        fig.update_traces(line_width=2)
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Quarterly Profit Margin (%)", xaxis_title="", yaxis_title="Margin (%)")
        st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════
# PAGE 2: Geographic & Product Drilldown
# ═════════════════════════════════════════════
def page_geo_product(df, theme):
    t = THEMES[theme]
    page_header("🌍 Geographic & Product Drilldown", "Drill down by Market → Region → Country, and by Category → Sub-Category")

    # ── Premium Choropleth Map (Mapbox) ──
    section_title("🗺️ Profit by Country (Spatial Visualization)")

    geo_country = calculate_kpi_table(df, ['Country'])

    # Load GeoJSON for country boundaries
    geojson_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"

    @st.cache_data(show_spinner=False)
    def load_geojson(url):
        import json, urllib.request
        with urllib.request.urlopen(url) as resp:
            return json.loads(resp.read().decode())

    geojson = load_geojson(geojson_url)

    # Build a lookup: country name → feature id (using 'name' field)
    name_to_id = {}
    for feat in geojson['features']:
        props = feat.get('properties', {})
        name = props.get('name', '')
        name_to_id[name] = name
        feat['id'] = name

    # Alias mapping: dataset name → GeoJSON name (for mismatches)
    COUNTRY_ALIASES = {
        'United States': 'United States of America',
        'Czech Republic': 'Czechia',
        'Myanmar (Burma)': 'Myanmar',
        'Tanzania': 'United Republic of Tanzania',
        'Swaziland': 'Eswatini',
        'Macedonia': 'North Macedonia',
        "Cote d'Ivoire": "Côte d'Ivoire",
    }
    geo_country['geo_id'] = geo_country['Country'].map(
        lambda c: name_to_id.get(c, name_to_id.get(COUNTRY_ALIASES.get(c, ''), None))
    )
    geo_matched = geo_country.dropna(subset=['geo_id'])

    # Custom diverging color scale: dark red → pink → white → mint → green
    custom_colorscale = [
        [0.00, '#8B0000'],   # very high loss
        [0.45, '#EF4444'],   # loss
        [0.50, '#FACC15'],   # neutral / zero
        [0.55, '#22C55E'],   # profit
        [1.00, '#006400'],   # very high profit
    ]

    # Mapbox/Map style based on theme
    tile_style = 'carto-darkmatter' if 'Dark' in theme else 'carto-positron'

    # Common arguments for map-based choropleth
    map_kwargs = dict(
        geojson=geojson,
        locations='geo_id',
        color='Total_Profit',
        color_continuous_scale=custom_colorscale,
        color_continuous_midpoint=0,
        zoom=1.1,
        center={"lat": 20, "lon": 15},
        opacity=0.75,
        hover_name='Country',
        hover_data={
            'Total_Sales': ':$,.0f',
            'Total_Profit': ':$,.0f',
            'Profit_Margin_%': ':.2f',
            'geo_id': False,
            'Country': False,
        },
        labels={
            'Total_Profit': 'Profit ($)',
            'Total_Sales': 'Sales ($)',
            'Profit_Margin_%': 'Margin (%)',
        },
    )

    # Try Plotly 6+ API first, then 5.x, then basic fallback
    choropleth_fn = getattr(px, 'choropleth_map', None)
    style_key = 'map_style'
    if choropleth_fn is None:
        choropleth_fn = getattr(px, 'choropleth_mapbox', None)
        style_key = 'mapbox_style'

    if choropleth_fn is not None:
        map_kwargs[style_key] = tile_style
        fig = choropleth_fn(geo_matched, **map_kwargs)
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=550,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color=t['text']),
            coloraxis_colorbar=dict(
                title=dict(text="Profit ($)", font=dict(size=12)),
                thickness=14,
                len=0.55,
                bgcolor='rgba(0,0,0,0)',
                borderwidth=0,
                tickfont=dict(size=10),
                x=0.99,
            ),
        )
        fig.update_traces(
            marker_line_width=0.5,
            marker_line_color='rgba(255,255,255,0.3)' if 'Dark' in theme else 'rgba(0,0,0,0.1)',
        )
    else:
        # Fallback: enhanced px.choropleth (works on any Plotly version)
        fig = px.choropleth(
            geo_matched,
            geojson=geojson,
            locations='geo_id',
            color='Total_Profit',
            color_continuous_scale=custom_colorscale,
            color_continuous_midpoint=0,
            hover_name='Country',
            hover_data={
                'Total_Sales': ':$,.0f',
                'Total_Profit': ':$,.0f',
                'Profit_Margin_%': ':.2f',
                'geo_id': False,
                'Country': False,
            },
            labels={
                'Total_Profit': 'Profit ($)',
                'Total_Sales': 'Sales ($)',
                'Profit_Margin_%': 'Margin (%)',
            },
        )
        fig.update_geos(
            showcoastlines=True, coastlinecolor="rgba(0,0,0,0.15)",
            showland=True, landcolor="#F1F5F9" if 'Dark' not in theme else "#1E293B",
            showocean=True, oceancolor="#E0F2FE" if 'Dark' not in theme else "#0F172A",
            showframe=False,
            projection_type='natural earth',
            showcountries=True, countrycolor='rgba(0,0,0,0.08)',
        )
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=550,
            paper_bgcolor='rgba(0,0,0,0)',
            geo=dict(bgcolor='rgba(0,0,0,0)'),
            font=dict(family="Inter, sans-serif", color=t['text']),
            coloraxis_colorbar=dict(
                title=dict(text="Profit ($)", font=dict(size=12)),
                thickness=14,
                len=0.55,
                bgcolor='rgba(0,0,0,0)',
                borderwidth=0,
                tickfont=dict(size=10),
                x=0.99,
            ),
        )
        fig.update_traces(
            marker_line_width=0.5,
            marker_line_color='rgba(255,255,255,0.3)' if 'Dark' in theme else 'rgba(0,0,0,0.08)',
        )

    st.plotly_chart(fig, use_container_width=True)

    # ── Market & Region ──
    section_title("📊 Market & Region Analysis")
    c1, c2 = st.columns(2)

    geo_market = calculate_kpi_table(df, ['Market']).sort_values('Profit_Margin_%', ascending=True)
    geo_region = calculate_kpi_table(df, ['Market', 'Region']).sort_values('Total_Profit')

    with c1:
        fig = px.bar(geo_market, x='Profit_Margin_%', y='Market', orientation='h',
                     text=geo_market['Profit_Margin_%'].apply(lambda x: f"{x:.1f}%"),
                     color='Profit_Margin_%',
                     color_continuous_scale='RdYlGn', color_continuous_midpoint=geo_market['Profit_Margin_%'].median())
        fig.update_traces(textposition='outside')
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Profit Margin by Market", xaxis_title="Margin (%)", yaxis_title="",
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        bottom_regions = geo_region.head(10)
        colors_region = [t['negative'] if v < 0 else t['accent'] for v in bottom_regions['Total_Profit']]
        fig = go.Figure(go.Bar(
            y=bottom_regions['Region'], x=bottom_regions['Total_Profit'],
            orientation='h', marker_color=colors_region,
            text=[f"${v:,.0f}" for v in bottom_regions['Total_Profit']],
            textposition='outside',
        ))
        fig.add_vline(x=0, line_dash="dash", line_color="gray")
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Bottom 10 Regions by Profit", xaxis_title="Profit ($)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    # ── Loss-Making Countries ──
    loss_countries = geo_country[geo_country['Total_Profit'] < 0].sort_values('Total_Profit')

    if not loss_countries.empty:
        section_title("🚩 Loss-Making Countries")
        c1, c2 = st.columns(2)

        with c1:
            top_loss = loss_countries.head(10)
            fig = px.bar(top_loss, y='Country', x='Total_Profit', orientation='h',
                         text=top_loss['Total_Profit'].apply(lambda x: f"${x:,.0f}"),
                         color_discrete_sequence=[t['negative']])
            fig.update_traces(textposition='outside')
            fig = apply_layout(fig, theme, showlegend=False)
            fig.update_layout(title=f"Top 10 Loss-Making Countries ({len(loss_countries)} total)",
                              xaxis_title="Profit ($)", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            # Heatmap: Sub-Category vs Top 5 Loss Countries
            top5 = loss_countries.head(5)['Country'].tolist()
            pivot = df[df['Country'].isin(top5)].pivot_table(
                index='Sub-Category', columns='Country', values='Profit', aggfunc='sum', fill_value=0
            )
            fig = px.imshow(
                pivot, text_auto=',.0f', color_continuous_scale='RdBu', color_continuous_midpoint=0,
                aspect='auto',
                labels=dict(x="Country", y="Sub-Category", color="Profit ($)"),
            )
            fig = apply_layout(fig, theme, height=480, showlegend=False)
            fig.update_layout(title="Loss Concentration: Sub-Category vs Top 5 Loss Countries",
                              coloraxis_showscale=True)
            st.plotly_chart(fig, use_container_width=True)

    # ── Sub-Category Profit ──
    section_title("📦 Profit by Sub-Category")
    product_subcat = calculate_kpi_table(df, ['Category', 'Sub-Category']).sort_values('Total_Profit')

    colors_sc = [t['negative'] if v < 0 else t['positive'] for v in product_subcat['Total_Profit']]
    fig = go.Figure(go.Bar(
        y=product_subcat['Sub-Category'], x=product_subcat['Total_Profit'],
        orientation='h', marker_color=colors_sc,
        text=[f"${v:,.0f}" for v in product_subcat['Total_Profit']],
        textposition='outside',
    ))
    fig.add_vline(x=0, line_dash="dash", line_color="gray")
    fig = apply_layout(fig, theme, height=520, showlegend=False)
    fig.update_layout(title="Profit by Sub-Category (Red = Loss)", xaxis_title="Profit ($)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

    # ── Sub-Category Diagnosis ──
    section_title("🩺 Sub-Category Diagnosis")

    # Add Diagnosis column based on profitability metrics
    def diagnose(row):
        if row['Total_Profit'] < 0:
            return '🔴 Loss-Making'
        elif row['Avg_Discount_%'] > 15 and row['Profit_Margin_%'] < 10:
            return '🟠 High Discount Risk'
        elif row['Profit_Margin_%'] < 5:
            return '🟡 Low Margin'
        else:
            return '🟢 Healthy / Profitable'

    product_subcat['Diagnosis'] = product_subcat.apply(diagnose, axis=1)

    # Sort all sub-categories by profit (worst first)
    all_subcat = product_subcat.sort_values('Total_Profit')

    # Summary count per diagnosis (all types)
    diag_order = ['🔴 Loss-Making', '🟠 High Discount Risk', '🟡 Low Margin', '🟢 Healthy / Profitable']
    diag_counts = all_subcat['Diagnosis'].value_counts()
    summary_cols = st.columns(4)
    for i, diag in enumerate(diag_order):
        count = diag_counts.get(diag, 0)
        with summary_cols[i]:
            st.markdown(
                f'<div class="kpi-card"><div class="kpi-label">{diag}</div>'
                f'<div class="kpi-value">{count}</div>'
                f'<div class="kpi-delta">sub-categories</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Full table of ALL sub-categories with diagnosis
    cols_to_show = ['Category', 'Sub-Category', 'Total_Sales', 'Total_Qty',
                    'Total_Profit', 'Profit_Margin_%', 'Avg_Discount_%', 'Diagnosis']
    diag_display = all_subcat[cols_to_show].copy()
    diag_display.columns = ['Category', 'Sub-Category', 'Sales ($)', 'Quantity',
                            'Profit ($)', 'Margin (%)', 'Avg Discount (%)', 'Diagnosis']
    diag_display = diag_display.reset_index(drop=True)
    diag_display.index = diag_display.index + 1

    st.dataframe(
        diag_display.style
        .format({
            'Sales ($)': '${:,.0f}',
            'Profit ($)': '${:,.0f}',
            'Quantity': '{:,.0f}',
            'Margin (%)': '{:.2f}%',
            'Avg Discount (%)': '{:.1f}%',
        })
        .background_gradient(subset=['Profit ($)'], cmap='RdYlGn')
        .background_gradient(subset=['Margin (%)'], cmap='RdYlGn')
        .background_gradient(subset=['Avg Discount (%)'], cmap='OrRd'),
        use_container_width=True,
        height=600,
    )


# ═════════════════════════════════════════════
# PAGE 3: Root Cause Analysis
# ═════════════════════════════════════════════
def page_root_cause(df, theme):
    t = THEMES[theme]
    page_header("🔍 Investigating Analysis", "Investigating Discount, Shipping Cost, Ship Mode & Product Mix impacts")

    # ── Discount Impact ──
    section_title("💸 Discount Impact on Profitability")

    discount_bins = [-0.01, 0.0, 0.10, 0.20, 0.30, 0.40, 0.50, 1.0]
    discount_labels = ['0%', '1-10%', '11-20%', '21-30%', '31-40%', '41-50%', '>50%']

    df_disc = df.copy()
    df_disc['Discount_Band'] = pd.cut(df_disc['Discount'], bins=discount_bins, labels=discount_labels)

    disc_agg = df_disc.groupby('Discount_Band', observed=False).agg(
        Order_Count=('Sales', 'count'),
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Loss_Orders=('Profit', lambda x: (x < 0).sum()),
    ).reset_index()
    disc_agg['Profit_Margin_%'] = (disc_agg['Total_Profit'] / disc_agg['Total_Sales']) * 100
    disc_agg['Loss_Rate_%'] = (disc_agg['Loss_Orders'] / disc_agg['Order_Count']) * 100

    c1, c2 = st.columns(2)

    with c1:
        colors_disc = [t['negative'] if v < 0 else t['accent'] for v in disc_agg['Profit_Margin_%']]
        fig = go.Figure(go.Bar(
            x=disc_agg['Discount_Band'].astype(str),
            y=disc_agg['Profit_Margin_%'],
            marker_color=colors_disc,
            text=[f"{v:.1f}%" for v in disc_agg['Profit_Margin_%']],
            textposition='outside',
        ))
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Profit Margin by Discount Band (Tipping Point)",
                          xaxis_title="Discount Level", yaxis_title="Profit Margin (%)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = go.Figure(go.Bar(
            x=disc_agg['Discount_Band'].astype(str),
            y=disc_agg['Loss_Rate_%'],
            marker_color=t['gradient_bar'],
            text=[f"{v:.1f}%" for v in disc_agg['Loss_Rate_%']],
            textposition='outside',
        ))
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Loss Order Rate by Discount Band",
                          xaxis_title="Discount Level", yaxis_title="Loss Rate (%)")
        st.plotly_chart(fig, use_container_width=True)

    # ── Shipping Cost ──
    section_title("🚚 Shipping Cost Efficiency")

    market_ship = df.groupby('Market').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Total_Shipping=('Shipping Cost', 'sum'),
    ).reset_index()
    market_ship['Ship_to_Sales_%'] = (market_ship['Total_Shipping'] / market_ship['Total_Sales']) * 100
    market_ship['Profit_Margin_%'] = (market_ship['Total_Profit'] / market_ship['Total_Sales']) * 100
    market_ship = market_ship.sort_values('Ship_to_Sales_%', ascending=False)

    st.markdown("**📋 Shipping Cost Efficiency by Market (sorted by Shipping/Sales ratio)**")
    ship_table = market_ship[['Market', 'Total_Sales', 'Total_Profit', 'Total_Shipping',
                              'Ship_to_Sales_%', 'Profit_Margin_%']].copy()
    ship_table.columns = ['Market', 'Sales ($)', 'Profit ($)', 'Shipping Cost ($)',
                          'Ship/Sales (%)', 'Profit Margin (%)']
    ship_table = ship_table.sort_values('Ship/Sales (%)', ascending=False).reset_index(drop=True)
    ship_table.index = ship_table.index + 1  # 1-based ranking
    st.dataframe(
        ship_table.style
        .format({
            'Sales ($)': '${:,.0f}',
            'Profit ($)': '${:,.0f}',
            'Shipping Cost ($)': '${:,.0f}',
            'Ship/Sales (%)': '{:.2f}%',
            'Profit Margin (%)': '{:.2f}%',
        })
        .background_gradient(subset=['Ship/Sales (%)'], cmap='OrRd')
        .background_gradient(subset=['Profit Margin (%)'], cmap='RdYlGn'),
        use_container_width=True,
    )

    # ── Discount vs Profit Scatter ──
    section_title("📊 Discount vs Profit Distribution")

    sample = df.sample(min(5000, len(df)), random_state=42)
    fig = px.scatter(sample, x='Discount', y='Profit', color='Category',
                     opacity=0.5, color_discrete_sequence=px.colors.qualitative.Set2,
                     hover_data={'Sales': ':$,.0f', 'Sub-Category': True})
    fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=1)
    fig = apply_layout(fig, theme, height=480)
    fig.update_layout(title="Discount vs Profit (Order Level)",
                      xaxis_title="Discount Rate", yaxis_title="Profit ($)")
    st.plotly_chart(fig, use_container_width=True)

    # ── Diagnosis Table ──
    section_title("🔬 Sub-Category Diagnosis: Discount vs Margin")

    subcat = calculate_kpi_table(df, ['Category', 'Sub-Category'])
    subcat_table = subcat[['Category', 'Sub-Category', 'Total_Sales', 'Total_Profit',
                           'Avg_Discount_%', 'Profit_Margin_%', 'Order_Count']].copy()
    subcat_table.columns = ['Category', 'Sub-Category', 'Sales ($)', 'Profit ($)',
                            'Avg Discount (%)', 'Profit Margin (%)', 'Orders']
    subcat_table = subcat_table.sort_values('Sales ($)', ascending=False).reset_index(drop=True)
    subcat_table.index = subcat_table.index + 1  # 1-based ranking

    st.dataframe(
        subcat_table.style
        .format({
            'Sales ($)': '${:,.0f}',
            'Profit ($)': '${:,.0f}',
            'Avg Discount (%)': '{:.1f}%',
            'Profit Margin (%)': '{:.2f}%',
            'Orders': '{:,.0f}',
        })
        .background_gradient(subset=['Profit Margin (%)'], cmap='RdYlGn')
        .background_gradient(subset=['Sales ($)'], cmap='Blues')
        .background_gradient(subset=['Avg Discount (%)'], cmap='OrRd'),
        use_container_width=True,
        height=520,
    )


# ═════════════════════════════════════════════
# PAGE 4: Segment & Trouble Spots
# ═════════════════════════════════════════════
def page_segment(df, theme):
    t = THEMES[theme]
    page_header("🎯 Customer Segment Analysis", "Customer Segment analysis and pinpointing the biggest loss concentrations")

    # ── Segment Performance ──
    section_title("👥 Customer Segment Performance")

    seg = calculate_kpi_table(df, ['Segment']).sort_values('Total_Profit', ascending=False)

    c1, c2, c3 = st.columns(3)

    with c1:
        fig = px.bar(seg, x='Segment', y='Total_Sales', text_auto='$,.0f',
                     color='Segment', color_discrete_sequence=t['gradient_bar'])
        fig.update_traces(textposition='outside')
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Sales by Segment", xaxis_title="", yaxis_title="Sales ($)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(seg, x='Segment', y='Total_Profit', text_auto='$,.0f',
                     color='Segment', color_discrete_sequence=t['gradient_bar'])
        fig.update_traces(textposition='outside')
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Profit by Segment", xaxis_title="", yaxis_title="Profit ($)")
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        fig = px.bar(seg, x='Segment', y='Profit_Margin_%',
                     text=seg['Profit_Margin_%'].apply(lambda x: f"{x:.2f}%"),
                     color='Segment', color_discrete_sequence=t['gradient_bar'])
        fig.update_traces(textposition='outside')
        fig = apply_layout(fig, theme, showlegend=False)
        fig.update_layout(title="Profit Margin by Segment", xaxis_title="", yaxis_title="Margin (%)")
        st.plotly_chart(fig, use_container_width=True)

    # ── Segment × Market Heatmap ──
    section_title("🔥 Segment × Market Heatmap")

    seg_market = df.pivot_table(index='Segment', columns='Market', values='Profit', aggfunc='sum', fill_value=0)
    fig = px.imshow(seg_market, text_auto='$,.0f', color_continuous_scale='RdYlGn',
                    color_continuous_midpoint=0, aspect='auto',
                    labels=dict(x="Market", y="Segment", color="Profit ($)"))
    fig = apply_layout(fig, theme, height=350, showlegend=False)
    fig.update_layout(title="Profit Heatmap: Segment × Market")
    st.plotly_chart(fig, use_container_width=True)

    # ── Trouble Spots Treemap ──
    section_title("🌳 Trouble Spots Treemap")

    trouble = calculate_kpi_table(df, ['Market', 'Country', 'Category', 'Sub-Category'])
    trouble_loss = trouble[trouble['Total_Profit'] < 0].copy()
    trouble_loss['Abs_Loss'] = trouble_loss['Total_Profit'].abs()

    if not trouble_loss.empty:
        top_troubles = trouble_loss.nlargest(50, 'Abs_Loss')
        fig = px.treemap(
            top_troubles,
            path=['Market', 'Country', 'Category', 'Sub-Category'],
            values='Abs_Loss',
            color='Total_Profit',
            color_continuous_scale='Reds_r',
            hover_data={'Total_Sales': ':$,.0f', 'Total_Profit': ':$,.0f', 'Profit_Margin_%': ':.2f'},
            labels={'Abs_Loss': 'Loss ($)', 'Total_Profit': 'Profit ($)'},
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=40, b=10),
            height=520,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color=t['text']),
            title="Top 50 Loss-Making Combinations (Market → Country → Category → Sub-Category)",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No loss-making combinations found with the current filters.")

    # ── Top Trouble Spots Table ──
    section_title("📋 Top Trouble Spots (Interactive Table)")

    trouble_top = trouble.sort_values('Total_Profit').head(20)
    trouble_display = trouble_top[['Market', 'Country', 'Category', 'Sub-Category',
                                    'Total_Sales', 'Total_Profit', 'Profit_Margin_%', 'Avg_Discount_%']].copy()
    trouble_display.columns = ['Market', 'Country', 'Category', 'Sub-Category',
                                'Sales ($)', 'Profit ($)', 'Margin (%)', 'Avg Discount (%)']

    st.dataframe(
        trouble_display.style
        .format({
            'Sales ($)': '${:,.0f}',
            'Profit ($)': '${:,.0f}',
            'Margin (%)': '{:.2f}%',
            'Avg Discount (%)': '{:.1f}%',
        })
        .background_gradient(subset=['Profit ($)'], cmap='RdYlGn')
        .background_gradient(subset=['Margin (%)'], cmap='RdYlGn'),
        use_container_width=True,
        height=500,
    )


# ═════════════════════════════════════════════
# MAIN APP
# ═════════════════════════════════════════════
def main():
    # Load data
    df = load_data()

    # ── Sidebar ──
    with st.sidebar:
        st.markdown("## 📊 Global Superstore")
        st.markdown("---")

        # Theme picker
        theme = st.selectbox("🎨 Theme", list(THEMES.keys()), index=0)

        st.markdown("---")

        # Navigation
        page = st.radio(
            "📑 Navigation",
            [
                "📈 Performance Overview",
                "🌍 Product Analysis",
                "🔍 Margin Analysis",
                "🎯 Segment Analysis",
            ],
            index=0,
        )

        st.markdown("---")

        # Filters
        st.markdown("### 🔧 Filters")

        years = sorted(df['Year'].unique())
        year_range = st.select_slider(
            "📅 Year Range",
            options=years,
            value=(min(years), max(years)),
        )

        markets = st.multiselect(
            "🌐 Market",
            options=sorted(df['Market'].unique()),
            default=sorted(df['Market'].unique()),
        )

        categories = st.multiselect(
            "📦 Category",
            options=sorted(df['Category'].unique()),
            default=sorted(df['Category'].unique()),
        )

        segments = st.multiselect(
            "👥 Segment",
            options=sorted(df['Segment'].unique()),
            default=sorted(df['Segment'].unique()),
        )

        st.markdown("---")
        st.caption("MK6 — Week 3 Business Analytics")

    # Inject theme CSS
    inject_css(theme)

    # Apply filters
    df_filtered = df[
        (df['Year'].between(year_range[0], year_range[1]))
        & (df['Market'].isin(markets))
        & (df['Category'].isin(categories))
        & (df['Segment'].isin(segments))
    ].copy()

    if df_filtered.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your selections.")
        return

    # Route to page
    if "Performance" in page:
        page_performance(df_filtered, theme)
    elif "Product Analysis" in page:
        page_geo_product(df_filtered, theme)
    elif "Margin Analysis" in page:
        page_root_cause(df_filtered, theme)
    elif "Segment Analysis" in page:
        page_segment(df_filtered, theme)


if __name__ == "__main__":
    main()
