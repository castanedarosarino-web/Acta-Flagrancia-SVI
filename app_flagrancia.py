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

# Inicialización de estados (Evita errores de variables vacías)
campos_lista = ["victimas", "testigos", "arrestados", "secuestros"]
for campo in campos_lista:
    if campo not in st.session_state: st.session_state[campo] = []

if "cup" not in st.session_state: st.session_state.cup = ""
if "relato_base" not in st.session_state: st.session_state.relato_base = ""
if "inspeccion_ocular" not in st.session_state: st.session_state.inspeccion_ocular = ""
if "fiscal_turno" not in st.session_state: st.session_state.fiscal_turno = ""
if "directivas_fiscal" not in st.session_state: st.session_state.directivas_fiscal = ""

# =====================================================
# 2. PANEL DE RECEPCIÓN (ELIMINADA TODA RESTRICCIÓN)
# =====================================================
with st.sidebar:
    st.header("📂 Central de Recepción")
    st.caption("Operador: SubComisario Castañeda Juan")
    
    archivos = st.file_uploader("Recibir datos JSON", type=["json"], accept_multiple_files=True)
    
    if archivos:
        for a in archivos:
            try:
                # Leemos el archivo sin importar el nombre o el CUP interno
                datos = json.load(a)
                with st.expander(f"📥 Archivo: {a.name}", expanded=True):
                    # Solo mostramos resumen para que el usuario sepa qué está cargando
                    st.write(f"Contiene: {len(datos.get('victimas',[]))} personas.")
                    
                    if st.button(f"Importar Datos", key=f"btn_imp_{a.name}"):
                        # Unimos las listas sin validaciones previas
                        st.session_state.victimas.extend(datos.get("victimas", []))
                        st.session_state.testigos.extend(datos.get("testigos", []))
                        st.session_state.arrestados.extend(datos.get("arrestados", []))
                        st.session_state.secuestros.extend(datos.get("secuestros", []))
                        
                        # Si el relato está vacío en el sistema principal, traemos el del archivo
                        if not st.session_state.relato_base:
                            st.session_state.relato_base = datos.get("relato_base", "")
                        
                        st.success("✅ Integrado correctamente")
                        st.rerun()
            except:
                st.error("Archivo no compatible")

    st.divider()
    
    # --- BOTÓN DE GUARDADO ---
    datos_actuales = {
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
        data=json.dumps(datos_actuales, indent=4),
        file_name=f"SVI_{st.session_state.cup}.json" if st.session_state.cup else "SVI_PROCESO.json",
        mime="application/json"
    )

# =====================================================
# 3. INTERFAZ DE CARGA
# =====================================================
st.title("🚔 SVI - Consolidación de Sumarios")
tabs = st.tabs(["1. Inicio", "2. Filiación Completa", "3. Inspección Ocular", "4. Secuestros", "5. Final e IA"])

with tabs[0]:
    st.subheader("🛡️ Identificación del Procedimiento")
    c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
    ur = c1.selectbox("U. Regional", ["UR II", "UR IV", "UR XVII", "UR I"])
    dep = c2.selectbox("Dependencia", ["CRE PÉREZ", "CRE ROSARIO", "CRE FUNES", "COMISARÍA 22", "OTRO"])
    acta = c3.text_input("Acta N°", value="")
    anio = c4.text_input("Año", value="2026")
    
    if acta:
        st.session_state.cup = f"{ur}-{dep.replace(' ', '_')}-{acta}-{anio}"
        st.info(f"🔐 SELLO ÚNICO: {st.session_state.cup}")
    
    st.session_state.relato_base = st.text_area("RELATO PREVENTIVO / NOTICIA CRIMINAL", value=st.session_state.relato_base, height=250)

def render_filiacion(tipo, lista):
    st.subheader(f"👤 {tipo}")
    if st.button(f"➕ Agregar {tipo}", key=f"add_{tipo}"):
        lista.append({"apellido": "", "nombre": "", "dni": "", "domicilio": "", "manifiesta": ""})
    
    for i, p in enumerate(lista):
        with st.expander(f"{tipo}: {p.get('apellido', 'Nuevo')}"):
            p["apellido"] = st.text_input("Apellido", p.get("apellido", ""), key=f"ap_{tipo}_{i}")
            p["nombre"] = st.text_input("Nombre", p.get("nombre", ""), key=f"nom_{tipo}_{i}")
            p["dni"] = st.text_input("DNI", p.get("dni", ""), key=f"dni_{tipo}_{i}")
            p["manifiesta"] = st.text_area("Declaración / Entrevista", p.get("manifiesta", ""), key=f"txt_{tipo}_{i}")

with tabs[1]:
    render_filiacion("Damnificado", st.session_state.victimas)
    st.divider()
    render_filiacion("Arrestado", st.session_state.arrestados)
    st.divider()
    render_filiacion("Testigo", st.session_state.testigos)

with tabs[2]:
    st.session_state.inspeccion_ocular = st.text_area("Inspección Ocular y Rastreos:", value=st.session_state.inspeccion_ocular, height=300)

with tabs[3]:
    if st.button("➕ Cargar Elemento"):
        st.session_state.secuestros.append({"item": "", "serie": ""})
    for i, s in enumerate(st.session_state.secuestros):
        ca, cb = st.columns(2)
        s["item"] = ca.text_input("Elemento", s.get("item", ""), key=f"sec_i_{i}")
        s["serie"] = cb.text_input("Nro Serie / Patente", s.get("serie", ""), key=f"sec_s_{i}")

with tabs[4]:
    st.session_state.fiscal_turno = st.text_input("Fiscalía / Dr.", value=st.session_state.fiscal_turno)
    st.session_state.directivas_fiscal = st.text_area("Directivas del Magistrado", value=st.session_state.directivas_fiscal)
    
    if st.button("🚀 GENERAR PAQUETE PARA REDACCIÓN"):
        redaccion = f"CUP: {st.session_state.cup}\nFISCAL: {st.session_state.fiscal_turno}\nRELATO: {st.session_state.relato_base}\n"
        st.text_area("Copiá este texto para la IA:", redaccion, height=300)
