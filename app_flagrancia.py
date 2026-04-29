import streamlit as st
import json
from datetime import datetime, date

# =====================================================
# 1. SEGURIDAD Y CONFIGURACIÓN (BLOQUE 1 - BASE)
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
st.set_page_config(page_title="SVI - Santa Fe v5.5 (Esencia Recuperada)", layout="wide", page_icon="🚔")

# PERSISTENCIA TOTAL: Nada se borra al navegar
if "victimas" not in st.session_state: st.session_state.victimas = []
if "testigos" not in st.session_state: st.session_state.testigos = []
if "arrestados" not in st.session_state: st.session_state.arrestados = []
if "secuestros" not in st.session_state: st.session_state.secuestros = []
if "relato_base" not in st.session_state: st.session_state.relato_base = ""

# =====================================================
# 2. PANEL DE FUSIÓN (SIDEBAR) - SIN ERRORES
# =====================================================
with st.sidebar:
    st.header("📂 Consolidación SVI")
    st.caption("Operador: SubComisario Castañeda Juan")
    archivos = st.file_uploader("Subir datos del móvil", type=["json"], accept_multiple_files=True)
    if archivos:
        for a in archivos:
            try:
                d = json.load(a)
                if st.button(f"Fusionar {a.name}"):
                    st.session_state.victimas.extend(d.get("victimas", []))
                    st.session_state.testigos.extend(d.get("testigos", []))
                    st.session_state.arrestados.extend(d.get("arrestados", []))
                    st.session_state.secuestros.extend(d.get("secuestros", []))
                    st.success("✅ Datos sumados al acta")
                    st.rerun()
            except: st.error("Archivo no compatible")
    
    st.divider()
    if st.button("🗑️ Limpiar Todo"):
        for k in ["victimas", "testigos", "arrestados", "secuestros", "relato_base"]: st.session_state[k] = []
        st.rerun()

# =====================================================
# 3. CUERPO DEL PROGRAMA (ESTRUCTURA DE CARGA)
# =====================================================
st.title("🚔 SVI - Sistema de Identificación y Sumarios")
tabs = st.tabs(["1. Inicio (Operativo)", "2. Filiación (Legal)", "3. Inspección", "4. Secuestros", "5. Cierre e IA"])

# --- BLOQUE 1: LA ESENCIA ---
with tabs[0]:
    st.subheader("🛡️ Identificación del Procedimiento")
    c1, c2, c3, c4 = st.columns(4)
    acta_n = c1.text_input("Nro. de Acta", placeholder="Ej: 154/2026")
    incidencia = c2.text_input("Nro. Incidencia (911)")
    dep_lista = ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M.", "SUB 18", "OTRO"]
    dependencia = c3.selectbox("Dependencia", dep_lista)
    movil = c4.text_input("Nro. de Móvil")

    c5, c6 = st.columns(2)
    personal = c5.text_input("Personal Actuante", value="SubComisario Castañeda Juan")
    refuerzo = c6.text_input("Refuerzo (Móviles/Personal en apoyo)")

    c7, c8 = st.columns(2)
    fecha_acta = c7.date_input("Fecha", date.today())
    hora_acta = c8.time_input("Hora", datetime.now().time())

    c9, c10 = st.columns(2)
    lugar_hecho = c9.text_input("📍 Lugar del Hecho")
    lugar_aprehension = c10.text_input("👮 Lugar de Aprehensión (si difiere)")

    st.divider()
    st.session_state.relato_base = st.text_area("📝 Relato Circunstanciado (Cronología):", 
                                               value=st.session_state.relato_base, height=350)

# --- BLOQUE 2: FILIACIÓN DETALLADA ---
with tabs[1]:
    st.subheader("👤 Registro de Personas")
    if st.button("➕ Cargar Aprehendido"):
        st.session_state.arrestados.append({"apellido": "", "nombre": "", "dni": "", "hijo_de": "", "domicilio": ""})
    
    for i, a in enumerate(st.session_state.arrestados):
        with st.expander(f"APREHENDIDO: {a['apellido'].upper()}"):
            a["apellido"] = st.text_input("Apellido", a["apellido"], key=f"ap_{i}")
            a["nombre"] = st.text_input("Nombre", a["nombre"], key=f"nom_{i}")
            a["dni"] = st.text_input("DNI", a["dni"], key=f"dni_{i}")
            a["hijo_de"] = st.text_input("Hijo de (Padre/Madre)", a["hijo_de"], key=f"hijo_{i}")
            a["domicilio"] = st.text_input("Domicilio Real", a["domicilio"], key=f"dom_{i}")

# --- BLOQUE 4: SECUESTROS ---
with tabs[3]:
    st.subheader("📦 Detalle de Elementos Secuestrados")
    if st.button("➕ Añadir Elemento"):
        st.session_state.secuestros.append({"item": "", "serie": ""})
    for i, s in enumerate(st.session_state.secuestros):
        ca, cb = st.columns(2)
        s["item"] = ca.text_input("Descripción (Marca/Modelo/Color)", s["item"], key=f"s_i_{i}")
        s["serie"] = cb.text_input("N° Serie / Patente / IMEI", s["serie"], key=f"s_s_{i}")

# --- BLOQUE 5: VISTA FINAL E IA ---
with tabs[4]:
    st.subheader("⚖️ Cierre Judicial")
    fiscal = st.text_input("Fiscalía / Dr.")
    directivas = st.text_area("Directivas Impartidas")
    
    if st.button("🚀 PREPARAR PAQUETE PARA REDACCIÓN"):
        resumen = f"SUMARIO SVI - {dependencia}\nACTA N°: {acta_n} | 911: {incidencia}\n"
        resumen += f"MÓVIL: {movil} | ACTUANTE: {personal}\n"
        resumen += f"UBICACIÓN: {lugar_hecho}\nRELATO: {st.session_state.relato_base}"
        st.success("Paquete listo para copiar a la IA")
        st.code(resumen)
