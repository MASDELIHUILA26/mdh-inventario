"""
Dashboard de Política de Inventario - Más Delicias del Huila
Prototipo (Fase 1) — Punto de venta: Jardín Plaza, Diciembre 2024

Cómo correr localmente:
    pip install streamlit pandas plotly
    streamlit run app.py

Cómo publicarlo gratis (visible en celular vía navegador):
    1. Sube esta carpeta a un repo de GitHub
    2. Entra a https://share.streamlit.io con tu cuenta de GitHub
    3. Conecta el repo y selecciona app.py -> Deploy
    4. Obtienes un link tipo https://tuapp.streamlit.app que abre bien en cualquier celular
"""

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Inventario MDH",
    page_icon="📦",
    layout="centered",  # 'centered' se ve mejor en celular que 'wide'
    initial_sidebar_state="collapsed",
)

# ---------- Carga de datos ----------
@st.cache_data
def load_data():
    productos = pd.read_csv("data/politica_productos.csv", dtype={"cod_producto": str})
    materiales = pd.read_csv("data/politica_materiales.csv")
    demanda = pd.read_csv("data/demanda_diaria.csv", dtype={"cod_producto": str})
    match = pd.read_csv("data/match_articulos_bom.csv")
    return productos, materiales, demanda, match

productos, materiales, demanda, match = load_data()

# ---------- Encabezado ----------
st.title("📦 Política de Inventario")
st.caption("Más Delicias del Huila · Punto de venta: Jardín Plaza · Datos: Dic 2024 (piloto)")

st.info(
    "⚠️ **Prototipo con datos de ejemplo.** Usa solo los 32 productos que cruzaron con "
    "confianza contra el BOM (de 91 vendidos). El resto requiere completar la tabla de "
    "equivalencias código histórico → código BOM.",
    icon="⚠️",
)

# ---------- Parámetros (simples, pensados para celular) ----------
with st.expander("⚙️ Parámetros del cálculo"):
    nivel_servicio = st.select_slider(
        "Nivel de servicio objetivo",
        options=["90%", "95%", "97.5%", "99%"],
        value="95%",
    )
    st.caption(
        "Nivel de servicio = probabilidad de NO quedarse sin stock durante el "
        "tiempo de reposición. A mayor nivel, mayor stock de seguridad."
    )

# ---------- Tabs ----------
tab1, tab2, tab3 = st.tabs(["🥖 Productos", "🧂 Materiales/Insumos", "📊 Demanda"])

# ===== TAB 1: Productos terminados =====
with tab1:
    st.subheader("¿Qué productos reponer hoy?")
    prod_view = productos[[
        "match_name", "demanda_proyectada_manana", "stock_seguridad", "punto_reorden"
    ]].rename(columns={
        "match_name": "Producto",
        "demanda_proyectada_manana": "Demanda esperada/día",
        "stock_seguridad": "Stock seguridad",
        "punto_reorden": "Punto de reorden",
    }).sort_values("Punto de reorden", ascending=False)

    st.dataframe(prod_view, use_container_width=True, hide_index=True)

    st.caption(
        "**Punto de reorden:** si el inventario actual de un producto cae por debajo "
        "de este número, hay que reponer ya. Compáralo manualmente con el inventario "
        "del cierre de anoche (esto se automatiza en la Fase 2, leyendo SharePoint)."
    )

# ===== TAB 2: Materiales / Insumos =====
with tab2:
    st.subheader("¿Qué materias primas e insumos pedir?")
    cat_filter = st.multiselect(
        "Filtrar por categoría",
        options=sorted(materiales["categoria_material"].dropna().unique()),
        default=sorted(materiales["categoria_material"].dropna().unique()),
    )
    mat_view = materiales[materiales["categoria_material"].isin(cat_filter)][[
        "descripcion_material", "categoria_material", "proveedor1",
        "consumo_diario_material", "stock_seguridad", "punto_reorden"
    ]].rename(columns={
        "descripcion_material": "Material",
        "categoria_material": "Categoría",
        "proveedor1": "Proveedor",
        "consumo_diario_material": "Consumo/día",
        "stock_seguridad": "Stock seguridad",
        "punto_reorden": "Punto de reorden",
    }).sort_values("Punto de reorden", ascending=False)

    st.dataframe(mat_view, use_container_width=True, hide_index=True)

    st.caption(
        "Calculado explotando la demanda de productos terminados a través del BOM "
        "(receta de cada producto). Agrupa automáticamente el consumo de un mismo "
        "material entre varios productos."
    )

# ===== TAB 3: Demanda histórica =====
with tab3:
    st.subheader("Comportamiento de la demanda")
    producto_sel = st.selectbox(
        "Selecciona un producto",
        options=sorted(productos["match_name"].unique()),
    )
    cod_sel = productos.loc[productos["match_name"] == producto_sel, "cod_producto"].iloc[0]
    serie = demanda[demanda["cod_producto"] == cod_sel].sort_values("fecha")

    fig = px.bar(
        serie, x="fecha", y="unidades_vendidas",
        labels={"fecha": "Fecha", "unidades_vendidas": "Unidades vendidas"},
        title=f"Ventas diarias — {producto_sel}",
    )
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

    media = serie["unidades_vendidas"].mean()
    std = serie["unidades_vendidas"].std()
    col1, col2 = st.columns(2)
    col1.metric("Demanda promedio/día", f"{media:.1f}")
    col2.metric("Variabilidad (desv. estándar)", f"{std:.1f}")

st.divider()
st.caption(
    "Siguiente paso: conectar este cálculo a los archivos reales en SharePoint para que "
    "se actualice solo cada noche después del cierre, y completar la tabla de "
    "equivalencias de códigos para cubrir el 100% del catálogo."
)
