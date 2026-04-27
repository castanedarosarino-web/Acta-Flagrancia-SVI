import streamlit as st
import json
from datetime import datetime

# =========================================================
# ACTA DE PROCEDIMIENTO
# Autor: Sub Comisario Castañeda Juan
# Versión: Original 10bis (CONSOLIDADO FINAL 2026)
# =========================================================

st.set_page_config(page_title="Acta de Procedimiento", layout="wide")

# ESTILO Y AUTORÍA
st.markdown("""
    <style>
    .main-header { text-align: center; color: #1e3d59; border-bottom: 2px solid #1e3d59; margin-bottom: 20px; }
    .ficha-sujeto { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #1e3d59; margin-bottom: 20px; }
    </style>
    <div class="main-header">
        <h1>ACTA DE PROCEDIMIENTO</h1>
        <h3>Creado por Sub Comisario Castañeda Juan</h3>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# BLOQUE 1: DATOS GENERALES Y NARRATIVA POR AUDIO
# =========================================================
with st.expander("📝 BLOQUE 1: DATOS Y NARRATIVA POR AUDIO", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        fecha_proc = st.date_input("Fecha", datetime.now())
        unidad_interviniente = st.text_input("Dependencia", "COMANDO RADIOELÉCTRICO PÉREZ")
    with col2:
        hora_proc = st.time_input("Hora de Inicio", datetime.now())
        oficial_actuante = st.text_input("Oficial Actuante", "Sub Comisario Castañeda Juan")
    
    st.markdown("---")
    st.subheader("🎙️ Dictado del Acta")
    st.info("Relate el procedimiento. El sistema transcribirá su voz para el cuerpo del acta.")
    
    audio_file = st.audio_input("Grabar relato de flagrancia")
    narrativa_cuerpo = st.text_area("Cuerpo del Acta (Editable)", height=250, 
                                   placeholder="En circunstancias que el móvil policial se encontraba patrullando...")

# =========================================================
# BLOQUE 2: ARRESTADO/S (ESTILO 10 BIS)
# =========================================================
with st.expander("👤 BLOQUE 2: ARRESTADO/S", expanded=True):
    cant_sujetos = st.number_input("Cantidad de sujetos:", min_value=1, value=1, step=1)
    
    for i in range(int(cant_sujetos)):
        st.markdown(f'<div class="ficha-sujeto"><h4>[ 👤 FICHA IDENTIFICATORIA - SUJETO N° {i+1} ]</h4>', unsafe_allow_html=True)
        
        # A. REGISTRO FOTOGRÁFICO E IA
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            foto_sujeto = st.camera_input(f"Capturar Rostro Sujeto {i+1}")
        with col_f2:
            st.info("Descripción IA de Vestimenta")
            desc_ia_vest = st.text_area(f"Descripción IA Sujeto {i+1}:", 
                value="Masculino, de contextura robusta, viste remera negra con logo blanco, pantalón tipo jogger gris y zapatillas deportivas...", height=100)

        # B. IDENTIDAD
        st.markdown("##### 🆔 IDENTIDAD (ESTILO 10 BIS)")
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            dni = st.text_input(f"DNI Sujeto {i+1}")
            apellido = st.text_input(f"Apellido Sujeto {i+1}")
            est_civil = st.selectbox("Estado Civil", ["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a"], key=f"ec_{i}")
        with c2:
            apodo = st.text_input(f"Apodo / Alias Sujeto {i+1}")
            nombre = st.text_input(f"Nombre Sujeto {i+1}")
            f_nac = st.date_input("Fecha de Nacimiento", value=datetime(1998, 5, 15), key=f"fn_{i}")
        with c3:
            edad = datetime.now().year - f_nac.year
            st.metric("Edad", f"{edad}")

        c4, c5 = st.columns(2)
        with c4:
            padres = st.text_input(f"Hijo de (Padre y Madre)", key=f"pa_{i}")
            profesion = st.text_input("Profesión", key=f"pr_{i}")
        with c5:
            domicilio = st.text_input("Domicilio", key=f"dom_{i}")
            instruccion = st.radio("Sabe leer/escribir:", ["SI", "NO"], horizontal=True, key=f"ins_{i}")

        # C. CONSULTA CÓNDOR / 911
        st.markdown("##### 📞 CONSULTA SISTEMA CÓNDOR / 911")
        col_911_1, col_911_2 = st.columns(2)
        with col_911_1:
            op_911 = st.text_input("Operador 911 Nro:", key=f"op9_{i}")
        with col_911_2:
            res_911 = st.selectbox("Resultado:", ["NEGATIVO", "POSITIVO (Captura/Paradero)"], key=f"res9_{i}")
        if "POSITIVO" in res_911:
            st.text_area("Detalle del Oficio / Juzgado / Causa:", key=f"det9_{i}")

        # D. REQUISA PERSONAL (ART. 268 CPP)
        st.markdown("##### 🔍 REQUISA PERSONAL (ART. 268 CPP)")
        res_req = st.radio("Resultado:", ["NEGATIVA", "POSITIVA"], horizontal=True, key=f"rreq_{i}")
        if res_req == "POSITIVA":
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                ocultamiento = st.text_input("Lugar de ocultamiento:", placeholder="Ej: Cintura lado derecho")
                elemento = st.text_input("Elemento Secuestrado:", placeholder="Ej: Pistola cal. 9mm")
            with col_r2:
                foto_hallazgo = st.camera_input(f"Capturar Hallazgo Sujeto {i+1}")

            testigos = st.radio("¿Hay Testigos?", ["SI", "NO (URGENCIA)"], horizontal=True, key=f"test_{i}")
            if testigos == "NO (URGENCIA)":
                urgencia = st.text_input("Causa de Urgencia:", placeholder="Ej: Zona hostil / Agresión de terceros")
        
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# BLOQUE 3: ESCENARIO Y FOTOS IA
# =========================================================
with st.expander("📸 BLOQUE 3: ESCENARIO E INSPECCIÓN OCULAR"):
    st.text_area("Inspección Genérica (Texto Reglamentario)", 
                 value="Que en relación al escenario del hecho, se toman apunte y vistas fotograficas para la posterior confeccion de la inspección ocular y relevamiento de camaras; no observándose rastros o indicios que requieran tratamiento pericial específico.")
    
    st.subheader("Protocolo de 4 Fotos")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.file_uploader("1. VISTA PANORÁMICA")
        st.text_area("Descripción IA (Panorámica)", "Escenario en zona urbana, visibilidad buena...")
    with col_f2:
        st.file_uploader("2. PLANO MEDIO (Vínculo)")
        st.text_area("Descripción IA (Plano Medio)", "Vínculo espacial entre sujeto y elemento...")

# =========================================================
# BLOQUE 4: COMUNICACIONES Y ENTREGA
# =========================================================
with st.expander("⚖️ BLOQUE 4: COMUNICACIONES Y CIERRE"):
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        st.text_input("Fiscal MPA (0800)")
        st.text_area("Directivas Judiciales")
    with col_j2:
        st.text_input("Defensoría de Turno")
        st.text_input("Oficial de Guardia que recibe (Grado y Nombre)")

if st.button("💾 FINALIZAR Y GENERAR ACTA"):
    st.success("Acta finalizada con éxito.")
    st.balloons()
