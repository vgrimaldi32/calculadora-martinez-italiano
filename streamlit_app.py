
import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Calculadora Martinez/Italiano", layout="centered")

# Logo
image = Image.open("logo para app.png")
st.image(image, use_container_width=True)

# Título
st.title("CALCULADORA MARTINEZ/ITALIANO")
st.subheader("Comparación de movilidad según ANSeS vs Justicia")

# Inputs
caso = st.text_input("Nombre del caso")
haber_base = st.number_input("Ingrese el haber base", value=50000.00, step=100.0, format="%.2f")
fecha_str = st.text_input("Fecha del haber base (YYYY-MM)", value="2020-01")

try:
    fecha_base = pd.to_datetime(fecha_str, format="%Y-%m")

    # Cargar coeficientes
    df_anses = pd.read_csv("movilidad anses.csv", sep=",")
    df_justicia = pd.read_csv("movilidad martinez italiano.csv", sep=",")

    df_anses["fecha"] = pd.to_datetime(df_anses["fecha"], format="%Y-%m")
    df_justicia["fecha"] = pd.to_datetime(df_justicia["fecha"], format="%Y-%m")

    # Calcular coeficientes acumulados
    coef_anses = df_anses[df_anses["fecha"] >= fecha_base]["coeficiente_anses"].prod()
    coef_justicia = df_justicia[df_justicia["fecha"] >= fecha_base]["coef_justicia"].prod()

    # Calcular haberes actualizados
    haber_anses = haber_base * coef_anses
    haber_justicia = haber_base * coef_justicia

    diferencia = haber_justicia - haber_anses
    porcentaje_dif = (diferencia / haber_anses) * 100 if haber_anses else 0

    st.markdown("### Resultados:")
    if caso:
        st.markdown(f"**Caso:** {caso}")

    st.markdown(f"**Haber actualizado según ANSeS:** ${haber_anses:,.2f}")
    st.markdown(f"**Haber actualizado según Justicia:** ${haber_justicia:,.2f}")
    st.markdown(f"**Diferencia:** ${diferencia:,.2f} ({porcentaje_dif:.2f}%)")

except Exception as e:
    st.error(f"Ocurrió un error: {e}")
