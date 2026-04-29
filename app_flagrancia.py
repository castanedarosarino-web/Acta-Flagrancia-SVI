import streamlit as st
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
st.set_page_config(page_title="SVI - Cooperativo Santa Fe", layout="wide", page_icon="🚔")

# Inicialización de estados (Corregido sin espacios extras)
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
# 2. PANEL DE RECEPCIÓN (SIN RESTRICCIONES)
# =====================================================
with st.sidebar:
    st.header("📂 Central de Recepción")
    st.caption("Operador: SubComisario Castañeda Juan")
    
    archivos = st.file_uploader("Recibir datos JSON", type=["json"], accept_multiple_files=True)
    
    if archivos:
        for a in archivos:
            try:
                datos = json.load(a)
                with st.expander(f"📥 Archivo: {a.name}", expanded=True):
                    st.write(f"Contenido: {len(datos.get('victimas',[]))} registros.")
                    if st.button(f"Importar Datos", key=f"btn_imp_{a.name}"):
                        st.session_state.victimas.extend(datos.get("victimas", []))
                        st.session_state.testigos.extend(datos.get("testigos", []))
                        st.session_state.arrestados.extend(datos.get("arrestados", []))
                        st.session_state.secuestros.extend(datos.get("secuestros", []))
                        if not st.session_state.relato_base:
                            st.session_state.relato_base = datos.get("relato_base", "")
                        st.success("✅ Datos sumados.")
                        st.rerun()
            except:
                st.error("Error en archivo")

    st.divider()
    
    datos_guardar = {
        "cup": st.session_state.cup,
        "relato_base": st.session_state.relato_base,
        "victimas": st.session_state.victimas,
        "testigos": st.session_state.testigos,
        "arrestados": st.session_state.arrestados,
        "secuestros": st.session_state.secuestros,
        "inspeccion_ocular": st.session_state.inspeccion_ocular,
        "fiscal_turno": st.session_state.fiscal_turno,
        "directivas_fiscal": st.session_state.directivas_fiscal
    }
    
    st.download_button(
        label="💾 Guardar Todo (PC)",
        data=json.dumps(datos_guardar, indent=4),
        file_name=f"SVI_{st.session_state.cup}.json" if st.session_state.cup else "SVI_BORRADOR.json",
        mime="application/json"
    )

# =====================================================
# 3. CUERPO DEL SISTEMA
# =====================================================
st.title("🚔 SVI - Consolidación de Sumarios")
tabs = st.tabs(["1. Inicio", "2. Filiación Completa", "3. Inspección Ocular", "4. Secuestros", "5. Final e IA"])

with tabs[0]:
    st.subheader("🛡️ Identificación del Procedimiento")
    c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
    ur = c1.selectbox("U. Regional", ["UR II", "UR IV", "UR XVII", "UR I"])
    dep = c2.selectbox("Dependencia", ["CRE PÉREZ", "CRE ROSARIO", "COMISARÍA 22", "OTRO"])
    acta = c3.text_input("Acta N°", value="")
    anio = c4.text_input("Año", value="2026")
    
    if acta:
        st.session_state.cup = f"{ur}-{dep.replace(' ', '_')}-{acta}-{anio}"
        st.info(f"🔐 SELLO ÚNICO: {st.session_state.cup}")
    
    st.session_state.relato_base = st.text_area("RELATO PREVENTIVO", value=st.session_state.relato_base, height=250)

def cargar_filiacion(tipo, lista):
    st.subheader(f"👤 {tipo}")
    if st.button(f"➕ Agregar {tipo}", key=f"add_{tipo}"):
        lista.append({"apellido": "", "nombre": "", "dni": "", "manifiesta": ""})
    for i, p in enumerate(lista):
        with st.expander(f"{tipo}: {p.get('apellido', 'Nuevo')}"):
            p["apellido"] = st.text_input("Apellido", p.get("apellido", ""), key=f"ap_{tipo}_{i}")
            p["nombre"] = st.text_input("Nombre", p.get("nombre", ""), key=f"nom_{tipo}_{i}")
            p["dni"] = st.text_input("DNI", p.get("dni", ""), key=f"dni_{tipo}_{i}")
            p["manifiesta"] = st.text_area("Dijo", p.get("manifiesta", ""), key=f"txt_{tipo}_{i}")

with tabs[1]:
    cargar_filiacion("Damnificado", st.session_state.victimas)
    st.divider()
    cargar_filiacion("Arrestado", st.session_state.arrestados)

with tabs[2]:
    st.session_state.inspeccion_ocular = st.text_area("Detalle ocular:", value=st.session_state.inspeccion_ocular, height=300)

with tabs[3]:
    if st.button("➕ Secuestro"):
        st.session_state.secuestros.append({"item": "", "serie": ""})
    for i, s in enumerate(st.session_state.secuestros):
        ca, cb = st.columns(2)
        s["item"] = ca.text_input("Elemento", s.get("item", ""), key=f"sec_i_{i}")
        s["serie"] = cb.text_input("Serie/Patente", s.get("serie", ""), key=f"sec_s_{i}")

with tabs[4]:
    st.session_state.fiscal_turno = st.text_input("Fiscal:", value=st.session_state.fiscal_turno)
    if st.button("🚀 PAQUETE FINAL"):
        st.code(f"Sumario: {st.session_state.cup}\nRelato: {st.session_state.relato_base}")
