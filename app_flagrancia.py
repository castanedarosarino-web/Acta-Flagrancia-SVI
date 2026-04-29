Import streamlit as st
from datetime import datetime, date
import json

# =====================================================
# 1. PROTOCOLO DE SEGURIDAD (TOKEN)
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
        st.info("Utilice el enlace oficial con token de seguridad.")
        st.stop()

verificar_acceso()

# =====================================================
# 2. CONFIGURACIÓN Y UTILIDADES
# =====================================================
st.set_page_config(page_title="SVI - Sistema de Validación de Identidad", layout="wide", page_icon="🚔")

MESES = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
         7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}

DEPENDENCIAS = ["COMANDO RADIOELÉCTRICO REGIONAL PÉREZ", "COMANDO RADIOELÉCTRICO ROSARIO", 
                "COMANDO RADIOELÉCTRICO FUNES", "COMISARÍA 22 PÉREZ", "COMISARÍA", "SUBCOMISARÍA", "B.O.U.", "G.T.M.", "OTRO"]

def formato_fecha_larga(fecha):
    return f"{fecha.day} días del mes de {MESES[fecha.month]} del año {fecha.year}"

def inicializar_estados():
    if "victimas" not in st.session_state: st.session_state.victimas = []
    if "testigos" not in st.session_state: st.session_state.testigos = []
    if "arrestados" not in st.session_state: st.session_state.arrestados = []
    if "secuestros" not in st.session_state: st.session_state.secuestros = []

inicializar_estados()

# =====================================================
# 3. PANEL DE CONTROL (SIDEBAR - FUSIÓN)
# =====================================================
with st.sidebar:
    st.header("📂 Consolidación SVI")
    st.caption("Autor: SubComisario Castañeda Juan")
    archivos = st.file_uploader("Subir archivos JSON de oficiales", type=["json"], accept_multiple_files=True)
    if archivos and st.button("Fusionar Datos de Calle"):
        for a in archivos:
            d = json.load(a)
            st.session_state.victimas.extend(d.get("victimas", []))
            st.session_state.testigos.extend(d.get("testigos", []))
            st.session_state.arrestados.extend(d.get("arrestados", []))
            st.session_state.secuestros.extend(d.get("secuestros", []))
        st.success("✅ Datos Unificados")
        st.rerun()
    
    if st.button("🗑️ Reiniciar Aplicación"):
        for k in ["victimas", "testigos", "arrestados", "secuestros"]: st.session_state[k] = []
        st.rerun()

# =====================================================
# 4. INTERFAZ DE CARGA (TABS)
# =====================================================
st.title("🚔 Sistema de Gestión de Actuaciones (SVI)")
t1, t2, t3, t4 = st.tabs(["1. Inicio", "2. Filiación y Entrevistas", "3. Inspección Ocular", "4. Vista Final"])

# --- TAB 1: INICIO ---
with t1:
    c1, c2 = st.columns(2)
    ciudad = c1.text_input("Ciudad", "Pérez")
    dependencia = c2.selectbox("Dependencia", DEPENDENCIAS)
    fecha = c1.date_input("Fecha", date.today())
    hora = c2.time_input("Hora", datetime.now().time())
    relato_base = st.text_area("Relato general del procedimiento (Hechos iniciales)")

# --- TAB 2: FILIACIÓN ESTILO SANTA FE ---
def agregar_persona_sf(tipo, lista):
    st.subheader(f"📋 Registro de {tipo}")
    if st.button(f"➕ Agregar {tipo}"):
        lista.append({
            "apellido": "", "nombre": "", "dni": "", "estado_civil": "Soltero/a",
            "edad": "", "ocupacion": "", "nacionalidad": "Argentina",
            "domicilio": "", "localidad": "Pérez", "telefono": "",
            "instruccion": "Sí", "entrevista_cuerpo": ""
        })

    for i, p in enumerate(lista):
        with st.expander(f"{tipo} N° {i+1}: {p.get('apellido', 'S/D')}"):
            c1, c2 = st.columns(2)
            p["apellido"] = c1.text_input("Apellido/s", p.get("apellido"), key=f"{tipo}_ap_{i}")
            p["nombre"] = c2.text_input("Nombre/s", p.get("nombre"), key=f"{tipo}_nom_{i}")
            c3, c4, c5 = st.columns([2, 2, 1])
            p["dni"] = c3.text_input("DNI N°", p.get("dni"), key=f"{tipo}_dni_{i}")
            p["estado_civil"] = c4.selectbox("Estado Civil", ["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Conviviente"], key=f"{tipo}_ec_{i}")
            p["edad"] = c5.text_input("Edad", p.get("edad"), key=f"{tipo}_ed_{i}")
            p["ocupacion"] = st.text_input("Profesión / Ocupación", p.get("ocupacion"), key=f"{tipo}_ocu_{i}")
            p["domicilio"] = st.text_input("Domicilio y Localidad", p.get("domicilio"), key=f"{tipo}_dom_{i}")
            p["telefono"] = st.text_input("Teléfono", p.get("telefono"), key=f"{tipo}_tel_{i}")
            p["instruccion"] = st.radio("¿Sabe leer y escribir?", ["Sí", "No"], key=f"{tipo}_inst_{i}", horizontal=True)
            p["entrevista_cuerpo"] = st.text_area("Manifestación / Entrevista", p.get("entrevista_cuerpo"), key=f"{tipo}_txt_{i}")

with t2:
    agregar_persona_sf("Damnificado", st.session_state.victimas)
    st.divider()
    agregar_persona_sf("Testigo", st.session_state.testigos)

# --- TAB 3: INSPECCIÓN OCULAR ---
with t3:
    st.header("📸 Relevamiento del Lugar")
    c1, c2, c3 = st.columns(3)
    clima = c1.selectbox("Clima", ["Despejado", "Lluvioso", "Nublado"])
    luz = c2.selectbox("Luz", ["Natural", "Artificial Buena", "Artificial Escasa"])
    visibilidad = c3.radio("Visibilidad", ["Buena", "Regular", "Mala"], horizontal=True)
    inspeccion_txt = st.text_area("Descripción de Inspección Ocular (Pegar análisis del Chat)", height=250)
    referencias_croquis = st.text_area("Referencias para el Croquis (Puntos A, B, C...)")

# --- TAB 4: VISTA FINAL ---
with t4:
    st.header("📄 Generación de Documentos")
    fiscal = st.text_input("Fiscal en Turno")
    directivas = st.text_area("Directivas impartidas por Fiscalía")
    
    # Generar Acta de Procedimiento
    if st.button("Generar Acta de Procedimiento"):
        acta = f"POLICÍA DE LA PROVINCIA DE SANTA FE\n{dependencia}\n\nEn la ciudad de {ciudad}, a los {formato_fecha_larga(fecha)}, siendo las {hora} horas... SE HACE CONSTAR: {relato_base}\n\nCOMUNICACIÓN: Consulta con Fiscal {fiscal}. Dispone: {directivas}."
        st.text_area("ACTA DE PROCEDIMIENTO", acta, height=250)

    # Generar Actas de Entrevista Independientes
    for p in st.session_state.victimas + st.session_state.testigos:
        if p.get("entrevista_cuerpo"):
            st.divider()
            inst = "sabe leer y escribir" if p["instruccion"] == "Sí" else "no sabe leer ni escribir"
            acta_ent = f"ACTA DE ENTREVISTA\nEn {ciudad}, a los {formato_fecha_larga(fecha)}, se identifica a {p['apellido'].upper()}, {p['nombre'].upper()}, DNI {p['dni']}, estado civil {p['estado_civil']}, ocupación {p['ocupacion']}, domic. en {p['domicilio']}. Quien consultado sobre si {inst}, responde afirmativamente. PREGUNTADO MANIFIESTA: {p['entrevista_cuerpo']}"
            st.text_area(f"ENTREVISTA: {p['apellido']}", acta_ent, height=200)

    # Generar Inspección Ocular
    if inspeccion_txt:
        st.divider()
        acta_insp = f"ACTA DE INSPECCIÓN OCULAR\nLugar: {ciudad}\nClima: {clima} | Luz: {luz} | Visibilidad: {visibilidad}\n\nRELEVAMIENTO: {inspeccion_txt}\n\nREFERENCIAS CROQUIS: {referencias_croquis}"
        st.text_area("INSPECCIÓN OCULAR", acta_insp, height=200)

    # DESCARGA DE RESPALDO JSON (Para oficiales de calle)
    st.divider()
    respaldo = {
        "victimas": st.session_state.victimas, "testigos": st.session_state.testigos,
        "arrestados": st.session_state.arrestados, "secuestros": st.session_state.secuestros
    }
    st.download_button("💾 Descargar Respaldo JSON", data=json.dumps(respaldo, default=str), file_name="respaldo_svi.json")
