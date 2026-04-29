import streamlit as st
import json

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
st.set_page_config(page_title="SVI - Santa Fe v4.0", layout="wide", page_icon="🚔")

# Inicialización de estados para no perder datos al cambiar de pestaña
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
# 2. PANEL DE RECEPCIÓN (SIDEBAR) - CARGA DE ARCHIVOS
# =====================================================
with st.sidebar:
    st.header("📂 Central de Recepción")
    st.caption("Operador: SubComisario Castañeda Juan")
    
    archivos = st.file_uploader("Recibir datos JSON", type=["json"], accept_multiple_files=True)
    
    if archivos:
        for a in archivos:
            try:
                datos_mvl = json.load(a)
                with st.expander(f"📥 Archivo: {a.name}", expanded=True):
                    st.write(f"Trae: {len(datos_mvl.get('victimas', []))} Vict / {len(datos_mvl.get('arrestados', []))} Arr.")
                    if st.button(f"Fusionar Datos", key=f"fush_{a.name}"):
                        st.session_state.victimas.extend(datos_mvl.get("victimas", []))
                        st.session_state.testigos.extend(datos_mvl.get("testigos", []))
                        st.session_state.arrestados.extend(datos_mvl.get("arrestados", []))
                        st.session_state.secuestros.extend(datos_mvl.get("secuestros", []))
                        if not st.session_state.relato_base:
                            st.session_state.relato_base = datos_mvl.get("relato_base", "")
                        st.success("✅ Datos integrados")
                        st.rerun()
            except:
                st.error("Error en archivo")

    st.divider()
    
    # --- BOTÓN DE GUARDADO FINAL ---
    final_json = {
        "cup": st.session_state.cup, "relato_base": st.session_state.relato_base,
        "victimas": st.session_state.victimas, "testigos": st.session_state.testigos,
        "arrestados": st.session_state.arrestados, "secuestros": st.session_state.secuestros,
        "inspeccion_ocular": st.session_state.inspeccion_ocular,
        "fiscal_turno": st.session_state.fiscal_turno, "directivas_fiscal": st.session_state.directivas_fiscal
    }
    
    st.download_button(
        label="💾 Guardar Todo (PC)",
        data=json.dumps(final_json, indent=4),
        file_name=f"SVI_{st.session_state.cup if st.session_state.cup else 'BORRADOR'}.json",
        mime="application/json"
    )

# =====================================================
# 3. CUERPO PRINCIPAL (BLOQUES 1 AL 5)
# =====================================================
st.title("🚔 SVI - Consolidación de Sumarios")
tabs = st.tabs(["1. Inicio", "2. Filiación Completa", "3. Inspección Ocular", "4. Secuestros", "5. Final e IA"])

# --- BLOQUE 1: INICIO ---
with tabs[0]:
    st.subheader("🛡️ Identificación del Procedimiento")
    c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
    ur = c1.selectbox("U. Regional", ["UR II", "UR IV", "UR XVII", "UR I"])
    dep = c2.selectbox("Dependencia", ["CRE PÉREZ", "CRE ROSARIO", "COMISARÍA 22", "SUB 18", "OTRO"])
    acta_n = c3.text_input("Acta N°", value="")
    anio_n = c4.text_input("Año", value="2026")
    
    if acta_n:
        st.session_state.cup = f"{ur}-{dep.replace(' ', '_')}-{acta_n}-{anio_n}"
        st.info(f"🔐 SELLO ÚNICO: {st.session_state.cup}")
    
    st.session_state.relato_base = st.text_area("RELATO PREVENTIVO / NOTICIA CRIMINAL", value=st.session_state.relato_base, height=300)

# --- BLOQUE 2: FILIACIÓN ---
def form_persona(tipo, lista):
    st.subheader(f"👤 Registro de {tipo}")
    if st.button(f"➕ Agregar {tipo}", key=f"add_{tipo}"):
        lista.append({"apellido": "", "nombre": "", "dni": "", "domicilio": "Pérez", "manifiesta": ""})
    
    for i, p in enumerate(lista):
        with st.expander(f"{tipo}: {p['apellido'].upper() if p['apellido'] else 'NUEVO REGISTRO'}"):
            p["apellido"] = st.text_input("Apellido/s", p["apellido"], key=f"ap_{tipo}_{i}")
            p["nombre"] = st.text_input("Nombre/s", p["nombre"], key=f"nom_{tipo}_{i}")
            p["dni"] = st.text_input("DNI", p["dni"], key=f"dni_{tipo}_{i}")
            p["domicilio"] = st.text_input("Domicilio Real", p["domicilio"], key=f"dom_{tipo}_{i}")
            p["manifiesta"] = st.text_area("Manifestación Técnica / Entrevista", p["manifiesta"], key=f"txt_{tipo}_{i}")

with tabs[1]:
    form_persona("Damnificado", st.session_state.victimas)
    st.divider()
    form_persona("Testigo", st.session_state.testigos)
    st.divider()
    form_persona("Arrestado", st.session_state.arrestados)

# --- BLOQUE 3: INSPECCIÓN ---
with tabs[2]:
    st.subheader("📸 Inspección Ocular")
    st.session_state.inspeccion_ocular = st.text_area("Descripción del lugar y rastros:", value=st.session_state.inspeccion_ocular, height=400)

# --- BLOQUE 4: SECUESTROS ---
with tabs[3]:
    st.subheader("📦 Registro de Secuestros")
    if st.button("➕ Agregar Elemento"):
        st.session_state.secuestros.append({"item": "", "serie": ""})
    
    for i, s in enumerate(st.session_state.secuestros):
        c1, c2 = st.columns(2)
        s["item"] = c1.text_input("Elemento / Vehículo", s["item"], key=f"sec_i_{i}")
        s["serie"] = c2.text_input("Serie / Patente / IMEI", s["serie"], key=f"sec_s_{i}")

# --- BLOQUE 5: FINAL E IA ---
with tabs[4]:
    st.subheader("⚖️ Cierre y Procesamiento")
    st.session_state.fiscal_turno = st.text_input("Fiscalía / Dr.", value=st.session_state.fiscal_turno)
    st.session_state.directivas_fiscal = st.text_area("Directivas impartidas:", value=st.session_state.directivas_fiscal)
    
    if st.button("🚀 PREPARAR PAQUETE PARA REDACCIÓN IA"):
        paquete = f"AUTOR: SubComisario Castañeda Juan\nCUP: {st.session_state.cup}\nHECHO: {st.session_state.relato_base}\n"
        paquete += f"\nARRESTADOS: {len(st.session_state.arrestados)}\nVICTIMAS: {len(st.session_state.victimas)}\n"
        st.success("✅ Datos consolidados.")
        st.text_area("Copiar para IA:", paquete, height=400)
