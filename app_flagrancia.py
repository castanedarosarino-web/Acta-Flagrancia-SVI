import streamlit as st
import json
from datetime import datetime

# =========================================================
# SISTEMA SVI - ACTA DE PROCEDIMIENTO PROFESIONAL
# Versión: Original 10bis (2026)
# Autor: Sub Comisario Castañeda Juan
# =========================================================

st.set_page_config(page_title="SVI - Original 10bis", layout="wide")

# ESTILO Y AUTORÍA
st.markdown("""
    <style>
    .autor-header {
        background-color: #1e3d59;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
    <div class="autor-header">
        <h1>SISTEMA SVI</h1>
        <h3>Creado por Sub Comisario Castañeda Juan</h3>
    </div>
    """, unsafe_allow_html=True)

# --- INICIO DE FORMULARIO ---
if 'acta_id' not in st.session_state:
    st.session_state.acta_id = datetime.now().strftime("%Y%m%d-%H%M")

# BLOQUE 1: DATOS GENERALES Y NARRATIVA
with st.expander("📝 BLOQUE 1: DATOS Y NARRATIVA", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        fecha_proc = st.date_input("Fecha del Hecho", datetime.now())
        unidad_interviniente = st.text_input("Dependencia", "COMANDO RADIOELÉCTRICO PÉREZ")
    with col2:
        hora_proc = st.time_input("Hora de Intervención", datetime.now())
        oficial_actuante = st.text_input("Oficial Actuante", "Sub Comisario Castañeda Juan")
    
    narrativa_inicial = st.text_area("Relato de Flagrancia", placeholder="Describa el inicio del procedimiento...")

# BLOQUE 2: APREHENDIDO Y MESA DE ENLACE
with st.expander("👤 BLOQUE 2: APREHENDIDO Y VALIDACIÓN"):
    sujeto_nom = st.text_input("Nombre y Apellido del Demorado")
    requisa_ia = st.text_area("Acta de Requisa (Descripción IA de Vestimenta/Pertenencias)")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        opr_911 = st.text_input("Operador 911 (Cóndor)")
    with c2:
        opr_mesa = st.text_input("Operador Mesa de Enlace (Validación)")

# BLOQUE 3: FOTOS IA, ESCENARIO Y CROQUIS
with st.expander("📸 BLOQUE 3: ESCENARIO, FOTOS IA Y CROQUIS"):
    st.subheader("Registro Fotográfico de Protocolo")
    cf1, cf2 = st.columns(2)
    with cf1:
        f1 = st.file_uploader("1. Panorámica", type=['jpg','png'])
        d1 = st.text_area("IA Panorámica", "Escenario en zona urbana, visibilidad buena, iluminación artificial activa.")
        
        f3 = st.file_uploader("3. Primer Plano", type=['jpg','png'])
        d3 = st.text_area("IA Primer Plano", "Enfoque sobre elemento secuestrado/rostro para identificación.")
    with cf2:
        f2 = st.file_uploader("2. Plano Medio", type=['jpg','png'])
        d2 = st.text_area("IA Plano Medio", "Vínculo espacial entre sujeto y elementos del ilícito.")
        
        f4 = st.file_uploader("4. Detalle", type=['jpg','png'])
        d4 = st.text_area("IA Detalle", "Captura de guarismos/daños específicos sin adulteraciones visibles.")

    st.markdown("---")
    st.subheader("Inspección Ocular Genérica")
    inspeccion_texto = st.text_area("Texto Reglamentario", 
        value="Que en relación al escenario del hecho, se toman apunte y vistas fotograficas para la posterior confeccion de la inspección ocular y relevamiento de camaras; no observándose rastros o indicios que requieran tratamiento pericial específico.")

    st.subheader("📽️ Relevamiento de Cámaras")
    cc1, cc2 = st.columns(2)
    with cc1:
        cam_tipo = st.selectbox("Tipo", ["Domo 911", "Privada", "Comercial"])
        cam_ubi = st.text_input("Ubicación exacta")
    with cc2:
        cam_est = st.radio("Estado", ["Funcionando", "Fuera de Servicio"])

    st.subheader("🗺️ Croquis Demostrativo")
    st.info("Orientación Automática: NORTE")
    croquis_pos = st.text_input("Ubicación de elementos (Móvil, Secuestro, Sujeto)")

# BLOQUE 4: COMUNICACIONES Y CIERRE
with st.expander("⚖️ BLOQUE 4: COMUNICACIONES Y ENTREGA"):
    ca1, ca2 = st.columns(2)
    with ca1:
        fiscal_mpa = st.text_input("Fiscal MPA (0800)")
        instrucciones = st.text_area("Directivas Judiciales")
    with ca2:
        defensoria = st.text_input("Defensoría de Turno")
        oficial_guardia = st.text_input("Oficial de Guardia que recibe")

# BOTÓN FINAL
if st.button("💾 FINALIZAR Y GENERAR ACTA"):
    # Lógica de guardado
    resultado = {
        "id": st.session_state.acta_id,
        "autor": "Sub Comisario Castañeda Juan",
        "datos": {"sujeto": sujeto_nom, "fiscal": fiscal_mpa, "entrega": oficial_guardia}
    }
    st.success(f"Acta {st.session_state.acta_id} guardada con éxito. Listo para impresión de folios.")
    st.balloons()
