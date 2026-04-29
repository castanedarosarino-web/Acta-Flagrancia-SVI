import streamlit as st
from datetime import datetime, date
import json

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
st.set_page_config(page_title="SVI - Cooperativo", layout="wide", page_icon="🚔")

# Inicialización de estados (Evita errores de variables vacías)
if "victimas" not in st.session_state: st.session_state.victimas = []
if "testigos" not in st.session_state: st.session_state.testigos = []
if "arrestados" not in st.session_state: st.session_state.arrestados = []
if "secuestros" not in st.session_state: st.session_state.secuestros = []
if "cup" not in st.session_state: st.session_state.cup = ""
if "relato_base" not in st.session_state: st.session_state.relato_base = ""
if "inspeccion_ocular" not in st.session_state: st.session_state.inspeccion_ocular = ""
if "fiscal_turno" not in st.session_state: st.session_state.fiscal_turno = ""
if "directivas_fiscal" not in st.session_state: st.session_state.directivas_fiscal = ""

# =====================================================
# 2. PANEL DE FUSIÓN INTELIGENTE (SIDEBAR)
# =====================================================
with st.sidebar:
    st.header("📂 Central de Recepción")
    st.caption(f"Operador: SubComisario Castañeda Juan")
    
    archivos = st.file_uploader("Recibir datos de oficiales (JSON)", type=["json"], accept_multiple_files=True)
    
    if archivos:
        for a in archivos:
            d = json.load(a)
            if d.get("cup") != st.session_state.cup:
                st.error(f"❌ CUP No Coincide: {a.name}")
                continue
            
            with st.expander(f"📥 Datos de: {a.name}", expanded=True):
                if st.button(f"Sumar Personas/Objetos", key=f"sum_{a.name}"):
                    st.session_state.victimas.extend(d.get("victimas", []))
                    st.session_state.testigos.extend(d.get("testigos", []))
                    st.session_state.arrestados.extend(d.get("arrestados", []))
                    st.session_state.secuestros.extend(d.get("secuestros", []))
                    st.rerun()

                if d.get("relato_base") and d.get("relato_base") != st.session_state.relato_base:
                    if st.button("📥 Importar Relato", key=f"rel_{a.name}"):
                        st.session_state.relato_base = d.get("relato_base")
                        st.rerun()
                
                if d.get("directivas_fiscal") and d.get("directivas_fiscal") != st.session_state.directivas_fiscal:
                    if st.button("📥 Importar Fiscal/Directivas", key=f"dir_{a.name}"):
                        st.session_state.directivas_fiscal = d.get("directivas_fiscal")
                        st.session_state.fiscal_turno = d.get("fiscal_turno")
                        st.rerun()

    st.divider()
    respaldo = {
        "cup": st.session_state.cup, "relato_base": st.session_state.relato_base,
        "victimas": st.session_state.victimas, "testigos": st.session_state.testigos,
        "arrestados": st.session_state.arrestados, "secuestros": st.session_state.secuestros,
        "inspeccion_ocular": st.session_state.inspeccion_ocular,
        "fiscal_turno": st.session_state.fiscal_turno, "directivas_fiscal": st.session_state.directivas_fiscal
    }
    st.download_button("💾 Guardar Todo (PC)", data=json.dumps(respaldo, indent=4), file_name=f"SVI_{st.session_state.cup}.json")

# =====================================================
# 3. INTERFAZ DE CARGA
# =====================================================
st.title("🚔 SVI - Consolidación de Sumarios")
t1, t2, t3, t4, t5 = st.tabs(["1. Inicio (CUP)", "2. Filiación", "3. Inspección", "4. Secuestros", "5. Final"])

with t1:
    st.subheader("🛡️ Identificación")
    c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
    ur = c1.selectbox("U. Regional", ["UR II", "UR IV", "UR XVII"])
    dep = c2.selectbox("Dependencia", ["CRE PÉREZ", "CRE ROSARIO", "COMISARÍA 22", "SUB 18", "OTRO"])
    acta = c3.text_input("Acta N°")
    anio = c4.text_input("Año", value="2026")
    
    if acta:
        st.session_state.cup = f"{ur}-{dep.replace(' ', '_')}-{acta}-{anio}"
        st.success(f"🔐 Sello: {st.session_state.cup}")
        # CORRECCIÓN AQUÍ: Se eliminó el typo 'relate_base'
        st.session_state.relato_base = st.text_area("Noticia Criminal / Relato Preventivo", value=st.session_state.relato_base, height=200)
    else:
        st.warning("Ingrese Nro de Acta")
        st.stop()

def cargar_p(tipo, lista):
    st.subheader(f"👥 {tipo}")
    if st.button(f"➕ Nuevo {tipo}", key=f"btn_{tipo}"):
        lista.append({"apellido": "", "nombre": "", "dni": "", "relato": ""})
    for i, p in enumerate(lista):
        with st.expander(f"{tipo}: {p['apellido'] if p['apellido'] else 'S/D'}"):
            p["apellido"] = st.text_input("Apellido", p["apellido"], key=f"{tipo}a{i}")
            p["nombre"] = st.text_input("Nombre", p["nombre"], key=f"{tipo}n{i}")
            p["dni"] = st.text_input("DNI", p["dni"], key=f"{tipo}d{i}")
            p["relato"] = st.text_area("Relato/Entrevista", p["relato"], key=f"{tipo}r{i}")

with t2:
    cargar_p("Damnificado", st.session_state.victimas)
    cargar_p("Testigo", st.session_state.testigos)
    cargar_p("Arrestado", st.session_state.arrestados)

with t3:
    st.session_state.inspeccion_ocular = st.text_area("Detalles de la Inspección Ocular", value=st.session_state.inspeccion_ocular, height=300)

with t4:
    if st.button("➕ Agregar Secuestro"):
        st.session_state.secuestros.append({"tipo": "Vehículo", "marca": "", "serie": ""})
    for i, s in enumerate(st.session_state.secuestros):
        with st.expander(f"📦 Secuestro {i+1}"):
            s["tipo"] = st.selectbox("Tipo", ["Vehículo", "Arma", "Celular", "Dinero"], key=f"st{i}")
            s["serie"] = st.text_input("Patente/Motor/IMEI", s["serie"], key=f"ss{i}")

with t5:
    st.session_state.fiscal_turno = st.text_input("Fiscal en Turno", value=st.session_state.fiscal_turno)
    st.session_state.directivas_fiscal = st.text_area("Directivas impartidas", value=st.session_state.directivas_fiscal)
    
    if st.button("🚀 Generar Paquete para IA"):
        resumen = f"CUP: {st.session_state.cup}\n\nRELATO: {st.session_state.relato_base}\n\n"
        resumen += f"INSPECCIÓN: {st.session_state.inspeccion_ocular}\n\n"
        resumen += f"FISCALÍA: {st.session_state.fiscal_turno} - Directivas: {st.session_state.directivas_fiscal}"
        st.text_area("Copiar y pegar en el chat:", resumen, height=300)
