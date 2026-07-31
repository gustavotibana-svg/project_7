import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Dashboard de Vehículos", page_icon="🚗", layout="wide")

# Caché para cargar los datos más rápido y optimizar el rendimiento
@st.cache_data
def load_data():
    car_data = pd.read_csv('vehicles_us.csv')
    return car_data

car_data = load_data()

# Encabezado principal y descripción
st.title("🚗 Explorador de Datos de Vehículos Usados")
st.header("Análisis Interactivo del Inventario")
st.write("Utiliza las opciones a continuación para generar gráficos dinámicos y explorar las relaciones en los datos del inventario de vehículos.")

# Diseño en columnas para una apariencia más moderna
col1, col2 = st.columns(2)

with col1:
    # Casilla de verificación para el histograma
    build_histogram = st.checkbox("📊 Construir un histograma del odómetro")

with col2:
    # Casilla de verificación para el gráfico de dispersión
    build_scatter = st.checkbox("📈 Construir diagrama de dispersión (Precio vs. Odómetro)")

# Lógica del Histograma
if build_histogram:
    st.write("Generando un **histograma interactivo** que muestra la distribución del kilometraje (odómetro) según la condición del vehículo...")
    
    # Gráfico moderno con gráfico marginal (caja) superior para ver outliers
    fig_hist = px.histogram(
        car_data, 
        x="odometer", 
        color="condition",
        marginal="box", 
        title="Distribución del Odómetro agrupado por Condición",
        labels={"odometer": "Odómetro (Millas)", "condition": "Condición"},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Mejorando el diseño del gráfico
    fig_hist.update_layout(bargap=0.1, template="plotly_white")
    st.plotly_chart(fig_hist, use_container_width=True)

# Lógica del Gráfico de Dispersión
if build_scatter:
    st.write("Generando un **gráfico de dispersión** para analizar cómo afecta el kilometraje al precio, segmentado por el tipo de vehículo...")
    
    # Gráfico de dispersión moderno con opacidad para evitar superposición visual (overplotting)
    fig_scatter = px.scatter(
        car_data, 
        x="odometer", 
        y="price", 
        color="type",
        opacity=0.6,
        title="Relación entre Precio y Odómetro por Tipo de Vehículo",
        labels={"odometer": "Odómetro (Millas)", "price": "Precio ($)", "type": "Tipo"},
        hover_data=["model", "model_year"] # Muestra datos adicionales al pasar el ratón
    )
    
    # Restringiendo ligeramente el eje Y para una mejor visualización de los datos típicos si hay valores extremos
    fig_scatter.update_layout(template="plotly_white")
    fig_scatter.update_yaxes(range=[0, 100000]) # Opcional: enfocar la vista en vehículos de hasta 100k
    
    st.plotly_chart(fig_scatter, use_container_width=True)

# Sección extra moderna: Métricas rápidas
st.divider()
st.header("Métricas Clave del Inventario")
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric(label="Total de Vehículos", value=f"{len(car_data):,}")
metric_col2.metric(label="Precio Promedio", value=f"${car_data['price'].mean():,.2f}")
metric_col3.metric(label="Odómetro Promedio", value=f"{car_data['odometer'].mean():,.0f} mi")