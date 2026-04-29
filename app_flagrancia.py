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
    if st.button("💾 GUARDAR ACTA (JSON)"):
        st.toast("Guardando...")

# =====================================================
# 4. CUERPO PRINCIPAL - ESTRUCTURA DE ACTA
# =====================================================
st.title("🚔 ACTA DE PROCEDIMIENTO UR II _(S.I.V.)")
st.subheader("Creado por Sub Comisario CASTAÑEDA Juan")

tabs = st.tabs(["1. Inicio (Datos Base)", "2. Arrestado", "3. Victima", "4. Testigo", "5. Consulta", "6. Inspección", "7. Secuestros", "8. Cierre"])

with tabs[0]:
    st.subheader("🛡️ Identificación Administrativa y Operativa")
    
    c1, c2, c3, c4 = st.columns(4)
    n_acta = c1.text_input("Nro. de Acta", value=st.session_state.data_operativa["nro_acta"])
    n_incidencia = c2.text_input("Nro. Incidencia (911)", value=st.session_state.data_operativa["incidencia"])
    
    dep_opciones = ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M.", "OTRO"]
    dep = c3.selectbox("Dependencia", dep_opciones)
    
    if dep == "OTRO":
        dep_otra = c4.text_input("Especifique Dependencia")
        n_movil = st.text_input("Nro. de Móvil", value=st.session_state.data_operativa["movil"])
    else:
        n_movil = c4.text_input("Nro. de Móvil", value=st.session_state.data_operativa["movil"])
        dep_otra = ""

    personal_actuante = st.text_input("Personal Actuante", value=st.session_state.data_operativa["personal"])
    refuerzos = st.text_input("Refuerzo (Móviles/Personal de apoyo)", value=st.session_state.data_operativa["refuerzo"])

    st.divider()
    st.subheader("📝 Relato Circunstanciado")
    relato_usuario = st.text_area("Narración de los hechos:", value=st.session_state.data_operativa["relato"], height=200)

    # LÓGICA DE COPIADO AUTOMÁTICO AL PORTAPAPELES
    prompt_ia = f"Actuá como asistente de redacción policial de la Provincia de Santa Fe. Necesito ordenar este relato para un acta de procedimiento. No uses lenguaje de IA. No pongas título 'Relato del hecho'. Redactá en estilo policial, como texto corrido que pueda continuar luego de 'SE HACE CONSTAR:'. Empezá con 'Que...' y mantené una redacción clara, formal y técnica. No inventes datos; utilizá únicamente lo siguiente: \\n\\n{relato_usuario}"

    # Botón invisible/JavaScript para copiar al portapapeles
    if st.button("🚀 COPIAR Y LISTO PARA PEGAR EN IA"):
        # Usamos st.components para inyectar el copiado directo
        st.components.v1.html(f"""
            <script>
            navigator.clipboard.writeText(`{prompt_ia}`);
            </script>
            """, height=0)
        st.success("✅ ¡Copiado! Ahora andá a ChatGPT/Gemini y apretá Ctrl+V (Pegar).")

    # Guardado de estado
    st.session_state.data_operativa.update({
        "nro_acta": n_acta, "incidencia": n_incidencia, "dependencia": dep,
        "dependencia_otra": dep_otra, "movil": n_movil, "relato": relato_usuario, "personal": personal_actuante
    })
