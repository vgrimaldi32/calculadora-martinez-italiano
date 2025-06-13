import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# Logo
image = Image.open("logo_para_app.png")
st.image(image, use_column_width=True)

# Título
st.title("CALCULADORA MARTINEZ/ITALIANO")
st.subheader("Comparación de movilidad según ANSeS vs Justicia")

# Inputs
nombre = st.text_input("Nombre del caso")
haber_base = st.number_input("Ingrese el haber base", min_value=0.0, value=50000.00, step=100.0, format="%.2f")
fecha_base = st.text_input("Fecha del haber base (YYYY-MM)", value="2020-01")

# Validación de fecha
try:
    fecha_base_dt = pd.to_datetime(fecha_base, format="%Y-%m")
except ValueError:
    st.error("Ingresá la fecha en formato YYYY-MM (ejemplo: 2020-04)")
    st.stop()

# Carga de coeficientes
df_anses = pd.read_csv("movilidad_anses.csv", sep=";")
df_anses["Fecha"] = pd.to_datetime(df_anses["Fecha"], format="%Y-%m")
df_anses = df_anses[df_anses["Fecha"] > fecha_base_dt]

df_justicia = pd.read_csv("movilidad_martinez_italiano.csv", sep=";")
df_justicia["fecha"] = pd.to_datetime(df_justicia["Fecha"], format="%Y-%m", errors="coerce")
df_justicia = df_justicia[df_justicia["Fecha"] >= pd.to_datetime("2020-03")]  # Ajuste solicitado
df_justicia = df_justicia[df_justicia["Fecha"] > fecha_base_dt]

# Cálculos
haber_anses = haber_base * df_anses["Coeficiente anses"].prod()
haber_justicia = haber_base * df_justicia["Coeficiente justicia"].prod()

# Resultados
st.markdown("### Resultados:")
if nombre:
    st.markdown(f"**Caso:** {nombre}")

st.markdown(f"**Haber actualizado según ANSeS:** ${haber_anses:,.2f}")
st.markdown(f"**Haber actualizado según Justicia:** ${haber_justicia:,.2f}")

diferencia = haber_justicia - haber_anses
porcentaje = diferencia / haber_anses * 100 if haber_anses else 0
st.markdown(f"**Diferencia:** ${diferencia:,.2f} ({porcentaje:.2f}%)")
