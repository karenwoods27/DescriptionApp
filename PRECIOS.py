import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Histórico de Precios de Cierre (Close) - Primer y Último día bursátil del año")

# Entrada del ticker
ticker_input = st.text_input("Escribe el ticker (ej. AGUA.MX, AC.MX, AAPL):", value="AGUA.MX")

# Años a consultar
anios = list(range(2020, 2025))

def obtener_cierres(ticker):
    # Descargar datos desde 2020 hasta inicios de 2025
    data = yf.download(ticker, start="2020-01-01", end="2025-01-10")
    
    if data.empty:
        return pd.DataFrame()

    data["Año"] = data.index.year
    resultados = []

    for anio in anios:
        datos_anio = data[data["Año"] == anio]
        if not datos_anio.empty:
            # Extraer el primer y último día disponible del año y sus precios de cierre
            primer_dia = datos_anio.index[0]
            ultimo_dia = datos_anio.index[-1]

            resultados.append({
                "Año": anio,
                "Tipo de Día": "Primer día disponible",
                "Fecha": primer_dia.strftime('%Y-%m-%d'),
                "Precio de Cierre (Close)": datos_anio.loc[primer_dia, "Close"]
            })

            resultados.append({
                "Año": anio,
                "Tipo de Día": "Último día disponible",
                "Fecha": ultimo_dia.strftime('%Y-%m-%d'),
                "Precio de Cierre (Close)": datos_anio.loc[ultimo_dia, "Close"]
            })

    return pd.DataFrame(resultados)

if ticker_input:
    try:
        df_resultado = obtener_cierres(ticker_input)

        if df_resultado.empty:
            st.warning("No se encontraron datos para el ticker ingresado.")
        else:
            # Mostrar resultados
            st.dataframe(df_resultado)

            # Descarga CSV
            csv = df_resultado.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name=f"{ticker_input}_cierres_2020_2024.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

