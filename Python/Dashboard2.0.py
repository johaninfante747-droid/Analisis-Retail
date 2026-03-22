import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Análisis Retail 2023", layout="wide")

@st.cache_data
def cargar_datos():
    datos = pd.read_csv('Dataset.limpio/retail_limpio.csv')
    datos['Date'] = pd.to_datetime(datos['Date'])
    datos['Mes'] = datos['Date'].dt.month_name()
    limites = [0, 25, 35, 45, 55, 100]
    etiquetas = ['<25', '26-35', '36-45', '46-55', '56+']
    datos['Rango Edad'] = pd.cut(datos['Age'], bins=limites, labels=etiquetas)
    return datos

df = cargar_datos()

st.sidebar.title("Panel de Control")
st.sidebar.info("Este dashboard responde al problema central: asociación entre perfil demográfico y hábitos de consumo.")

st.sidebar.subheader("Autores:")
st.sidebar.write("- Johan Infante")
st.sidebar.write("- Eddie Palomino")
st.sidebar.write("- Juan Covarrubia")

st.title("Análisis de Consumo Retail 2023")

with st.container():
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Ventas Totales 2023", value=f"${df['Total Amount'].sum():,.2f}")
    with col2:
        st.metric(label="Edad Promedio", value=f"{df['Age'].mean():.0f} años")
    with col3:
        st.metric(label="Total de Transacciones", value=f"{len(df)}")
    st.write("---")
