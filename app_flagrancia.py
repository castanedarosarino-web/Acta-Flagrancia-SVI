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
st.set_page_config(page_title="Acta Flagrancia SVI", layout="wide", page_icon="🚔")

MESES = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
         7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}

DEPENDENCIAS = ["COMANDO RADIOELÉCTRICO REGIONAL PÉREZ", "COMANDO RADIOELÉCTRICO ROSARIO", 
                "COMANDO RADIOELÉCTRICO FUNES", "COMISARÍA 22 PÉREZ", "COMISARÍA", "SUBCOMISARÍA", "B.O.U.", "G.T.M.", "OTRO"]

DOCUMENTOS_ENTREGA = ["acta de aprehensión", "acta de procedimiento", "acta de secuestro", "cadena de custodia", 
                     "inspección ocular", "croquis demostrativo", "fotografías", "acta/s de entrevista/s", "otro"]

def formato_fecha_larga(fecha):
    return f"{fecha.day} días del mes de {MESES[fecha.month]} del año {fecha.year}"

def edad(fecha_nac):
    if not fecha_nac: return ""
    hoy = date.today()
    return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

def inicializar():
    if "victimas" not in st.session_state: st.session_state.victimas = []
    if "testigos" not in st.session_state: st.session_state.testigos = []
    if "arrestados" not in st.session_state: st.session_state.arrestados = []
    if "secuestros" not in st.session_state: st.session_state.secuestros = []

inicializar()

# =====================================================
# 3. PANEL DE FUSIÓN (SIDEBAR)
# =====================================================
with st.sidebar:
    st.header("📂 Consolidación SVI")
    archivos = st.file_uploader("Subir JSON de la calle", type=["json"], accept_multiple_files=True)
    if archivos and st.button("Fusionar Datos"):
        for a in archivos:
            d = json.load(a)
            st.session_state.victimas.extend(d.get("victimas", []))
            st.session_state.testigos.extend(d.get("testigos", []))
            st.session_state.arrestados.extend(d.get("arrestados", []))
            st.session_state.secuestros.extend(d.get("secuestros", []))
        st.success("✅ Datos Unificados")
        st.rerun()
    
    if st.button("🗑️ Limpiar App"):
        for k in ["victimas", "testigos", "arrestados", "secuestros"]: st.session_state[k] = []
        st.rerun()

# =====================================================
# 4. FUNCIONES DE REDACCIÓN TÉCNICA
# =====================================================
def generar_persona_texto(p):
    return f"{p.get('apellido', '').upper()}, {p.get('nombre', '').upper()}, DNI N° {p.get('dni', '')}"

def armar_acta_completa(d):
    # Encabezado
    texto = f"POLICÍA DE LA PROVINCIA DE SANTA FE\n{d['dependencia']}\n\n"
    texto += f"En la ciudad de {d['ciudad']}, a los {formato_fecha_larga(d['fecha'])}, siendo las {d['hora']} horas... SE HACE CONSTAR:\n\n"
    
    # Hecho
    texto += f"Que {d['relato_ia'] if d['relato_ia'] else d['relato_base']}\n\n"
    
    # Personas
    if st.session_state.arrestados:
        texto += "APREHENDIDOS:\n"
        for a in st.session_state.arrestados:
            texto += f"- {generar_persona_texto(a)}, nacido el {a.get('fecha_nac')}, hijo de {a.get('hijo_de')}, domic. en {a.get('domicilio')}.\n"
    
    if st.session_state.secuestros:
        texto += "\nSECUESTROS:\n"
        for s in st.session_state.secuestros:
            texto += f"- {s.get('texto')}\n"
            
    texto += f"\nCOMUNICACIÓN: Se entabla consulta con {d['fiscal']}, quien dispone: {d['directivas']}."
    return texto

# =====================================================
# 5. INTERFAZ (TABS)
# =====================================================
st.title("🚔 Sistema SVI - Gestión de Actas")
st.caption(f"SubComisario Castañeda Juan | UR II")

t1, t2, t3, t4 = st.tabs(["1. Inicio", "2. Detenidos/Secuestro", "3. Inspección", "4. Vista Final"])

with t1:
    c1, c2 = st.columns(2)
    ciudad = c1.text_input("Ciudad", "Pérez")
    dependencia = c2.selectbox("Dependencia", DEPENDENCIAS)
    fecha = c1.date_input("Fecha", date.today())
    hora = c2.time_input("Hora", datetime.now().time())
    relato_base = st.text_area("Relato de los hechos")
    relato_ia = st.text_area("Pegar Redacción de ChatGPT (si se usó)")

with t2:
    if st.button("➕ Cargar Arrestado"):
        st.session_state.arrestados.append({"apellido": "", "nombre": "", "dni": "", "fecha_nac": date(1998, 5, 15), "hijo_de": "", "domicilio": "", "descripcion": ""})
    
    for i, a in enumerate(st.session_state.arrestados):
        with st.expander(f"Arrestado {i+1}"):
            a["apellido"] = st.text_input("Apellido", a["apellido"], key=f"ap_{i}")
            a["nombre"] = st.text_input("Nombre", a["nombre"], key=f"nom_{i}")
            a["dni"] = st.text_input("DNI", a["dni"], key=f"dni_{i}")
            a["hijo_de"] = st.text_input("Hijo de", a["hijo_de"], key=f"hijo_{i}")
            a["domicilio"] = st.text_input("Domicilio", a["domicilio"], key=f"dom_{i}")
            st.text_area("Descripción física", key=f"desc_{i}")

    st.divider()
    if st.button("➕ Cargar Secuestro"):
        st.session_state.secuestros.append({"tipo": "", "texto": ""})
    
    for i, s in enumerate(st.session_state.secuestros):
        with st.expander(f"Secuestro {i+1}"):
            s["tipo"] = st.selectbox("Tipo", TIPOS_SECUESTRO, key=f"tipo_s_{i}")
            s["texto"] = st.text_area("Descripción técnica", key=f"txt_s_{i}")

with t4:
    st.header("Vista Final")
    fiscal = st.text_input("Fiscal en turno")
    directivas = st.text_area("Directivas impartidas")
    
    datos_acta = {
        "ciudad": ciudad, "dependencia": dependencia, "fecha": fecha, "hora": hora,
        "relato_base": relato_base, "relato_ia": relato_ia, "fiscal": fiscal, "directivas": directivas
    }
    
    acta_final = armar_acta_completa(datos_acta)
    st.text_area("Acta Lista para Word", acta_final, height=500)
    
    # BOTÓN DE RESPALDO (Crucial para el flujo calle-PC)
    respaldo = {
        "victimas": st.session_state.victimas,
        "testigos": st.session_state.testigos,
        "arrestados": [{k: str(v) for k, v in a.items()} for a in st.session_state.arrestados],
        "secuestros": st.session_state.secuestros,
    }
    
    st.download_button(
        "💾 Descargar Respaldo JSON",
        data=json.dumps(respaldo, ensure_ascii=False, indent=2),
        file_name=f"SVI_{datetime.now().strftime('%H%M')}.json",
        mime="application/json"
    )
