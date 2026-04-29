import streamlit as st
import json
from datetime import datetime, date

# =====================================================
# 1. SEGURIDAD Y CONFIGURACIÓN (BLOQUE 1)
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
st.set_page_config(page_title="SVI - Santa Fe v5.1", layout="wide", page_icon="🚔")

# Inicialización de estados para que no se borre nada al cambiar de pestaña
if "victimas" not in st.session_state: st.session_state.victimas = []
if "testigos" not in st.session_state: st.session_state.testigos = []
if "arrestados" not in st.session_state: st.session_state.arrestados = []
if "secuestros" not in st.session_state: st.session_state.secuestros = []
if "relato_base" not in st.session_state: st.session_state.relato_base = ""
if "inspeccion_ocular" not in st.session_state: st.session_state.inspeccion_ocular = ""
if "fiscal_turno" not in st.session_state: st.session_state.fiscal_turno = ""
if "directivas_fiscal" not in st.session_state: st.session_state.directivas_fiscal = ""

# =====================================================
# 2. PANEL LATERAL (IMPORTACIÓN Y GUARDADO)
# =====================================================
with st.sidebar:
    st.header("📂 Gestión de Archivos")
    st.caption("SubComisario Castañeda Juan")
    
    archivos = st.file_uploader("Importar datos de móviles", type=["json"], accept_multiple_files=True)
    if archivos:
        for a in archivos:
            try:
                d = json.load(a)
                if st.button(f"Fusionar {a.name}"):
                    st.session_state.victimas.extend(d.get("victimas", []))
                    st.session_state.testigos.extend(d.get("testigos", []))
                    st.session_state.arrestados.extend(d.get("arrestados", []))
                    st.session_state.secuestros.extend(d.get("secuestros", []))
                    st.success("✅ Datos integrados")
                    st.rerun()
            except: st.error("Error en archivo")

    st.divider()
    
    # Datos para el respaldo total
    respaldo = {
        "victimas": st.session_state.victimas,
        "testigos": st.session_state.testigos,
        "arrestados": st.session_state.arrestados,
        "secuestros": st.session_state.secuestros,
        "relato": st.session_state.relato_base
    }
    st.download_button("💾 DESCARGAR TODO (JSON)", 
                       data=json.dumps(respaldo, indent=2),
                       file_name=f"SVI_RESPALDO_{date.today()}.json")

# =====================================================
# 3. INTERFAZ POR BLOQUES (TABS)
# =====================================================
st.title("🚔 SVI - Sistema de Gestión de Actas")
tabs = st.tabs(["1. Inicio", "2. Filiación", "3. Inspección", "4. Secuestros", "5. Cierre e IA"])

# --- BLOQUE 1: DATOS OPERATIVOS ---
with tabs[0]:
    st.subheader("🛡️ Identificación Administrativa")
    c1, c2, c3, c4 = st.columns(4)
    acta_n = c1.text_input("Nro. de Acta", placeholder="Ej: 154/26")
    incidencia = c2.text_input("Nro. Incidencia (911)")
    dep_lista = ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M.", "SUB 18", "OTRO"]
    dependencia = c3.selectbox("Dependencia", dep_lista)
    movil = c4.text_input("Nro. de Móvil")

    c5, c6 = st.columns(2)
    personal = c5.text_input("Personal Actuante", value="SubComisario Castañeda Juan")
    refuerzo = c6.text_input("Refuerzo (Móviles de apoyo)")

    c7, c8 = st.columns(2)
    fecha_acta = c7.date_input("Fecha", date.today())
    hora_acta = c8.time_input("Hora", datetime.now().time())

    c9, c10 = st.columns(2)
    lugar_hecho = c9.text_input("📍 Lugar del Hecho")
    lugar_aprehension = c10.text_input("👮 Lugar de Aprehensión")

    st.divider()
    st.session_state.relato_base = st.text_area("📝 Relato Circunstanciado:", value=st.session_state.relato_base, height=350)

# --- BLOQUE 2: FILIACIÓN (PERSONAS) ---
def form_p(tipo, lista):
    st.subheader(f"👤 {tipo}")
    if st.button(f"➕ Añadir {tipo}", key=f"btn_{tipo}"):
        lista.append({"apellido": "", "nombre": "", "dni": "", "hijo_de": "", "domicilio": ""})
    for i, p in enumerate(lista):
        with st.expander(f"{tipo}: {p['apellido'].upper()}"):
            p["apellido"] = st.text_input("Apellido", p["apellido"], key=f"ap_{tipo}_{i}")
            p["nombre"] = st.text_input("Nombre", p["nombre"], key=f"nom_{tipo}_{i}")
            p["dni"] = st.text_input("DNI", p["dni"], key=f"dni_{tipo}_{i}")
            p["hijo_de"] = st.text_input("Hijo de", p["hijo_de"], key=f"hijo_{tipo}_{i}")
            p["domicilio"] = st.text_input("Domicilio", p["domicilio"], key=f"dom_{tipo}_{i}")

with tabs[1]:
    form_p("Arrestado", st.session_state.arrestados)
    st.divider()
    form_p("Víctima/Testigo", st.session_state.victimas)

# --- BLOQUE 3: INSPECCIÓN ---
with tabs[2]:
    st.subheader("📸 Inspección Ocular")
    st.session_state.inspeccion_ocular = st.text_area("Descripción de rastros y lugar:", value=st.session_state.inspeccion_ocular, height=300)

# --- BLOQUE 4: SECUESTROS ---
with tabs[3]:
    st.subheader("📦 Secuestros")
    if st.button("➕ Añadir Elemento"):
        st.session_state.secuestros.append({"item": "", "serie": ""})
    for i, s in enumerate(st.session_state.secuestros):
        ca, cb = st.columns(2)
        s["item"] = ca.text_input("Elemento", s["item"], key=f"item_{i}")
        s["serie"] = cb.text_input("Serie/Patente", s["serie"], key=f"serie_{i}")

# --- BLOQUE 5: CIERRE E IA ---
with tabs[4]:
    st.subheader("⚖️ Consulta Judicial")
    st.session_state.fiscal_turno = st.text_input("Fiscalía en turno", value=st.session_state.fiscal_turno)
    st.session_state.directivas_fiscal = st.text_area("Directivas:", value=st.session_state.directivas_fiscal)
    
    if st.button("🚀 GENERAR PAQUETE FINAL"):
        resumen = f"ACTA: {acta_n} | 911: {incidencia}\nHECHO: {st.session_state.relato_base}\n"
        resumen += f"DETENIDOS: {len(st.session_state.arrestados)}\nFISCAL: {st.session_state.fiscal_turno}"
        st.code(resumen)
