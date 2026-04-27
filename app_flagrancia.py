import streamlit as st
import json
from datetime import datetime

# =========================================================
# ACTA DE PROCEDIMIENTO
# Autor: Sub Comisario Castañeda Juan
# =========================================================

# Configuración de página y Título Reglamentario
st.set_page_config(page_title="Acta de Procedimiento", layout="wide")
st.markdown("<h1 style='text-align: center;'>ACTA DE PROCEDIMIENTO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Creado por Sub Comisario Castañeda Juan</h3>", unsafe_allow_html=True)

# BLOQUE 1: DATOS Y NARRATIVA POR AUDIO
with st.container():
    st.subheader("📝 Bloque 1: Datos Generales")
    col1, col2 = st.columns(2)
    with col1:
        fecha_proc = st.date_input("Fecha", datetime.now())
        unidad_interviniente = st.text_input("Dependencia", "COMANDO RADIOELÉCTRICO PÉREZ")
    with col2:
        hora_proc = st.time_input("Hora de Inicio", datetime.now())
        oficial_actuante = st.text_input("Oficial Actuante", "Sub Comisario Castañeda Juan")
    
    st.markdown("---")
    st.subheader("🎙️ Narrativa del Hecho")
    st.info("Utilice el micrófono para dictar el relato de flagrancia. El sistema convertirá su voz en texto para el acta.")
    
    # Componente de entrada de audio para el personal de calle
    audio_file = st.audio_input("Grabar relato")
    
    if audio_file:
        st.success("Audio capturado. El texto aparecerá a continuación para su revisión:")
        narrativa = st.text_area(
            "Cuerpo del Acta (Editable)", 
            placeholder="Relate aquí los pormenores del procedimiento...",
            height=300
        )
    else:
        narrativa = st.text_area(
            "Cuerpo del Acta (Escritura Manual)", 
            placeholder="En circunstancias que el móvil policial se encontraba patrullando...",
            height=300
        )

st.caption("Documento generado bajo protocolo profesional - Autoría: Sub Comisario Castañeda Juan")
