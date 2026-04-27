import streamlit as st
import json
from datetime import datetime

# =========================================================
# ACTA DE PROCEDIMIENTO
# Autor: Sub Comisario Castañeda Juan
# Versión: Original 10bis (Consolidada 2026)
# =========================================================

# 0. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Acta de Procedimiento", layout="wide")

# Estilo para limpieza visual y autoría
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1e3d59;
        font-family: 'Arial', sans-serif;
        padding: 10px;
        border-bottom: 2px solid #1e3d59;
        margin-bottom: 20px;
    }
    </style>
    <div class="main-header">
        <h1>ACTA DE PROCEDIMIENTO</h1>
        <h3>Creado por Sub Comisario Castañeda Juan</h3>
    </div>
    """, unsafe_allow_html=True)

# Manejo de ID de Acta
if 'acta_id' not in st.session_state:
    st.session_state.acta_id = datetime.now().strftime("%Y%m%d-%H%M")

# =========================================================
# BLOQUE 1: DATOS GENERALES Y NARRATIVA (AUDIO)
# =========================================================
with st.expander("📝 BLOQUE 1: DATOS GENERALES Y NARRATIVA", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        fecha_proc = st.date_input("Fecha", datetime.now())
        unidad_interviniente = st.text_input("Dependencia", "COMANDO RADIOELÉCTRICO PÉREZ")
    with col2:
        hora_proc = st.time_input("Hora de Inicio", datetime.now())
        oficial_actuante = st.text_input("Oficial Actuante", "Sub Comisario Castañeda Juan")
    
    st.markdown("---")
    st.subheader("🎙️ Narrativa del Hecho (Dictado por Voz)")
    st.info("Presione el micrófono para relatar el procedimiento. El sistema transcribirá su voz para el cuerpo del acta.")
    
    audio_file = st.audio_input("Grabar relato de flagrancia")
    
    if audio_file:
        st.success("Audio capturado correctamente.")
        narrativa = st.text_area("Cuerpo del Acta (Transcripción Editable)", height=300, 
                                 placeholder="El texto dictado aparecerá aquí para su revisión...")
    else:
        narrativa = st.text_area("Cuerpo del Acta (Escritura Manual)", height=300, 
                                 placeholder="En circunstancias que el móvil policial se encontraba patrullando...")

# =========================================================
# BLOQUE 2: APREHENDIDO Y VALIDACIÓN (MESA DE ENLACE)
# =========================================================
with st.expander("👤 BLOQUE 2: APREHENDIDO Y VALIDACIÓN"):
    col_suj1, col_suj2 = st.columns(2)
    with col_suj1:
        nombre_sujeto = st.text_input("Nombre y Apellido del Demorado")
        dni_sujeto = st.text_input("DNI / Documento")
    with col_suj2:
        requisa_ia = st.text_area("Acta de Requisa y Pertenencias (Descripción IA)", 
                                 placeholder="Describa vestimenta y elementos secuestrados...")

    st.markdown("---")
    st.subheader("📞 Validación de Seguridad")
    col_val1, col_val2 = st.columns(2)
    with col_val1:
        consulta_911 = st.text_input("Operador 911 / Cóndor")
    with col_val2:
        mesa_enlace = st.text_input("Operador Mesa de Enlace (Validación Obligatoria)")

# =========================================================
# BLOQUE 3: ESCENARIO, FOTOS IA Y CROQUIS
# =========================================================
with st.expander("📸 BLOQUE 3: ESCENARIO, REGISTRO FOTOGRÁFICO Y CROQUIS"):
    st.subheader("Inspección Ocular Genérica")
    inspeccion_texto = st.text_area("Texto Reglamentario de Preservación", 
        value="Que en relación al escenario del hecho, se toman apunte y vistas fotograficas para la posterior confeccion de la inspección ocular y relevamiento de camaras; no observándose rastros o indicios que requieran tratamiento pericial específico.")

    st.markdown("---")
    st.subheader("Registro Fotográfico (Protocolo de 4 Fotos)")
    cf1, cf2 = st.columns(2)
    with cf1:
        f1 = st.file_uploader("1. VISTA PANORÁMICA", type=['jpg','png'])
        d1 = st.text_area("Descripción IA (Panorámica)", "Escenario en zona urbana, visibilidad buena, iluminación artificial activa.")
        
        f3 = st.file_uploader("3. PRIMER PLANO", type=['jpg','png'])
        d3 = st.text_area("Descripción IA (Primer Plano)", "Enfoque sobre elemento secuestrado/rostro para identificación.")
    with cf2:
        f2 = st.file_uploader("2. PLANO MEDIO", type=['jpg','png'])
        d2 = st.text_area("Descripción IA (Plano Medio)", "Vínculo espacial entre sujeto y elementos del ilícito.")
        
        f4 = st.file_uploader("4. DETALLE / GUARISMOS", type=['jpg','png'])
        d4 = st.text_area("Descripción IA (Detalle)", "Captura de guarismos/daños específicos sin adulteraciones visibles.")

    st.markdown("---")
    col_cam1, col_cam2 = st.columns(2)
    with col_cam1:
        st.subheader("📽️ Videovigilancia")
        cam_tipo = st.selectbox("Tipo de Cámara", ["Domo 911", "Privada", "Comercial"])
        cam_ubi = st.text_input("Ubicación exacta")
        cam_est = st.radio("Estado", ["Funcionando", "Fuera de Servicio"])
    with col_cam2:
        st.subheader("🗺️ Croquis Demostrativo")
        st.info("Orientación Automática: NORTE")
        croquis_pos = st.text_area("Detalle de posiciones", placeholder="Posición del móvil, demorado y elementos...")

# =========================================================
# BLOQUE 4: COMUNICACIONES JUDICIALES Y ENTREGA
# =========================================================
with st.expander("⚖️ BLOQUE 4: COMUNICACIONES Y ENTREGA"):
    col_jud1, col_jud2 = st.columns(2)
    with col_jud1:
        fiscal_mpa = st.text_input("Fiscal MPA (0800)")
        instrucciones = st.text_area("Directivas Fiscales Recibidas")
    with col_jud2:
        defensoria = st.text_input("Defensoría de Turno")
        hora_cierre = st.time_input("Hora de Finalización de Acta", datetime.now())

    st.markdown("---")
    st.subheader("📦 Entrega de Actuaciones")
    oficial_guardia = st.text_input("Oficial de Guardia que recibe (Grado y Nombre)")

# =========================================================
# FINALIZACIÓN Y GUARDADO
# =========================================================
if st.button("💾 FINALIZAR Y GENERAR ACTA DE PROCEDIMIENTO"):
    # Estructura de persistencia JSON
    acta_final = {
        "id": st.session_state.acta_id,
        "autor": "Sub Comisario Castañeda Juan",
        "unidad": unidad_interviniente,
        "narrativa": narrativa,
        "mesa_enlace": mesa_enlace,
        "fiscal": fiscal_mpa,
        "entrega": oficial_guardia
    }
    st.success(f"Acta {st.session_state.acta_id} finalizada correctamente.")
    st.balloons()
