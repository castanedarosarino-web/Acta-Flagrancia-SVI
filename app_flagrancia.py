import streamlit as st
from datetime import datetime

# =====================================================
# 1. CONFIGURACIÓN Y ESTÉTICA (SVI PROFESIONAL)
# =====================================================
st.set_page_config(page_title="SVI - Acta de Procedimiento", layout="wide", page_icon="🚔")

# Corrección de la línea 23: Todo el CSS dentro del string triple
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
        "dependencia_otra": "", "movil": "", "refuerzo": "", 
        "l_hecho": "", "l_apre": "", "relato": "",
        "personal": "Sub Comisario CASTAÑEDA Juan"
    }

# =====================================================
# 3. SIDEBAR (CENTRAL DE RECEPCIÓN)
# =====================================================
with st.sidebar:
    st.title("📂 Central de Recepción")
    st.markdown("### **Creado por Sub Comisario CASTAÑEDA Juan**")
    
    st.divider()
    st.subheader("Importar JSON")
    st.file_uploader("Upload", type=["json"], help="200MB per file • JSON")
    
    st.divider()
    if st.button("💾 GUARDAR ACTA (JSON)"):
        st.toast("Guardando...")

# =====================================================
# 4. CUERPO PRINCIPAL - ESTRUCTURA DE ACTA
# =====================================================
st.title("🚔 ACTA DE PROCEDIMIENTO UR II _(S.I.V.)")
st.subheader("Creado por Sub Comisario CASTAÑEDA Juan")

tabs = st.tabs([
    "1. Inicio (Datos Base)", 
    "2. Arrestado", 
    "3. Victima", 
    "4. Testigo", 
    "5. Consulta", 
    "6. Inspección", 
    "7. Secuestros", 
    "8. Cierre"
])

with tabs[0]:
    st.subheader("🛡️ Identificación Administrativa y Operativa")
    
    c1, c2, c3, c4 = st.columns(4)
    n_acta = c1.text_input("Nro. de Acta", value=st.session_state.data_operativa["nro_acta"], placeholder="Ej: 154/26")
    n_incidencia = c2.text_input("Nro. Incidencia (911)", value=st.session_state.data_operativa["incidencia"], placeholder="Ej: 2026-00123")
    
    dep_opciones = ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M.", "OTRO"]
    dep = c3.selectbox("Dependencia", dep_opciones, index=0)
    
    if dep == "OTRO":
        dep_otra = c4.text_input("Especifique Dependencia", value=st.session_state.data_operativa["dependencia_otra"])
        n_movil = st.text_input("Nro. de Móvil", value=st.session_state.data_operativa["movil"], placeholder="Ej: 9845")
    else:
        n_movil = c4.text_input("Nro. de Móvil", value=st.session_state.data_operativa["movil"], placeholder="Ej: 9845")
        dep_otra = ""

    st.write("") 
    personal_actuante = st.text_input("Personal Actuante", value=st.session_state.data_operativa["personal"])
    refuerzos = st.text_input("Refuerzo (Móviles/Personal de apoyo)", value=st.session_state.data_operativa["refuerzo"])

    c5, c6 = st.columns(2)
    fecha_proc = c5.date_input("Fecha", value=datetime.now())
    hora_proc = c6.time_input("Hora", value=datetime.now())

    lugar_hecho = st.text_input("📍 Lugar del Hecho", value=st.session_state.data_operativa["l_hecho"], placeholder="Calle y Nro / Intersección")
    lugar_apre = st.text_input("👤 Lugar de Aprehensión", value=st.session_state.data_operativa["l_apre"], placeholder="Si difiere del lugar del hecho")

    st.divider()
    
    st.subheader("📝 Relato Circunstanciado")
    relato_usuario = st.text_area("Narración cronológica y detallada:", 
                                  value=st.session_state.data_operativa["relato"],
                                  placeholder="Escribí aquí los puntos clave del hecho...",
                                  height=200)

    prompt_ia = f"""Actuá como asistente de redacción policial de la Provincia de Santa Fe. Necesito ordenar este relato para un acta de procedimiento. No uses lenguaje de IA. No pongas título "Relato del hecho". Redactá en estilo policial, como texto corrido que pueda continuar luego de "SE HACE CONSTAR:". Empezá con "Que..." y mantené una redacción clara, formal y técnica. No inventes datos; utilizá únicamente lo siguiente: \n\n{relato_usuario}"""
    
    if st.button("📋 COPIAR PARA CHATGPT / GEMINI"):
        st.code(prompt_ia, language="text")
        st.success("Copiá el texto del recuadro gris y pegalo en el chat de la IA.")

    st.session_state.data_operativa.update({
        "nro_acta": n_acta, "incidencia": n_incidencia, "dependencia": dep,
        "dependencia_otra": dep_otra, "movil": n_movil, 
        "refuerzo": refuerzos, "l_hecho": lugar_hecho, 
        "l_apre": lugar_apre, "relato": relato_usuario, "personal": personal_actuante
    })

# Pestañas vacías listas para desarrollar
with tabs[1]: st.info("Módulo de Arrestado - En desarrollo")
with tabs[2]: st.info("Módulo de Victima - En desarrollo")
with tabs[3]: st.info("Módulo de Testigo - En desarrollo")
with tabs[4]: st.info("Módulo de Consulta - En desarrollo")
