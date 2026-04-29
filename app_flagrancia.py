import streamlit as st
from datetime import datetime

# =====================================================
# 1. CONFIGURACIÓN Y ESTÉTICA (SVI PROFESIONAL)
# =====================================================
st.set_page_config(page_title="SVI - Acta de Procedimiento", layout="wide", page_icon="🚔")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextInput { margin-top: -15px; }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# 2. PERSISTENCIA DE DATOS
# =====================================================
if "data_operativa" not in st.session_state:
    st.session_state.data_operativa = {
        "nro_acta": "", "incidencia": "", "dependencia": "CRE PÉREZ",
        "movil": "", "refuerzo": "", "l_hecho": "", "l_apre": "", "relato": ""
    }

# =====================================================
# 3. SIDEBAR (CENTRAL DE RECEPCIÓN)
# =====================================================
with st.sidebar:
    st.title("📂 Central de Recepción")
    # DIRECTIVA: AUTORÍA EN SIDEBAR
    st.write("**Creado por Sub Comisario CASTAÑEDA Juan**")
    
    st.divider()
    st.subheader("Importar JSON")
    st.file_uploader("Upload", type=["json"], help="200MB per file • JSON")
    
    st.divider()
    if st.button("💾 GUARDAR ACTA (JSON)"):
        st.toast("Guardando acta...")

# =====================================================
# 4. CUERPO PRINCIPAL - BLOQUE 1
# =====================================================
# DIRECTIVA: CAMBIO DE TÍTULO Y AUTORÍA DEBAJO
st.title("🚓 ACTA DE PROCEDIMIENTO UR II _(S.I.V.)")
st.subheader("Creado por Sub Comisario CASTAÑEDA Juan")

tabs = st.tabs(["1. Inicio (Datos Base)", "2. Filiación", "3. Inspección", "4. Secuestros", "5. Cierre"])

with tabs[0]:
    st.subheader("🛡️ Identificación Administrativa y Operativa")
    
    # FILA 1
    c1, c2, c3, c4 = st.columns(4)
    n_acta = c1.text_input("Nro. de Acta", value=st.session_state.data_operativa["nro_acta"], placeholder="Ej: 154/26")
    n_incidencia = c2.text_input("Nro. Incidencia (911)", value=st.session_state.data_operativa["incidencia"], placeholder="Ej: 2026-00123")
    dep = c3.selectbox("Dependencia", ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M."], index=0)
    n_movil = c4.text_input("Nro. de Móvil", value=st.session_state.data_operativa["movil"], placeholder="Ej: 9845")

    # FILA 2
    st.write("") 
    personal_actuante = st.text_input("Personal Actuante", value="Sub Comisario CASTAÑEDA Juan", disabled=True)
    refuerzos = st.text_input("Refuerzo (Móviles/Personal de apoyo)", value=st.session_state.data_operativa["refuerzo"])

    # FILA 3: TIEMPO
    c5, c6 = st.columns(2)
    fecha_proc = c5.date_input("Fecha", value=datetime.now())
    hora_proc = c6.time_input("Hora", value=datetime.now())

    # FILA 4: ESPACIO
    lugar_hecho = st.text_input("📍 Lugar del Hecho", value=st.session_state.data_operativa["l_hecho"], placeholder="Calle y Nro / Intersección")
    lugar_apre = st.text_input("👤 Lugar de Aprehensión", value=st.session_state.data_operativa["l_apre"], placeholder="Si difiere del lugar del hecho")

    st.divider()
    
    # RELATO CIRCUNSTANCIADO
    st.subheader("📝 Relato Circunstanciado")
    relato = st.text_area("Narración cronológica y detallada:", 
                          value=st.session_state.data_operativa["relato"],
                          placeholder="A la hora indicada, cumplimentando directivas de la Central 911...",
                          height=200)

    # Actualización del estado
    st.session_state.data_operativa.update({
        "nro_acta": n_acta, "incidencia": n_incidencia, "dependencia": dep,
        "movil": n_movil, "refuerzo": refuerzos, "l_hecho": lugar_hecho, 
        "l_apre": lugar_apre, "relato": relato
    })
