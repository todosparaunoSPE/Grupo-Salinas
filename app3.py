# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 15:10:34 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="Dashboard Interactivo - Grupo Salinas",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar logo (asegúrate de tener salinas.png en tu directorio)
try:
    logo = Image.open('salinas.png')
except:
    logo = None

# ================ SIDEBAR DINÁMICO ================
with st.sidebar:
    if logo:
        st.image(logo, width=120)
    st.title("Filtros Interactivos")
    
    # Filtro de fechas dinámico
    fecha_inicio = st.date_input(
        "Fecha inicial",
        value=datetime(2023, 1, 1),
        min_value=datetime(2020, 1, 1),
        max_value=datetime(2023, 12, 31)
    )
    
    fecha_fin = st.date_input(
        "Fecha final",
        value=datetime(2023, 12, 31),
        min_value=datetime(2020, 1, 1),
        max_value=datetime(2023, 12, 31)
    )
    
    # Selector de empresas
    empresas = ["Elektra", "Banco Azteca", "Totalplay", "Seguros Azteca"]
    empresas_seleccionadas = st.multiselect(
        "Empresas del Grupo",
        options=empresas,
        default=empresas
    )
    
    # Selector de métrica
    metrica = st.selectbox(
        "Métrica principal",
        options=["Ventas", "Margen", "Clientes"],
        index=0
    )

# ================ GENERACIÓN DE DATOS DINÁMICOS ================
def generar_datos(fecha_inicio, fecha_fin, empresas):
    # Crear rango de fechas
    rango_fechas = pd.date_range(fecha_inicio, fecha_fin, freq='D')
    
    # Generar datos aleatorios pero consistentes
    np.random.seed(int(fecha_inicio.strftime("%Y%m%d")))  # Seed basada en fecha
    
    data = pd.DataFrame({
        "Fecha": np.random.choice(rango_fechas, 500),
        "Empresa": np.random.choice(empresas, 500),
        "Ventas": np.random.lognormal(mean=3, sigma=0.5, size=500).round(2) * 1000,
        "Margen": np.random.normal(loc=15, scale=5, size=500).clip(5, 30),
        "Clientes": np.random.poisson(lam=50, size=500)
    })
    
    return data

# Cargar datos (se regeneran automáticamente al cambiar filtros)
df = generar_datos(fecha_inicio, fecha_fin, empresas_seleccionadas)

# ================ KPIs DINÁMICOS ================
ventas_totales = df["Ventas"].sum()
margen_promedio = df["Margen"].mean()
clientes_unicos = df["Clientes"].sum()
tasa_crecimiento = ((ventas_totales / (ventas_totales * 0.8)) - 1) * 100  # Cálculo porcentual

# Formateo de valores para mostrar
ventas_formateadas = f"${ventas_totales/1e6:,.2f}M"
margen_formateado = f"{margen_promedio:.1f}%"
clientes_formateados = f"{clientes_unicos/1e3:,.1f}K"
crecimiento_formateado = f"{tasa_crecimiento:.1f}%"

# ================ INTERFAZ PRINCIPAL ================
# Header
col1, col2 = st.columns([1, 4])
with col1:
    if logo:
        st.image(logo, width=150)
with col2:
    st.title("DASHBOARD INTERACTIVO")
    st.markdown(f"""
    <style>
    .big-font {{
        font-size:22px !important;
        color: #2F5496;
    }}
    </style>
    <p class='big-font'><strong>Candidato:</strong> Javier Horacio Pérez Ricárdez | <strong>Cel:</strong> +52 56 1056 4095</p>
    <p>Última actualización: {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
    """, unsafe_allow_html=True)

# Sección de KPIs
st.markdown("---")
st.subheader("Indicadores Clave")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="Ventas Totales", value=ventas_formateadas)
with kpi2:
    st.metric(label="Margen Promedio", value=margen_formateado)
with kpi3:
    st.metric(label="Clientes Atendidos", value=clientes_formateados)
with kpi4:
    st.metric(label="Tasa de Crecimiento", value=crecimiento_formateado)

# ================ VISUALIZACIONES ================
st.markdown("---")
st.subheader("Análisis Visual")

# Gráfico 1: Serie temporal de la métrica seleccionada
fig1 = px.line(
    df.groupby(['Fecha', 'Empresa'])[metrica].mean().reset_index(),
    x="Fecha",
    y=metrica,
    color="Empresa",
    title=f"Evolución de {metrica} por Empresa",
    height=400
)
fig1.update_layout(hovermode="x unified")
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Distribución por empresa
col1, col2 = st.columns(2)
with col1:
    fig2 = px.bar(
        df.groupby('Empresa')[metrica].sum().reset_index(),
        x="Empresa",
        y=metrica,
        title=f"Total de {metrica} por Empresa",
        color="Empresa"
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    fig3 = px.pie(
        df.groupby('Empresa')[metrica].sum().reset_index(),
        names="Empresa",
        values=metrica,
        title=f"Distribución de {metrica}",
        hole=0.3
    )
    st.plotly_chart(fig3, use_container_width=True)

# Tabla de datos resumidos
st.markdown("---")
st.subheader("Datos Detallados")
df_resumen = df.groupby('Empresa').agg({
    'Ventas': ['sum', 'mean'],
    'Margen': ['mean', 'std'],
    'Clientes': ['sum']
}).round(2)
st.dataframe(df_resumen.style.format({
    ('Ventas', 'sum'): '${:,.2f}',
    ('Ventas', 'mean'): '${:,.2f}',
    ('Margen', 'mean'): '{:.2f}%',
    ('Margen', 'std'): '{:.2f}'
}))

# ================ ANÁLISIS ADICIONAL ================
st.markdown("---")
st.subheader("Análisis Adicional")

# Selector de tipo de análisis
analisis = st.selectbox(
    "Seleccione un tipo de análisis",
    options=["Correlación entre métricas", "Distribución de valores", "Tendencia mensual"],
    index=0
)

if analisis == "Correlación entre métricas":
    fig = px.scatter_matrix(
        df,
        dimensions=["Ventas", "Margen", "Clientes"],
        color="Empresa",
        title="Correlación entre Métricas"
    )
    st.plotly_chart(fig, use_container_width=True)
elif analisis == "Distribución de valores":
    fig = px.histogram(
        df,
        x=metrica,
        color="Empresa",
        marginal="box",
        title=f"Distribución de {metrica}",
        nbins=30
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    df_mensual = df.copy()
    df_mensual['Mes'] = df_mensual['Fecha'].dt.to_period('M').astype(str)
    fig = px.line(
        df_mensual.groupby(['Mes', 'Empresa'])[metrica].mean().reset_index(),
        x="Mes",
        y=metrica,
        color="Empresa",
        title=f"Tendencia Mensual de {metrica}"
    )
    st.plotly_chart(fig, use_container_width=True)

# ================ FOOTER ================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p>Dashboard desarrollado para Grupo Salinas - Todos los derechos reservados</p>
    <p>© 2025 Powered by Python</p>
</div>
""", unsafe_allow_html=True)