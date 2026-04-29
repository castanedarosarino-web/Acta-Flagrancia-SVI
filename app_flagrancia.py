import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="SVI - Acta de Procedimiento", layout="wide", page_icon="🚔")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextInput { margin-top: -15px; }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if "data_operativa" not in st.session_state:
    st.session_state.data_operativa = {
        "nro_acta": "",
        "incidencia": "",
        "dependencia": "CRE PÉREZ",
        "dependencia_otra": "",
        "movil": "",
        "refuerzo": "",
        "l_hecho": "",
        "l_apre": "",
        "relato": "",
        "personal": "Sub Comisario CASTAÑEDA Juan"
    }

def normalizar_clave(clave):
    return str(clave).strip().lower().replace("_", " ").replace("-", " ")

def aplanar_json(data, salida=None):
    if salida is None:
        salida = {}

    if isinstance(data, dict):
        for k, v in data.items():
            salida[normalizar_clave(k)] = v
            if isinstance(v, (dict, list)):
                aplanar_json(v, salida)

    elif isinstance(data, list):
        for item in data:
            aplanar_json(item, salida)

    return salida

def cargar_datos_json(datos):
    plano = aplanar_json(datos)

    campos = {
        "nro_acta": ["nro acta", "numero acta", "número acta", "acta"],
        "incidencia": ["incidencia", "nro incidencia", "numero incidencia", "número incidencia", "911"],
        "dependencia": ["dependencia", "unidad", "cre"],
        "movil": ["movil", "móvil", "nro movil", "nro móvil", "numero movil", "número móvil"],
        "refuerzo": ["refuerzo", "apoyo", "moviles apoyo", "móviles apoyo"],
        "l_hecho": ["l hecho", "lugar hecho", "lugar del hecho", "domicilio hecho"],
        "l_apre": [
            "l apre", "lugar apre", "lugar aprehension", "lugar aprehensión",
            "lugar de aprehension", "lugar de aprehensión", "domicilio aprehension"
        ],
        "relato": [
            "relato", "relato hechos", "relato de los hechos",
            "narracion", "narración", "narracion de los hechos",
            "narración de los hechos", "hechos", "descripcion",
            "descripción", "circunstancias", "procedimiento",
            "texto", "detalle", "observaciones"
        ],
        "personal": ["personal", "personal actuante", "actuante"]
    }

    for destino, variantes in campos.items():
        for variante in variantes:
            clave_normal = normalizar_clave(variante)
            if clave_normal in plano and plano[clave_normal] not in [None, ""]:
                st.session_state.data_operativa[destino] = str(plano[clave_normal])
                break

with st.sidebar:
    st.title("📂 Central de Recepción")
    st.markdown("### **Creado por Sub Comisario CASTAÑEDA Juan**")

    st.divider()
    st.subheader("📥 Cargar Trabajo de Calle")
    archivo_subido = st.file_uploader("Subir archivo JSON", type=["json"])

    if archivo_subido is not None:
        try:
            datos_nuevos = json.loads(archivo_subido.getvalue().decode("utf-8"))
            cargar_datos_json(datos_nuevos)
            st.success("✅ Datos del móvil integrados.")

            with st.expander("🔍 Ver claves detectadas del JSON"):
                st.json(aplanar_json(datos_nuevos))

        except Exception as e:
            st.error(f"Error al cargar: {e}")

    st.divider()

    data_json = json.dumps(st.session_state.data_operativa, indent=4, ensure_ascii=False)

    st.download_button(
        label="💾 GUARDAR ACTA (JSON)",
        data=data_json,
        file_name=f"acta_{st.session_state.data_operativa.get('nro_acta', 'SVI')}.json",
        mime="application/json",
        use_container_width=True
    )

st.title("🚔 ACTA DE PROCEDIMIENTO UR II _(S.I.V.)")
st.subheader("Creado por Sub Comisario CASTAÑEDA Juan")

tabs = st.tabs([
    "1. Inicio (Datos Base)",
    "2. Arrestado",
    "3. Victima",
    "4. Testigo",
    "5. Consulta",
    "6. Inspección",
    "7. Secuestros",
    "8. Cierre"
])

with tabs[0]:
    st.subheader("🛡️ Identificación Administrativa y Operativa")

    c1, c2, c3, c4 = st.columns(4)

    n_acta = c1.text_input("Nro. de Acta", value=st.session_state.data_operativa["nro_acta"])
    n_incidencia = c2.text_input("Nro. Incidencia (911)", value=st.session_state.data_operativa["incidencia"])

    dep_opciones = ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M.", "OTRO"]
    dep_actual = st.session_state.data_operativa.get("dependencia", "CRE PÉREZ")
    idx_dep = dep_opciones.index(dep_actual) if dep_actual in dep_opciones else 0

    dep = c3.selectbox("Dependencia", dep_opciones, index=idx_dep)

    if dep == "OTRO":
        dep_otra = c4.text_input(
            "Especifique Dependencia",
            value=st.session_state.data_operativa.get("dependencia_otra", "")
        )
        n_movil = st.text_input(
            "Nro. de Móvil",
            value=st.session_state.data_operativa.get("movil", "")
        )
    else:
        n_movil = c4.text_input(
            "Nro. de Móvil",
            value=st.session_state.data_operativa.get("movil", "")
        )
        dep_otra = ""

    personal_actuante = st.text_input(
        "Personal Actuante",
        value=st.session_state.data_operativa.get("personal", "Sub Comisario CASTAÑEDA Juan")
    )

    refuerzos = st.text_input(
        "Refuerzo (Móviles/Personal de apoyo)",
        value=st.session_state.data_operativa.get("refuerzo", "")
    )

    c5, c6 = st.columns(2)
    fecha_proc = c5.date_input("Fecha", value=datetime.now())
    hora_proc = c6.time_input("Hora", value=datetime.now())

    lugar_hecho = st.text_input(
        "📍 Lugar del Hecho",
        value=st.session_state.data_operativa.get("l_hecho", "")
    )

    lugar_apre = st.text_input(
        "👤 Lugar de Aprehensión",
        value=st.session_state.data_operativa.get("l_apre", "")
    )

    st.divider()
    st.subheader("📝 Relato Circunstanciado")

    relato_usuario = st.text_area(
        "Narración de los hechos:",
        value=st.session_state.data_operativa.get("relato", ""),
        height=200
    )

    prompt_ia = relato_usuario

    if st.button("🚀 COPIAR Y LISTO PARA PEGAR EN IA"):
        st.components.v1.html(
            f"<script>navigator.clipboard.writeText(`{prompt_ia}`);</script>",
            height=0
        )
        st.success("✅ Copiado al portapapeles.")

    st.session_state.data_operativa.update({
        "nro_acta": n_acta,
        "incidencia": n_incidencia,
        "dependencia": dep,
        "dependencia_otra": dep_otra,
        "movil": n_movil,
        "relato": relato_usuario,
        "personal": personal_actuante,
        "refuerzo": refuerzos,
        "l_hecho": lugar_hecho,
        "l_apre": lugar_apre
    })
