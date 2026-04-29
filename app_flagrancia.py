import streamlit as st
import json
from datetime import datetime

# =====================================================
# 1. CONFIGURACIÓN Y ESTÉTICA
# =====================================================
st.set_page_config(page_title="SVI - Sistema de Gestión", layout="wide")

# =====================================================
# 2. INICIALIZACIÓN DE MEMORIA (Session State)
# =====================================================
# Definimos las llaves exactas que debe tener el JSON
if "data_operativa" not in st.session_state:
    st.session_state.data_operativa = {
        "nro_acta": "", "incidencia": "", "dependencia": "CRE PÉREZ",
        "dependencia_otra": "", "movil": "", "refuerzo": "", 
        "l_hecho": "", "l_apre": "", "relato": "",
        "personal": "Sub Comisario CASTAÑEDA Juan"
    }

# =====================================================
# 3. SIDEBAR - CARGA Y DESCARGA
# =====================================================
with st.sidebar:
    st.title("📂 Central de Recepción")
    st.subheader("📥 Cargar Trabajo de Calle")
    archivo_subido = st.file_uploader("Subir archivo JSON", type=["json"])
    
    if archivo_subido is not None:
        try:
            datos_nuevos = json.loads(archivo_subido.getvalue().decode("utf-8"))

            # Actualizamos solo las llaves existentes para no romper la estructura
            for k in st.session_state.data_operativa.keys():
                if k in datos_nuevos:
                    st.session_state.data_operativa[k] = datos_nuevos[k]

            st.success("✅ Datos sincronizados.")

        except Exception as e:
            st.error(f"Error: {e}")

    st.divider()
    # Generar JSON para descargar
    data_json = json.dumps(st.session_state.data_operativa, indent=4)
    st.download_button(
        label="💾 GUARDAR ACTA (JSON)",
        data=data_json,
        file_name=f"acta_{st.session_state.data_operativa.get('nro_acta', 'SVI')}.json",
        mime="application/json",
        use_container_width=True
    )

# =====================================================
# 4. CUERPO - BLOQUE 1 CON LLAVES (KEYS)
# =====================================================
st.title("🚔 ACTA DE PROCEDIMIENTO UR II _(S.I.V.)")

tabs = st.tabs(["1. Inicio", "2. Arrestado", "3. Victima", "4. Testigo"])

with tabs[0]:
    st.subheader("🛡️ Identificación Administrativa y Operativa")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Usamos la memoria directamente para los valores
    st.session_state.data_operativa["nro_acta"] = col1.text_input("Nro. de Acta", value=st.session_state.data_operativa["nro_acta"])
    st.session_state.data_operativa["incidencia"] = col2.text_input("Nro. Incidencia", value=st.session_state.data_operativa["incidencia"])
    
    # Dependencia
    deps = ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M.", "OTRO"]
    idx = deps.index(st.session_state.data_operativa["dependencia"]) if st.session_state.data_operativa["dependencia"] in deps else 0
    st.session_state.data_operativa["dependencia"] = col3.selectbox("Dependencia", deps, index=idx)
    
    st.session_state.data_operativa["movil"] = col4.text_input("Móvil", value=st.session_state.data_operativa["movil"])

    # LUGARES (Críticos)
    st.session_state.data_operativa["l_hecho"] = st.text_input("📍 Lugar del Hecho", value=st.session_state.data_operativa["l_hecho"])
    st.session_state.data_operativa["l_apre"] = st.text_input("👤 Lugar de Aprehensión", value=st.session_state.data_operativa["l_apre"])

    st.divider()
    st.subheader("📝 Relato")
    st.session_state.data_operativa["relato"] = st.text_area("Narración:", value=st.session_state.data_operativa["relato"], height=200)

    # Botón de copiado
    if st.button("🚀 COPIAR PARA IA"):
        prompt = f"Actuá como asistente policial... Redactá en 1ra persona plural: {st.session_state.data_operativa['relato']}"
        st.components.v1.html(f"<script>navigator.clipboard.writeText(`{prompt}`);</script>", height=0)
        st.success("Copiado.")
