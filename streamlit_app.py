
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Calculadora Martinez/Italiano", layout="centered")
st.image("logo.png", use_column_width=True)
st.title("CALCULADORA MARTINEZ/ITALIANO")

nombre = st.text_input("Nombre del caso")
haber_input = st.text_input("Ingrese el haber base", "53036,00")
try:
    haber_inicial = float(haber_input.replace(",", "."))
except ValueError:
    st.error("⚠ Ingresá el haber en formato numérico válido (ej: 53036.00 o 53036,00)")
    st.stop()

fecha_base = st.text_input("Fecha del haber base (YYYY-MM)", "2020-01")

df_anses = pd.read_csv("coef_anses.csv", sep=";")
df_justicia = pd.read_csv("coef_justicia.csv", sep=";")
df_anses["coef_anses"] = df_anses["coef_anses"].astype(str).str.replace(",", ".").astype(float)
df_justicia["coef_justicia"] = df_justicia["coef_justicia"].astype(str).str.replace(",", ".").astype(float)

df = pd.merge(df_anses, df_justicia, on="fecha")
df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m")

try:
    fecha_base_dt = datetime.strptime(fecha_base, "%Y-%m")

    marzo_dt = datetime.strptime("2020-03", "%Y-%m")
    if fecha_base_dt < marzo_dt:
        coef_marzo_2020 = 1.023 + (1500 / haber_inicial)
        nueva_fila = pd.DataFrame([{
            "fecha": marzo_dt,
            "coef_anses": coef_marzo_2020,
            "coef_justicia": coef_marzo_2020
        }])
        df = pd.concat([df, nueva_fila], ignore_index=True)
        df = df.sort_values("fecha")

    df_tramo = df[df["fecha"] > fecha_base_dt].copy()

    if not df_tramo.empty:
        factor_anses = df_tramo["coef_anses"].prod()
        factor_justicia = df_tramo["coef_justicia"].prod()

        haber_anses = haber_inicial * factor_anses
        haber_justicia = haber_inicial * factor_justicia
        diferencia = haber_justicia - haber_anses
        diferencia_pct = (diferencia / haber_anses * 100) if haber_anses != 0 else 0

        st.subheader("Resultados:")
        if nombre:
            st.write(f"**Caso:** {nombre}")
        st.write(f"**Haber actualizado según ANSeS:** ${haber_anses:,.2f}")
        st.write(f"**Haber actualizado según Justicia:** ${haber_justicia:,.2f}")
        st.write(f"**Diferencia:** ${diferencia:,.2f} ({diferencia_pct:.2f}%%)")
    else:
        st.warning("No hay coeficientes posteriores a la fecha ingresada.")
except ValueError:
    st.error("⚠ Ingresá la fecha en formato YYYY-MM (ejemplo: 2020-04)")
