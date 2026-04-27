import streamlit as st
import json
from datetime import datetime

# =========================================================
# BLOQUE 1: DATOS Y NARRATIVA POR AUDIO (EL CORAZÓN)
# =========================================================

# Título y Autoría (Para que no se pierda)
st.title("SISTEMA SVI - Original 10bis")
st.subheader("Creado por Sub Comisario Castañeda Juan")

with st.expander("📝 BLOQUE 1: DATOS Y NARRATIVA POR AUDIO", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        fecha_proc = st.date_input("Fecha del Hecho", datetime.now())
        unidad_interviniente = st.text_input("Dependencia", "COMANDO RADIOELÉCTRICO PÉREZ")
    with col2:
        hora_proc = st.time_input("Hora de Intervención", datetime.now())
        oficial_actuante = st.text_input("Oficial Actuante", "Sub Comisario Castañeda Juan")
    
    st.markdown("---")
    st.subheader("🎙️ Dictado del Acta")
    st.info("Presione el micrófono para relatar el procedimiento. El sistema transcribirá su voz.")
    
    # Este es el componente que captura el audio del oficial
    audio_file = st.audio_input("Grabar relato de flagrancia")
    
    if audio_file:
        st.success("Audio capturado correctamente.")
        # Aquí el oficial podrá ver y corregir lo que dictó
        narrativa = st.text_area(
            "Narrativa Transcripta (Editable)", 
            placeholder="En circunstancias que el móvil se encontraba patrullando...",
            height=250
        )
    else:
        narrativa = st.text_area(
            "Narrativa Manual (Si no usa dictado)", 
            placeholder="Escriba aquí si no puede usar el micrófono...",
            height=250
        )
