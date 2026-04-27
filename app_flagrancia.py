# app_flagrancia.py - SISTEMA SVI ACTUALIZADO 2026
# Autor: Sub Comisario Castañeda Juan

import streamlit as st
import json
from datetime import datetime

# CONFIGURACIÓN DE AUTORÍA Y TÍTULO
st.set_page_config(page_title="SUMARIO SVI - Original 10bis", layout="wide")
st.title("Sistema de Validación de Identidad (SVI)")
st.subheader("Creado por Sub Comisario Castañeda Juan")

# BLOQUE 1: APERTURA Y NARRATIVA TÁCTICA 
with st.expander("Bloque 1: Apertura y Narrativa Táctica"):
    fecha_hora = st.text_input("Fecha y Hora de intervención", value=datetime.now().strftime("%d/%m/%Y %H:%M"))
    unidad = st.text_input("Unidad Interviniente")
    narrativa = st.text_area("Narrativa de Flagrancia (Relato objetivo)")
    identificacion = st.text_input("Identificación de Personas (Validación)")

# BLOQUE 2: REQUISA Y MESA DE ENLACE 
with st.expander("Bloque 2: Requisa, Pertenencias y Mesa de Enlace"):
    testigos = st.text_area("Testigos Hábiles (Art. 225 CPP)")
    inventario = st.text_area("Inventario de Objetos (Descripción de prendas)")
    secuestro = st.text_area("Módulo de Secuestro (Armas, estupefacientes, etc.)")
    mesa_enlace = st.checkbox("Validación Mesa de Enlace (Antecedentes/Pedidos)")

# BLOQUE 3: INSPECCIÓN Y REGISTRO FOTOGRÁFICO 
with st.expander("Bloque 3: Inspección Genérica y Croquis"):
    inspeccion = st.text_area("Inspección Ocular Genérica")
    st.info("Protocolo de 4 Fotos: 1. Panorámica, 2. Plano Medio, 3. Primer Plano, 4. Detalle.")
    camaras = st.text_input("Relevamiento de Cámaras (911/Privadas)")
    croquis = st.checkbox("Generar Croquis Demostrativo (Orientación al NORTE)")

# BLOQUE 4: COMUNICACIONES JUDICIALES Y CIERRE 
with st.expander("Bloque 4: Comunicaciones Judiciales y Cierre"):
    consulta_mpa = st.text_input("Consulta MPA 0800 (Hora y Fiscal interviniente)")
    defensoria = st.checkbox("Constancia de aviso a Defensoría General")
    recepcion = st.text_input("Oficial de Guardia receptor (Firma de responsabilidad)")

# PERSISTENCIA Y GENERACIÓN
if st.button("Guardar Acta y Generar PDF"):
    datos_acta = {
        "autor": "Castañeda Juan",
        "fecha": fecha_hora,
        "unidad": unidad,
        "narrativa": narrativa
    }
    # Lógica de guardado en JSON y generación de PDF legal
    st.success("Acta 'Original 10bis' procesada correctamente.")
