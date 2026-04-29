import streamlit as st
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

# Inicialización robusta de estados
if "victimas" not in st.session_state: st.session_state.victimas = []
if "testigos" not in st.session_state: st.session_state.testigos = []
if "arrestados" not in st.session_state: st.session_state.arrestados = []
if "secuestros" not in st.session_state: st.session_state.secuestros = []
if "cup" not in st.session_state: st.session_state.cup = ""
if "borrador_pulido" not in st.session_state: st.session_state.borrador_pulido = ""

# =====================================================
# 3. PANEL DE CONTROL (SIDEBAR)
# =====================================================
with st.sidebar:
    st.header("📂 Consolidación SVI")
    st.caption("Autor: SubComisario Castañeda Juan")
    st.info(f"**Sello CUP Activo:**\n{st.session_state.cup if st.session_state.cup else 'PENDIENTE'}")
    
    archivos = st.file_uploader("Subir archivos JSON de oficiales", type=["json"], accept_multiple_files=True)
    if archivos and st.button("Fusionar Datos de Calle"):
        for a in archivos:
            try:
                d = json.load(a)
                # VALIDACIÓN DE SELLO (CUP)
                if d.get("cup") != st.session_state.cup:
                    st.error(f"🚨 Rechazado: {a.name} pertenece a otra acta.")
                    continue
                st.session_state.victimas.extend(d.get("victimas", []))
                st.session_state.testigos.extend(d.get("testigos", []))
                st.session_state.arrestados.extend(d.get("arrestados", []))
                st.session_state.secuestros.extend(d.get("secuestros", []))
                st.success(f"✅ {a.name} unificado.")
            except Exception as e:
                st.error(f"Error al leer {a.name}: {e}")

    st.divider()
    # Botón de Descarga Preventiva (Respaldo)
    respaldo = {
        "cup": st.session_state.cup,
        "victimas": st.session_state.victimas, 
        "testigos": st.session_state.testigos,
        "arrestados": st.session_state.arrestados, 
        "secuestros": st.session_state.secuestros
    }
    st.download_button("💾 Descargar Respaldo JSON", 
                       data=json.dumps(respaldo, indent=4), 
                       file_name=f"SVI_{st.session_state.cup}.json")
    
    if st.button("🗑️ Reiniciar Aplicación"):
        st.session_state.clear()
        st.rerun()

# =====================================================
# 4. INTERFAZ DE CARGA (TABS)
# =====================================================
st.title("🚔 Sistema de Gestión de Actuaciones (SVI)")
t1, t2, t3, t4, t5 = st.tabs(["1. Inicio (CUP)", "2. Personas (Filiación Pro)", "3. Inspección Ocular", "4. Secuestros", "5. Vista Final e Impresión"])

# --- TAB 1: INICIO (SELLO MAESTRO) ---
with t1:
    st.subheader("🛡️ Identificación Única del Procedimiento")
    c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
    ur_val = c1.selectbox("U. Regional", ["UR II", "UR IV", "UR XVII"])
    dep_val = c2.selectbox("Dependencia", DEPENDENCIAS)
    acta_val = c3.text_input("Nro Acta", placeholder="Ej: 454")
    anio_val = c4.text_input("Año", value="2026")
    
    if acta_val:
        st.session_state.cup = f"{ur_val}-{dep_val.replace(' ', '_')}-{acta_val}-{anio_val}"
        st.success(f"🔐 Sello de Integridad Activo: **{st.session_state.cup}**")
        st.divider()
        col1, col2 = st.columns(2)
        ciudad = col1.text_input("Ciudad", "Pérez")
        fecha = col1.date_input("Fecha", date.today())
        hora = col2.time_input("Hora del Hecho", datetime.now().time())
        relato_base = st.text_area("Relato general del procedimiento (Hechos iniciales)")
    else:
        st.warning("⚠️ DEBE INGRESAR EL NRO DE ACTA PARA DESBLOQUEAR EL SISTEMA")
        st.stop()

# --- TAB 2: FILIACIÓN ---
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
    st.divider()
    agregar_persona_sf("Arrestado", st.session_state.arrestados)

# --- TAB 3: INSPECCIÓN OCULAR ---
with t3:
    st.header("📸 Relevamiento del Lugar")
    c1, c2, c3 = st.columns(3)
    clima = c1.selectbox("Clima", ["Despejado", "Lluvioso", "Nublado", "Neblina"])
    luz = c2.selectbox("Luz", ["Natural", "Artificial Buena", "Artificial Escasa", "Nula"])
    visibilidad = c3.radio("Visibilidad", ["Buena", "Regular", "Mala"], horizontal=True)
    inspeccion_txt = st.text_area("Descripción de Inspección Ocular (Detalle de daños y rastros)", height=250)
    referencias_croquis = st.text_area("Referencias para el Croquis (Puntos A, B, C...)")

# --- TAB 4: SECUESTROS ---
with t4:
    st.subheader("📦 Registro Técnico de Secuestros")
    if st.button("➕ Agregar Elemento"):
        st.session_state.secuestros.append({"tipo": "Vehículo", "marca": "", "modelo": "", "nro_serie": "", "detalle": ""})
    
    for i, s in enumerate(st.session_state.secuestros):
        with st.expander(f"📦 Elemento {i+1}: {s['tipo']}"):
            c_s1, c_s2, c_s3 = st.columns(3)
            s["tipo"] = c_s1.selectbox("Tipo", ["Vehículo", "Arma", "Celular", "Dinero", "Otros"], key=f"sec_t_{i}")
            s["marca"] = c_s2.text_input("Marca", key=f"sec_m_{i}")
            s["modelo"] = c_s3.text_input("Modelo / Calibre", key=f"sec_mo_{i}")
            s["nro_serie"] = st.text_input("Serie / Motor / IMEI / Patente", key=f"sec_se_{i}")
            s["detalle"] = st.text_area("Estado y Observaciones", key=f"sec_de_{i}")

# --- TAB 5: VISTA FINAL E IMPRESIÓN ---
with t5:
    st.header("📄 Generación de Documentos y Pulido IA")
    fiscal = st.text_input("Fiscal en Turno")
    directivas = st.text_area("Directivas impartidas por Fiscalía")
    
    if st.button("🚀 Procesar Acta para Pulido IA"):
        # Protocolo para la IA
        protocolo = f"--- PROTOCOLO SVI CASTAÑEDA: ACTA {st.session_state.cup} ---\n"
        protocolo += "DIRECTIVA: Traducir entrevistas a lenguaje jurídico impecable. Mantener DNI y datos fijos. Generar Resumen Noticia Criminal.\n\n"
        
        cuerpo_acta = f"POLICÍA DE LA PROVINCIA DE SANTA FE\n{dep_val}\n\n"
        cuerpo_acta += f"En la ciudad de {ciudad}, a los {formato_fecha_larga(fecha)}, siendo las {hora} horas... SE HACE CONSTAR: {relato_base}\n\n"
        cuerpo_acta += f"INSPECCIÓN OCULAR: Clima {clima}, Luz {luz}, Visibilidad {visibilidad}. {inspeccion_txt}\n\n"
        
        personas = "PERSONAS INVOLUCRADAS Y MANIFESTACIONES:\n"
        for p in st.session_state.victimas + st.session_state.testigos + st.session_state.arrestados:
            personas += f"- {p['apellido'].upper()}, {p['nombre']} (DNI {p['dni']}): {p['entrevista_cuerpo']}\n"
            
        sec = "\nELEMENTOS SECUESTRADOS:\n"
        for s in st.session_state.secuestros:
            sec += f"- {s['tipo']} {s['marca']} {s['modelo']} (ID: {s['nro_serie']}) - Obs: {s['detalle']}\n"
            
        final = f"\nCONSULTA FISCAL: Fiscal {fiscal}. Directivas: {directivas}."
        
        st.session_state.borrador_pulido = protocolo + cuerpo_acta + personas + sec + final
        st.success("✅ Datos preparados para procesar")

    if st.session_state.borrador_pulido:
        st.text_area("1. COPIAR PARA EL CHAT (GÉMINI/GPT):", st.session_state.borrador_pulido, height=300)
        st.divider()
        st.text_area("2. PEGAR AQUÍ EL RESULTADO PULIDO (LISTO PARA IMPRIMIR):", height=400)
