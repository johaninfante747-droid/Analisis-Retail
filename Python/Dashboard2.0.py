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

tab1, tab2 = st.tabs(["👥 Obj 1 y 2: Perfil Demográfico", "📈 Obj 3 y 4: Patrones de Compra"])

with tab1:
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("1. Estructura Demográfica")
        piramide_data = df.groupby(["Rango Edad", "Gender"]).size().reset_index(name="Cantidad")
        piramide_data.loc[piramide_data["Gender"] == "Male", "Cantidad"] *= -1
        fig_piramide = px.bar(
            piramide_data, y="Rango Edad", x="Cantidad", color="Gender", 
            orientation="h", barmode="relative",
            color_discrete_sequence=["#ef553b", "#636efa"]
        )
        st.plotly_chart(fig_piramide, use_container_width=True)
    with col_der:
        st.subheader("2. Correlación de Variables")
        cols_numericas = df[["Age", "Quantity", "Price per Unit", "Total Amount"]]
        matriz_corr = cols_numericas.corr()
        fig_corr = px.imshow(
            matriz_corr, text_auto=".2f", aspect="auto",
            color_continuous_scale="Blues",
            title="¿La edad influye en el monto gastado?"
        )
        st.plotly_chart(fig_corr, use_container_width=True)