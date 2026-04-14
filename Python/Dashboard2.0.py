import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Análisis Retail 2023", layout="wide")

@st.cache_data
def cargar_datos():
    datos = pd.read_csv("Python/retail_limpio.csv")
    datos["Date"] = pd.to_datetime(datos["Date"])
    datos["Mes"] = datos["Date"].dt.month_name()
    
    limites = [0, 25, 35, 45, 55, 100]
    etiquetas = ["<25", "26-35", "36-45", "46-55", "56+"]
    datos["Rango Edad"] = pd.cut(datos["Age"], bins=limites, labels=etiquetas)
    return datos

df_completo = cargar_datos()

st.sidebar.title("Panel de Control")
st.sidebar.info("Este dashboard responde al problema central: asociación entre perfil demográfico y hábitos de consumo.")

st.sidebar.subheader("Autores:")
st.sidebar.write("- Johan Infante")
st.sidebar.write("- Eddie Palomino")
st.sidebar.write("- Juan Covarrubia")

st.sidebar.write("---")
st.sidebar.subheader("Filtros por Edades y Categorias")
categorias_disponibles = df_completo["Product Category"].unique().tolist()
categoria_sel = st.sidebar.multiselect(
    "Filtrar por Categoría:", 
    options=categorias_disponibles,
    default=categorias_disponibles
)
edad_min = int(df_completo["Age"].min())
edad_max = int(df_completo["Age"].max())
rango_edad = st.sidebar.slider(
    "Rango de Edad:", 
    min_value=edad_min, 
    max_value=edad_max, 
    value=(edad_min, edad_max)
)

df = df_completo[
    (df_completo["Product Category"].isin(categoria_sel)) & 
    (df_completo["Age"] >= rango_edad[0]) & 
    (df_completo["Age"] <= rango_edad[1])
]

st.title("Análisis de Consumo Retail 2023")

with st.container():
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        ventas_totales = df["Total Amount"].sum()
        st.metric(label="Ventas Totales 2023", value=f"${ventas_totales:,.2f}")
    with col2:
        edad_promedio = df["Age"].mean()
        st.metric(label="Edad Promedio", value=f"{edad_promedio:.0f} años")
    with col3:
        total_tx = len(df)
        st.metric(label="Total de Transacciones", value=f"{total_tx}")
    st.write("---")

tab1, tab2 = st.tabs(["Obj 1 y 2: Perfil Demográfico", "Obj 3 y 4: Patrones de Compra"])

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
        if len(cols_numericas) > 1:
            matriz_corr = cols_numericas.corr()
            fig_corr = px.imshow(
                matriz_corr, text_auto=".2f", aspect="auto",
                color_continuous_scale="Blues",
                title="¿La edad influye en el monto gastado?"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.warning("No hay suficientes datos en este rango para calcular la correlación.")

with tab2:
    col_izq2, col_der2 = st.columns(2)
    
    with col_izq2:
        st.subheader("3. Estacionalidad Mensual")
        ventas_mensuales = df.groupby(df["Date"].dt.month)["Total Amount"].sum().reset_index()
        
        fig_lineas = px.line(
            ventas_mensuales, x="Date", y="Total Amount", markers=True,
            labels={"Date": "Mes (1-12)", "Total Amount": "Ingresos ($)"}
        )
        st.plotly_chart(fig_lineas, use_container_width=True)

    with col_der2:
        st.subheader("4. Preferencias por Edad")
        pref_edad = df.groupby(["Rango Edad", "Product Category"]).size().reset_index(name="Transacciones")
        
        fig_pref = px.bar(
            pref_edad, x="Rango Edad", y="Transacciones", color="Product Category", 
            barmode="stack", title="Categorías más compradas según edad"
        )
        st.plotly_chart(fig_pref, use_container_width=True)

st.write("---")
with st.expander("Base de datos limpia"):
    st.write("Datos transaccionales filtrados y procesados:")
    st.dataframe(df)