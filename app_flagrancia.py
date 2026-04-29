import streamlit as st
import json
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
    st.subheader("📥 Cargar Trabajo de Calle")
    archivo_subido = st.file_uploader("Subir archivo JSON", type=["json"])
    
    # LÓGICA DE CARGA MEJORADA
    if archivo_subido is not None:
        try:
            datos_nuevos = json.load(archivo_subido)
            # Actualizamos el estado
            st.session_state.data_operativa.update(datos_nuevos)
            st.success("✅ Datos cargados.")
            # FORZAMOS RECARGA para que los datos aparezcan en los campos
            st.rerun() 
        except Exception as e:
            st.error(f"Error al cargar: {e}")

    st.divider()
    
    # LÓGICA DE DESCARGA
    data_json = json.dumps(st.session_state.data_operativa, indent=4)
    st.download_button(
        label="💾 GUARDAR ACTA (JSON)",
        data=data_json,
        file_name=f"acta_{st.session_state.data_operativa.get('nro_acta', 'SVI')}.json",
        mime="application/json",
        use_container_width=True
    )

# =====================================================
# 4. CUERPO PRINCIPAL - BLOQUE 1
# =====================================================
st.title("🚔 ACTA DE PROCEDIMIENTO UR II _(S.I.V.)")
st.subheader("Creado por Sub Comisario CASTAÑEDA Juan")

tabs = st.tabs(["1. Inicio (Datos Base)", "2. Arrestado", "3. Victima", "4. Testigo", "5. Consulta", "6. Inspección", "7. Secuestros", "8. Cierre"])

with tabs[0]:
    st.subheader("🛡️ Identificación Administrativa y Operativa")
    
    c1, c2, c3, c4 = st.columns(4)
    n_acta = c1.text_input("Nro. de Acta", value=st.session_state.data_operativa["nro_acta"])
    n_incidencia = c2.text_input("Nro. Incidencia (911)", value=st.session_state.data_operativa["incidencia"])
    
    # Lógica para pre-seleccionar la dependencia cargada
    dep_actual = st.session_state.data_operativa.get("dependencia", "CRE PÉREZ")
    dep_opciones = ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M.", "OTRO"]
    # Buscamos el indice para que no de error si no existe
    idx_dep = dep_opciones.index(dep_actual) if dep_actual in dep_opciones else 0
    
    dep = c3.selectbox("Dependencia", dep_opciones, index=idx_dep)
    
    if dep == "OTRO":
        dep_otra = c4.text_input("Especifique Dependencia", value=st.session_state.data_operativa.get("dependencia_otra", ""))
        n_movil = st.text_input("Nro. de Móvil", value=st.session_state.data_operativa.get("movil", ""))
    else:
        n_movil = c4.text_input("Nro. de Móvil", value=st.session_state.data_operativa.get("movil", ""))
        dep_otra = ""

    personal_actuante = st.text_input("Personal Actuante", value=st.session_state.data_operativa.get("personal", "Sub Comisario CASTAÑEDA Juan"))
    refuerzos = st.text_input("Refuerzo (Móviles/Personal de apoyo)", value=st.session_state.data_operativa.get("refuerzo", ""))

    st.divider()
    st.subheader("📝 Relato Circunstanciado")
    # El valor ahora se toma directamente del session_state actualizado por la carga
    relato_usuario = st.text_area("Narración de los hechos:", 
                                  value=st.session_state.data_operativa.get("relato", ""), 
                                  height=200)

    # El botón de copiado ya incluye el prompt
    prompt_ia = f"""Actuá como asistente de redacción policial de la Provincia de Santa Fe. Necesito ordenar este relato para un acta de procedimiento. 
REGLA CRÍTICA DE COHERENCIA: Mantené la narración en PRIMERA PERSONA DEL PLURAL (Nosotros). 
Empezá con "Que..." y mantené una redacción clara y formal. \n\n{relato_usuario}"""

    if st.button("🚀 COPIAR Y LISTO PARA PEGAR EN IA"):
        st.components.v1.html(f"<script>navigator.clipboard.writeText(`{prompt_ia}`);</script>", height=0)
        st.success("✅ ¡Copiado! Pegalo en el chat de la IA.")

    # Sincronizamos cualquier cambio manual que se haga en pantalla
    st.session_state.data_operativa.update({
        "nro_acta": n_acta, "incidencia": n_incidencia, "dependencia": dep,
        "dependencia_otra": dep_otra, "movil": n_movil, "relato": relato_usuario, 
        "personal": personal_actuante, "refuerzo": refuerzos
    })
