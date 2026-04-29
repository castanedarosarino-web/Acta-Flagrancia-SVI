import streamlit as st
import json
from datetime import datetime, date

# =====================================================
# 1. SEGURIDAD Y CONFIGURACIÓN
# =====================================================
TOKEN_ACCESO = "svi2026perez" 

def verificar_acceso():
    if st.query_params.get("token") == TOKEN_ACCESO:
        st.session_state.autenticado = True
    elif "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    if not st.session_state.autenticado:
        st.set_page_config(page_title="Acceso Restringido", page_icon="🚫")
        st.error("🚫 Acceso Restringido")
        st.stop()

verificar_acceso()
st.set_page_config(page_title="SVI - Santa Fe v5.0", layout="wide", page_icon="🚔")

# Inicialización de estados persistentes
if "victimas" not in st.session_state: st.session_state.victimas = []
if "testigos" not in st.session_state: st.session_state.testigos = []
if "arrestados" not in st.session_state: st.session_state.arrestados = []
if "secuestros" not in st.session_state: st.session_state.secuestros = []
if "relato_base" not in st.session_state: st.session_state.relato_base = ""
if "inspeccion_ocular" not in st.session_state: st.session_state.inspeccion_ocular = ""

# =====================================================
# 2. PANEL LATERAL (SIDEBAR)
# =====================================================
with st.sidebar:
    st.header("📂 Central de Recepción")
    st.caption("SubComisario Castañeda Juan")
    
    archivos = st.file_uploader("Importar JSON", type=["json"], accept_multiple_files=True)
    if archivos:
        for a in archivos:
            try:
                d = json.load(a)
                if st.button(f"Fusionar {a.name}"):
                    st.session_state.victimas.extend(d.get("victimas", []))
                    st.session_state.testigos.extend(d.get("testigos", []))
                    st.session_state.arrestados.extend(d.get("arrestados", []))
                    st.session_state.secuestros.extend(d.get("secuestros", []))
                    st.success("✅ Datos sumados")
                    st.rerun()
            except: st.error("Error en archivo")

    st.divider()
    st.download_button("💾 GUARDAR ACTA (JSON)", 
                       data=json.dumps({"victimas": st.session_state.victimas, "arrestados": st.session_state.arrestados}, indent=2),
                       file_name=f"SVI_ACTA_{date.today()}.json")

# =====================================================
# 3. BLOQUE 1: INICIO (RECONSTRUIDO AL 100%)
# =====================================================
st.title("🚔 SVI - Sistema de Gestión de Actas")
tabs = st.tabs(["1. Inicio (Datos Base)", "2. Filiación", "3. Inspección", "4. Secuestros", "5. Cierre"])

with tabs[0]:
    st.subheader("🛡️ Identificación Administrativa y Operativa")
    
    # Fila 1: Números y Dependencia
    c1, c2, c3, c4 = st.columns(4)
    acta_n = c1.text_input("Nro. de Acta", placeholder="Ej: 154/26")
    incidencia = c2.text_input("Nro. Incidencia (911)", placeholder="Ej: 2026-00123")
    dependencia = c3.selectbox("Dependencia", ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M.", "SUB 18", "OTRO"])
    movil = c4.text_input("Nro. de Móvil", placeholder="Ej: 9845")

    # Fila 2: Personal y Apoyo
    c5, c6 = st.columns(2)
    personal = c5.text_input("Personal Actuante", value="SubComisario Castañeda Juan")
    refuerzo = c6.text_input("Refuerzo (Móviles/Personal de apoyo)")

    # Fila 3: Tiempo
    c7, c8 = st.columns(2)
    fecha_acta = c7.date_input("Fecha", date.today())
    hora_acta = c8.time_input("Hora", datetime.now().time())

    # Fila 4: Ubicaciones
    c9, c10 = st.columns(2)
    lugar_hecho = c9.text_input("📍 Lugar del Hecho", placeholder="Calle y Nro / Intersección")
    lugar_aprehension = c10.text_input("👮 Lugar de Aprehensión", placeholder="Si difiere del lugar del hecho")

    st.divider()
    
    # Fila 5: Relato
    st.subheader("📝 Relato Circunstanciado")
    st.session_state.relato_base = st.text_area("Narración cronológica y detallada:", 
                                               value=st.session_state.relato_base, 
                                               height=400,
                                               placeholder="A la hora indicada, cumplimentando directivas de la Central 911...")

# --- RESTO DE LOS BLOQUES (FILIACIÓN, INSPECCIÓN, ETC) ---
with tabs[1]:
    st.info("Utilice el botón de la izquierda para sumar personas desde los móviles.")
    # (Aquí iría el formulario de filiación que ya tenemos)

with tabs[2]:
    st.session_state.inspeccion_ocular = st.text_area("Detalles de la Inspección Ocular:", value=st.session_state.inspeccion_ocular, height=300)
