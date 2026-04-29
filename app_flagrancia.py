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

# Inicialización de estados
 campos = ["victimas", "testigos", "arrestados", "secuestros"]
for campo in campos:
    if campo not in st.session_state: st.session_state[campo] = []

if "cup" not in st.session_state: st.session_state.cup = ""
if "relato_base" not in st.session_state: st.session_state.relato_base = ""
if "inspeccion_ocular" not in st.session_state: st.session_state.inspeccion_ocular = ""
if "fiscal_turno" not in st.session_state: st.session_state.fiscal_turno = ""
if "directivas_fiscal" not in st.session_state: st.session_state.directivas_fiscal = ""

# =====================================================
# 2. PANEL DE RECEPCIÓN (SUBIDA DE DATOS)
# =====================================================
with st.sidebar:
    st.header("📂 Central de Recepción")
    st.caption(f"Operador: SubComisario Castañeda Juan")
    
    archivos = st.file_uploader("Recibir datos de móviles (JSON)", type=["json"], accept_multiple_files=True)
    
    if archivos:
        for a in archivos:
            try:
                datos_importados = json.load(a)
                with st.expander(f"📥 Archivo: {a.name}", expanded=True):
                    # ELIMINAMOS LA VALIDACIÓN RÍGIDA DE CUP PARA EVITAR ERRORES
                    st.warning(f"Contenido: {len(datos_importados.get('victimas',[]))} Vict. / {len(datos_importados.get('arrestados',[]))} Arr.")
                    
                    if st.button(f"Fusionar en Acta Actual", key=f"fusi_{a.name}"):
                        st.session_state.victimas.extend(datos_importados.get("victimas", []))
                        st.session_state.testigos.extend(datos_importados.get("testigos", []))
                        st.session_state.arrestados.extend(datos_importados.get("arrestados", []))
                        st.session_state.secuestros.extend(datos_importados.get("secuestros", []))
                        
                        # Si el relato actual está vacío, traer el del archivo
                        if not st.session_state.relato_base:
                            st.session_state.relato_base = datos_importados.get("relato_base", "")
                        
                        st.success("✅ Datos integrados")
                        st.rerun()
            except Exception as e:
                st.error("Error al leer el archivo")

    st.divider()
    
    # --- SISTEMA DE GUARDADO ---
    datos_para_guardar = {
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
        label="💾 GUARDAR TODO",
        data=json.dumps(datos_para_guardar, indent=4),
        file_name=f"SVI_{st.session_state.cup}.json" if st.session_state.cup else "SVI_BORRADOR.json",
        mime="application/json"
    )

# =====================================================
# 3. CUERPO DEL ACTA
# =====================================================
st.title("🚔 SVI - Sistema de Validación de Identidad")
t1, t2, t3, t4, t5 = st.tabs(["1. Inicio", "2. Filiación", "3. Inspección", "4. Secuestros", "5. Final e IA"])

with t1:
    st.subheader("🛡️ Identificación del Procedimiento")
    col_a, col_b, col_c, col_d = st.columns([1, 2, 1, 1])
    ur = col_a.selectbox("U. Regional", ["UR II", "UR IV", "UR XVII", "UR I"])
    dep = col_b.selectbox("Dependencia", ["CRE PÉREZ", "CRE ROSARIO", "COMISARÍA 22", "SUB 18", "OTRO"])
    acta_n = col_c.text_input("Acta N°", value="")
    anio_n = col_d.text_input("Año", value="2026")
    
    # Actualizamos el CUP global
    if acta_n:
        st.session_state.cup = f"{ur}-{dep.replace(' ', '_')}-{acta_n}-{anio_n}"
        st.info(f"🔐 SELLO ÚNICO: {st.session_state.cup}")
    
    st.session_state.relato_base = st.text_area("RELATO PREVENTIVO / NOTICIA CRIMINAL", value=st.session_state.relato_base, height=300)

def cargar_persona(tipo, lista):
    st.subheader(f"👤 {tipo}")
    if st.button(f"➕ Añadir {tipo}", key=f"btn_{tipo}"):
        lista.append({"apellido": "", "nombre": "", "dni": "", "domicilio": "Pérez", "manifiesta": ""})
    
    for i, p in enumerate(lista):
        with st.expander(f"{tipo} {i+1}: {p['apellido']}"):
            p["apellido"] = st.text_input("Apellido", p["apellido"], key=f"ap_{tipo}_{i}")
            p["nombre"] = st.text_input("Nombre", p["nombre"], key=f"nom_{tipo}_{i}")
            p["dni"] = st.text_input("DNI", p["dni"], key=f"dni_{tipo}_{i}")
            p["domicilio"] = st.text_input("Domicilio", p["domicilio"], key=f"dom_{tipo}_{i}")
            p["manifiesta"] = st.text_area("Declaración", p["manifiesta"], key=f"man_{tipo}_{i}")

with t2:
    cargar_persona("Victima", st.session_state.victimas)
    st.divider()
    cargar_persona("Arrestado", st.session_state.arrestados)

with t3:
    st.session_state.inspeccion_ocular = st.text_area("Detalles de la Inspección Ocular:", value=st.session_state.inspeccion_ocular, height=300)

with t4:
    if st.button("➕ Agregar Secuestro"):
        st.session_state.secuestros.append({"item": "", "serie": ""})
    for i, s in enumerate(st.session_state.secuestros):
        col1, col2 = st.columns(2)
        s["item"] = col1.text_input("Elemento", s["item"], key=f"item_{i}")
        s["serie"] = col2.text_input("Nro Serie / Patente", s["serie"], key=f"serie_{i}")

with t5:
    st.session_state.fiscal_turno = st.text_input("Fiscal en turno:", value=st.session_state.fiscal_turno)
    st.session_state.directivas_fiscal = st.text_area("Directivas:", value=st.session_state.directivas_fiscal)
    
    if st.button("🚀 GENERAR RESUMEN PARA REDACCIÓN"):
        resumen = f"CUP: {st.session_state.cup}\nHECHO: {st.session_state.relato_base}\n"
        resumen += f"ARRESTADOS: {len(st.session_state.arrestados)}\n"
        st.text_area("Paquete de datos:", resumen)
