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

with st.sidebar:
    st.title("📂 Central de Recepción")
    st.markdown("### **Creado por Sub Comisario CASTAÑEDA Juan**")

    st.divider()

    st.subheader("📥 Cargar Datos Administrativos")
    archivo_json = st.file_uploader("Subir archivo JSON", type=["json"], key="json_admin")

    if archivo_json is not None:
        try:
            datos_nuevos = json.loads(archivo_json.getvalue().decode("utf-8"))

            # JSON SOLO PARA DATOS ADMINISTRATIVOS
            campos_admin = [
                "nro_acta",
                "incidencia",
                "dependencia",
                "dependencia_otra",
                "movil",
                "refuerzo",
                "l_hecho",
                "l_apre",
                "personal"
            ]

            for campo in campos_admin:
                if campo in datos_nuevos:
                    st.session_state.data_operativa[campo] = datos_nuevos[campo]

            st.success("✅ Datos administrativos cargados.")

        except Exception as e:
            st.error(f"Error al cargar JSON: {e}")

    st.divider()

    st.subheader("📝 Cargar Relato")
    archivo_txt = st.file_uploader("Subir relato TXT", type=["txt"], key="txt_relato")

    if archivo_txt is not None:
        try:
            texto_relato = archivo_txt.getvalue().decode("utf-8")
            st.session_state.data_operativa["relato"] = texto_relato
            st.success("✅ Relato cargado desde TXT.")

        except Exception as e:
            st.error(f"Error al cargar TXT: {e}")

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
