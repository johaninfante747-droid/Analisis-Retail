import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Retail 2023", 
    layout="wide"
)

st.title("Análisis de Consumo Retail 2023")
st.subheader("Impacto Demográfico en Patrones de Compra")

st.write("""
Bienvenido al panel interactivo de análisis transaccional. 
Este dashboard responde a la pregunta central de nuestra investigación: 
**¿De qué manera influyen las características demográficas de los clientes en sus preferencias y volumen de gasto?**
""")