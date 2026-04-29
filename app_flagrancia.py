import streamlit as st
from datetime import datetime, date
import json
import base64

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
# 2. PANEL DE FUSIÓN (SIDEBAR)
# =====================================================
with st.sidebar:
    st.header("📂 Central de Recepción")
    st.caption(f"Operador: SubComisario Castañeda Juan")
    
    archivos = st.file_uploader("Recibir datos JSON", type=["json"], accept_multiple_files=True)
    
    if archivos:
        for a in archivos:
            try:
                d = json.load(a)
                if d.get("cup") != st.session_state.cup:
                    st.error(f"❌ CUP Diferente: {a.name}")
                    continue
                
                with st.expander(f"📥 De: {a.name}", expanded=True):
                    if st.button(f"Sumar Filiaciones/Objetos", key=f"sum_{a.name}"):
                        st.session_state.victimas.extend(d.get("victimas", []))
                        st.session_state.testigos.extend(d.get("testigos", []))
                        st.session_state.arrestados.extend(d.get("arrestados", []))
                        st.session_state.secuestros.extend(d.get("secuestros", []))
                        st.rerun()

                    if d.get("relato_base") and d.get("relato_base") != st.session_state.relato_base:
                        if st.button("📥 Importar Relato", key=f"rel_{a.name}"):
                            st.session_state.relato_base = d.get("relato_base")
                            st.rerun()
            except:
                st.error("Archivo corrupto")

    st.divider()
    
    # --- PARCHE DE DESCARGA SEGURA ---
    datos_finales = {
        "cup": st.session_state.cup, "relato_base": st.session_state.relato_base,
        "victimas": st.session_state.victimas, "testigos": st.session_state.testigos,
        "arrestados": st.session_state.arrestados, "secuestros": st.session_state.secuestros,
        "inspeccion_ocular": st.session_state.inspeccion_ocular,
        "fiscal_turno": st.session_state.fiscal_turno, "directivas_fiscal": st.session_state.directivas_fiscal
    }
    
    json_string = json.dumps(datos_finales, indent=4)
    # Creamos un botón de descarga más robusto
    st.download_button(
        label="💾 Guardar Todo (PC)",
        data=json_string,
        file_name=f"SVI_{st.session_state.cup if st.session_state.cup else 'BORRADOR'}.json",
        mime="application/json",
        key="download_btn_main"
    )

# =====================================================
# 3. INTERFAZ PRINCIPAL (TABS)
# =====================================================
st.title("🚔 SVI - Consolidación de Sumarios")
t1, t2, t3, t4, t5 = st.tabs(["1. Inicio", "2. Filiación Completa", "3. Inspección Ocular", "4. Secuestros", "5. Final e IA"])

with t1:
    st.subheader("🛡️ Identificación del Procedimiento")
    col_a, col_b, col_c, col_d = st.columns([1, 2, 1, 1])
    ur = col_a.selectbox("U. Regional", ["UR II", "UR IV", "UR XVII", "UR I"])
    dep = col_b.selectbox("Dependencia", ["CRE PÉREZ", "CRE ROSARIO", "COMISARÍA 22", "SUB 18", "OTRO"])
    acta = col_c.text_input("Acta N°", placeholder="Nro")
    anio = col_d.text_input("Año", value="2026")
    
    if acta:
        st.session_state.cup = f"{ur}-{dep.replace(' ', '_')}-{acta}-{anio}"
        st.info(f"🔐 SELLO ÚNICO: {st.session_state.cup}")
        st.session_state.relato_base = st.text_area("RELATO PREVENTIVO / NOTICIA CRIMINAL", value=st.session_state.relato_base, height=250)
    else:
        st.warning("⚠️ DEBE ASIGNAR UN NRO DE ACTA PARA EMPEZAR")
        st.stop()

def cargar_persona_pro(tipo, lista):
    st.subheader(f"👤 Registro de {tipo}")
    if st.button(f"➕ Agregar {tipo}", key=f"add_{tipo}"):
        lista.append({
            "apellido": "", "nombre": "", "dni": "", "nacimiento": "S/D",
            "estado_civil": "Soltero/a", "ocupacion": "", "domicilio": "Pérez",
            "instruccion": "Sí", "manifiesta": ""
        })
    
    for i, p in enumerate(lista):
        with st.expander(f"{tipo}: {p['apellido'].upper() if p['apellido'] else 'Nuevo'}"):
            c1, c2 = st.columns(2)
            p["apellido"] = c1.text_input("Apellido/s", p["apellido"], key=f"{tipo}ap{i}")
            p["nombre"] = c2.text_input("Nombre/s", p["nombre"], key=f"{tipo}nom{i}")
            
            c3, c4, c5 = st.columns([2, 2, 1])
            p["dni"] = c3.text_input("DNI / Pasaporte", p["dni"], key=f"{tipo}dni{i}")
            p["estado_civil"] = c4.selectbox("Estado Civil", ["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Conviviente"], key=f"{tipo}ec{i}")
            p["instruccion"] = c5.radio("¿Sabe leer?", ["Sí", "No"], key=f"{tipo}ins{i}")
            
            p["ocupacion"] = st.text_input("Profesión / Ocupación", p["ocupacion"], key=f"{tipo}oc{i}")
            p["domicilio"] = st.text_input("Domicilio Real", p["domicilio"], key=f"{tipo}dom{i}")
            p["manifiesta"] = st.text_area("Entrevista / Manifestación Técnica", p["manifiesta"], key=f"{tipo}man{i}")

with t2:
    cargar_persona_pro("Damnificado", st.session_state.victimas)
    st.divider()
    cargar_persona_pro("Testigo", st.session_state.testigos)
    st.divider()
    cargar_persona_pro("Arrestado", st.session_state.arrestados)

with t3:
    st.subheader("📸 Inspección Ocular")
    st.session_state.inspeccion_ocular = st.text_area("Descripción del lugar, rastros, daños y clima:", value=st.session_state.inspeccion_ocular, height=350)

with t4:
    st.subheader("📦 Registro de Secuestros")
    if st.button("➕ Agregar Elemento"):
        st.session_state.secuestros.append({"tipo": "Vehículo", "marca": "", "modelo": "", "identificador": "", "estado": ""})
    
    for i, s in enumerate(st.session_state.secuestros):
        with st.expander(f"Objeto {i+1}: {s['tipo']}"):
            s["tipo"] = st.selectbox("Categoría", ["Vehículo", "Arma de Fuego", "Arma Blanca", "Celular", "Dinero", "Herramienta", "Otro"], key=f"stipo{i}")
            c1, c2 = st.columns(2)
            s["marca"] = c1.text_input("Marca", s["marca"], key=f"smarca{i}")
            s["modelo"] = c2.text_input("Modelo", s["modelo"], key=f"smod{i}")
            s["identificador"] = st.text_input("Nro Serie / Patente / IMEI", s["identificador"], key=f"sid{i}")
            s["estado"] = st.text_area("Observaciones de conservación", s["estado"], key=f"sobs{i}")

with t5:
    st.subheader("⚖️ Cierre y Procesamiento")
    c_f1, c_f2 = st.columns(2)
    st.session_state.fiscal_turno = c_f1.text_input("Fiscalía / Dr.", value=st.session_state.fiscal_turno)
    st.session_state.directivas_fiscal = st.text_area("Directivas impartidas por el Magistrado", value=st.session_state.directivas_fiscal)
    
    if st.button("🚀 PREPARAR ACTA FINAL PARA IA"):
        paquete = f"AUTOR: SubComisario Castañeda Juan\nACTA: {st.session_state.cup}\nHECHO: {st.session_state.relato_base}\n\n"
        for lista, nombre in [(st.session_state.victimas, "VICTIMAS"), (st.session_state.testigos, "TESTIGOS"), (st.session_state.arrestados, "ARRESTADOS")]:
            paquete += f"[{nombre}]:\n"
            for p in lista:
                paquete += f"- {p['apellido'].upper()}, {p['nombre']}. DNI: {p['dni']}. Dijo: {p['manifiesta']}\n"
        st.success("✅ Paquete de datos consolidado.")
        st.text_area("Copiar este bloque:", paquete, height=400)
