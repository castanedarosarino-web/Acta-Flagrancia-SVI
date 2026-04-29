import streamlit as st
from datetime import datetime

# =====================================================
# 1. CONFIGURACIÓN DE INTERFAZ (SVI PROFESIONAL)
# =====================================================
st.set_page_config(page_title="Consolidación SVI", layout="wide", page_icon="🚔")

# CSS para estilización idéntica a la captura (minimalista y limpia)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextInput { margin-top: -15px; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# 2. PERSISTENCIA DE DATOS (PARA NO PERDER NADA)
# =====================================================
if "data_operativa" not in st.session_state:
    st.session_state.data_operativa = {
        "nro_acta": "", "incidencia": "", "dependencia": "CRE PÉREZ",
        "movil": "", "refuerzo": "", "l_hecho": "", "l_apre": ""
    }

# =====================================================
# 3. SIDEBAR (CONSOLIDACIÓN SVI)
# =====================================================
with st.sidebar:
    st.title("📂 Consolidación SVI")
    st.write(f"**Operador:** SubComisario Castañeda Juan")
    
    st.divider()
    st.subheader("Subir datos del móvil")
    st.file_uploader("Upload", type=["json"], help="Carga de datos SVI previos")
    
    st.divider()
    if st.button("🗑️ Limpiar Todo"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# =====================================================
# 4. CUERPO PRINCIPAL - BLOQUE 1 PERFECTO
# =====================================================
st.title("🚓 SVI - Sistema de Identificación y Sumarios")

# Pestañas respetando el diseño de la captura original
tabs = st.tabs(["1. Inicio (Operativo)", "2. Filiación (Legal)", "3. Inspección", "4. Secuestros", "5. Cierre e IA"])

with tabs[0]:
    st.subheader("🛡️ Identificación del Procedimiento")
    
    # FILA 1: Identificadores técnicos
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    n_acta = c1.text_input("Nro. de Acta", value=st.session_state.data_operativa["nro_acta"], placeholder="Ej: 154/2026")
    n_incidencia = c2.text_input("Nro. Incidencia (911)", value=st.session_state.data_operativa["incidencia"])
    dep = c3.selectbox("Dependencia", ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M."], index=0)
    n_movil = c4.text_input("Nro. de Móvil", value=st.session_state.data_operativa["movil"])

    # FILA 2: Personal y Apoyo
    st.write("") # Espaciador
    personal_fijo = st.text_input("Personal Actuante", value="SubComisario Castañeda Juan", disabled=True)
    refuerzos = st.text_input("Refuerzo (Móviles/Personal en apoyo)", value=st.session_state.data_operativa["refuerzo"])

    # FILA 3: Tiempo y Espacio (📍 Esencia del procedimiento)
    c5, c6 = st.columns(2)
    fecha_proc = c5.date_input("Fecha", value=datetime.now())
    hora_proc = c6.time_input("Hora", value=datetime.now())

    lugar_hecho = st.text_input("📍 Lugar del Hecho", value=st.session_state.data_operativa["l_hecho"])
    lugar_apre = st.text_input("👮 Lugar de Aprehensión", value=st.session_state.data_operativa["l_apre"])

    # Guardado automático en el estado de la sesión
    st.session_state.data_operativa.update({
        "nro_acta": n_acta, "incidencia": n_incidencia, "dependencia": dep,
        "movil": n_movil, "refuerzo": refuerzos, "l_hecho": lugar_hecho, "l_apre": lugar_apre
    })

# =====================================================
# CONTINUIDAD: LAS DEMÁS PESTAÑAS QUEDAN LISTAS PARA CARGAR
# =====================================================
with tabs[1]: st.info("Esperando directivas para Filiación (Legal)...")
with tabs[2]: st.info("Bloque de Inspección...")
with tabs[3]: st.info("Bloque de Secuestros...")
with tabs[4]: st.info("Generador de Cierre e IA...")
