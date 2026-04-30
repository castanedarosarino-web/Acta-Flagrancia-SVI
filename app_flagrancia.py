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

# =====================================================
# DATOS BASE
# =====================================================
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
        "personal": "Sub Comisario CASTAÑEDA Juan",
        "colaboraciones": []
    }

if "relato_usuario" not in st.session_state:
    st.session_state.relato_usuario = st.session_state.data_operativa.get("relato", "")

def cargar_en_estado(datos, acumular_relato=False):
    campos = [
        "nro_acta", "incidencia", "dependencia", "dependencia_otra",
        "movil", "refuerzo", "l_hecho", "l_apre", "personal"
    ]

    for campo in campos:
        if datos.get(campo):
            st.session_state.data_operativa[campo] = datos[campo]

    relato_nuevo = datos.get("relato", "")

    if relato_nuevo:
        if acumular_relato and st.session_state.data_operativa.get("relato"):
            st.session_state.data_operativa["relato"] += "\n\n--- APORTE DE COLABORACIÓN ---\n" + relato_nuevo
        else:
            st.session_state.data_operativa["relato"] = relato_nuevo

        st.session_state.relato_usuario = st.session_state.data_operativa["relato"]

    if acumular_relato:
        st.session_state.data_operativa["colaboraciones"].append(datos)

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.title("📂 Central de Recepción")
    st.markdown("### **Creado por Sub Comisario CASTAÑEDA Juan**")

    st.divider()

    modo = st.radio(
        "Modo de trabajo",
        ["Colaborador", "Central / Actero"]
    )

    st.divider()

    if modo == "Central / Actero":
        st.subheader("📥 Importar Colaboración")
        archivo_colab = st.file_uploader(
            "Subir colaboración JSON",
            type=["json"],
            key="importar_colaboracion"
        )

        if archivo_colab is not None:
            try:
                datos_colab = json.loads(archivo_colab.getvalue().decode("utf-8"))
                cargar_en_estado(datos_colab, acumular_relato=True)
                st.success("✅ Colaboración incorporada al acta.")
            except Exception as e:
                st.error(f"Error al importar colaboración: {e}")

    else:
        st.subheader("👮 Modo Colaborador")
        st.info("Complete el Bloque 1 y exporte su colaboración.")

    st.divider()

    nombre_base = st.session_state.data_operativa.get("nro_acta", "SVI") or "SVI"
    movil_base = st.session_state.data_operativa.get("movil", "MOVIL") or "MOVIL"

    data_exportar = dict(st.session_state.data_operativa)
    data_exportar["relato"] = st.session_state.get(
        "relato_usuario",
        st.session_state.data_operativa.get("relato", "")
    )

    data_json = json.dumps(
        data_exportar,
        indent=4,
        ensure_ascii=False
    )

    if modo == "Colaborador":
        st.download_button(
            label="💾 EXPORTAR COLABORACIÓN",
            data=data_json,
            file_name=f"colaboracion_{nombre_base}_{movil_base}.json",
            mime="application/json",
            use_container_width=True
        )
    else:
        st.download_button(
            label="💾 GUARDAR ACTA FINAL",
            data=data_json,
            file_name=f"acta_final_{nombre_base}.json",
            mime="application/json",
            use_container_width=True
        )

# =====================================================
# CUERPO PRINCIPAL - BLOQUE 1
# =====================================================
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

    n_acta = c1.text_input(
        "Nro. de Acta",
        value=st.session_state.data_operativa["nro_acta"]
    )

    n_incidencia = c2.text_input(
        "Nro. Incidencia (911)",
        value=st.session_state.data_operativa["incidencia"]
    )

    dep_opciones = ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M.", "OTRO"]
    dep_actual = st.session_state.data_operativa.get("dependencia", "CRE PÉREZ")
    idx_dep = dep_opciones.index(dep_actual) if dep_actual in dep_opciones else 0

    dep = c3.selectbox(
        "Dependencia",
        dep_opciones,
        index=idx_dep
    )

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

    fecha_proc = c5.date_input(
        "Fecha",
        value=datetime.now()
    )

    hora_proc = c6.time_input(
        "Hora",
        value=datetime.now()
    )

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
        key="relato_usuario",
        height=200
    )

    st.session_state.data_operativa["relato"] = st.session_state.relato_usuario

    if st.button("🚀 COPIAR Y LISTO PARA PEGAR EN IA"):
        st.components.v1.html(
            f"<script>navigator.clipboard.writeText({json.dumps(relato_usuario, ensure_ascii=False)});</script>",
            height=0
        )
        st.success("✅ Copiado al portapapeles.")

    st.session_state.data_operativa.update({
        "nro_acta": n_acta,
        "incidencia": n_incidencia,
        "dependencia": dep,
        "dependencia_otra": dep_otra,
        "movil": n_movil,
        "relato": st.session_state.relato_usuario,
        "personal": personal_actuante,
        "refuerzo": refuerzos,
        "l_hecho": lugar_hecho,
        "l_apre": lugar_apre
    })
