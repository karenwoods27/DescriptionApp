import streamlit as st
import yfinance as yf
import pandas as pd
from google import genai
import plotly.graph_objects as go
from datetime import datetime, timedelta

tokenGenAI = "AIzaSyAIcKJ8_n3oybahm13Zv-Gjo1hnPxDAvrk"

client = genai.Client(api_key=tokenGenAI)

# Configuración de la página
st.set_page_config(page_title="Riesgo-Retorno Empresa", layout="centered")

# Título principal
st.title("Calculadora de Riesgo-Retorno de una Acción")

# Input para ingresar el símbolo de la acción
symbol = st.text_input("Ingresa el símbolo de la acción (Ej: AAPL, TSLA, MSFT)", "", help="Introduce el ticker de la empresa y presiona buscar.")

# Botón de búsqueda
if st.button("Buscar"):
    if symbol:
        try:
            # Obtener información de la empresa
            company = yf.Ticker(symbol)
            info = company.info
            
            
            # Extraer datos relevantes
            company_name = info.get("longName", "Nombre no disponible").upper()
            description = info.get("longBusinessSummary", "Descripción no disponible")
            logo_url = info.get("logo_url", "")
            
            # Mostrar nombre de la empresa
            st.subheader(company_name)

            # Prompt
            prompt =  "Traduce el siguiente texto en español:" + description
            response = client.models.generate_content(model= "gemini-2.0-flash", contents =prompt )

            # Mostrar descripción 
            st.write(response.text)

            
            # Mostrar logo si está disponible
            if logo_url:
                st.image(logo_url, width=200)
            
            # Botón para copiar la descripción
            st.button("Copiar descripción", key="copy")


            #### Gráfica de precios historicos 
            st.markdown("### 📈 Precios históricos (últimos 5 años)")

            end_date = datetime.today()
            start_date = end_date - timedelta(days=5*365)

            hist = company.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

            if not hist.empty:
                fig = go.Figure()

                # Línea de precios de cierre
                fig.add_trace(go.Scatter(
                    x=hist.index,
                    y=hist["Close"],
                    mode="lines",
                    name="Precio de cierre"
                ))

                fig.update_layout(
                    title=f"Histórico de precios de {symbol.upper()}",
                    xaxis_title="Fecha",
                    yaxis_title="Precio (USD)",
                    template="plotly_white",
                    height=500
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No se encontraron datos históricos para graficar.")
            #############
        except Exception as e:
            st.error("No se pudo obtener información. Verifica el símbolo e intenta nuevamente.")
    else:
        st.warning("Por favor, ingresa un símbolo de acción válido.")

