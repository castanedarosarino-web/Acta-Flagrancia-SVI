import streamlit as st
import json
from datetime import datetime, date

# =====================================================
# 1. PROTOCOLO DE SEGURIDAD Y ESTADO (LA BASE)
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
st.set_page_config(page_title="SVI - Esencia Policial v6.0", layout="wide", page_icon="🚔")

# INICIALIZACIÓN DE MEMORIA (No se rompe, no se olvida)
if "victimas" not in st.session_state: st.session_state.victimas = []
if "testigos" not in st.session_state: st.session_state.testigos = []
if "arrestados" not in st.session_state: st.session_state.arrestados = []
if "secuestros" not in st.session_state: st.session_state.secuestros = []
if "relato_base" not in st.session_state: st.session_state.relato_base = ""

# =====================================================
# 2. PANEL DE CONSOLIDACIÓN (SIDEBAR)
# =====================================================
with st.sidebar:
    st.header("📂 Consolidación de Datos")
    st.caption("SubComisario Castañeda Juan")
    
    archivos = st.file_uploader("Recibir JSON de Móviles", type=["json"], accept_multiple_files=True)
    if archivos:
        for a in archivos:
            try:
                d = json.load(a)
                if st.button(f"Fusionar {a.name}"):
                    st.session_state.victimas.extend(d.get("victimas", []))
                    st.session_state.arrestados.extend(d.get("arrestados", []))
                    st.session_state.secuestros.extend(d.get("secuestros", []))
                    st.success(f"✅ {a.name} Integrado")
                    st.rerun()
            except: st.error("Error en formato")

    st.divider()
    if st.button("🗑️ Limpiar Acta Actual"):
        for k in ["victimas", "testigos", "arrestados", "secuestros", "relato_base"]: st.session_state[k] = []
        st.rerun()

# =====================================================
# 3. ESTRUCTURA DE CARGA INMEJORABLE (BLOQUES)
# =====================================================
st.title("🚔 SVI - Sistema de Validación de Identidad")
tabs = st.tabs(["1. Inicio Operativo", "2. Filiación y Datos Legales", "3. Inspección y Secuestros", "4. Cierre Judicial"])

# --- BLOQUE 1: LA IDENTIDAD DEL ACTA ---
with tabs[0]:
    st.subheader("🛡️ Identificación Administrativa")
    c1, c2, c3, c4 = st.columns(4)
    acta_n = c1.text_input("Nro. de Acta", placeholder="Ej: 001/26")
    incidencia = c2.text_input("Nro. Incidencia (911)")
    dep_lista = ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M.", "SUB 18", "OTRO"]
    dependencia = c3.selectbox("Dependencia", dep_lista)
    movil = c4.text_input("Nro. de Móvil")

    c5, c6 = st.columns(2)
    personal = c5.text_input("Personal Actuante", value="SubComisario Castañeda Juan")
    refuerzo = c6.text_input("Móviles de Apoyo / Refuerzos")

    c7, c8 = st.columns(2)
    fecha_acta = c7.date_input("Fecha", date.today())
    hora_acta = c8.time_input("Hora", datetime.now().time())

    c9, c10 = st.columns(2)
    lugar_hecho = c9.text_input("📍 Lugar del Hecho")
    lugar_aprehension = c10.text_input("👮 Lugar de Aprehensión")

    st.divider()
    st.subheader("📝 Noticia Criminal (Relato)")
    st.session_state.relato_base = st.text_area("Narración detallada:", value=st.session_state.relato_base, height=350)

# --- BLOQUE 2: FILIACIÓN (LA ESENCIA LEGAL) ---
with tabs[1]:
    st.subheader("👤 Registro de Personas (Filiación Completa)")
    if st.button("➕ Agregar Aprehendido"):
        st.session_state.arrestados.append({"apellido": "", "nombre": "", "dni": "", "hijo_de": "", "domicilio": ""})
    
    for i, a in enumerate(st.session_state.arrestados):
        with st.expander(f"Aprehendido: {a['apellido'].upper()}"):
            a["apellido"] = st.text_input("Apellido", a["apellido"], key=f"ap_{i}")
            a["nombre"] = st.text_input("Nombre", a["nombre"], key=f"nom_{i}")
            a["dni"] = st.text_input("DNI", a["dni"], key=f"dni_{i}")
            a["hijo_de"] = st.text_input("Hijo de (Padre/Madre)", a["hijo_de"], key=f"hijo_{i}")
            a["domicilio"] = st.text_input("Domicilio Real", a["domicilio"], key=f"dom_{i}")

# --- BLOQUE 3: INSPECCIÓN Y SECUESTROS ---
with tabs[2]:
    st.subheader("📸 Diligencias Técnicas")
    st.text_area("Inspección Ocular:", height=200)
    st.divider()
    st.subheader("📦 Secuestros")
    if st.button("➕ Nuevo Elemento"):
        st.session_state.secuestros.append({"item": "", "serie": ""})
    for i, s in enumerate(st.session_state.secuestros):
        ca, cb = st.columns(2)
        s["item"] = ca.text_input("Elemento", s["item"], key=f"item_{i}")
        s["serie"] = cb.text_input("Serie/IMEI/Patente", s["serie"], key=f"serie_{i}")

# --- BLOQUE 4: CIERRE ---
with tabs[3]:
    st.subheader("⚖️ Consulta con el Magistrado")
    fiscal = st.text_input("Fiscal en Turno")
    directivas = st.text_area("Directivas Impartidas")
    
    if st.button("🚀 FINALIZAR Y COPIAR"):
        paquete = f"AUTOR: {personal}\nCUP: {acta_n}\n911: {incidencia}\nMÓVIL: {movil}\n"
        paquete += f"HECHO: {st.session_state.relato_base}\n"
        paquete += f"APREHENDIDOS: {len(st.session_state.arrestados)}\n"
        st.code(paquete)
