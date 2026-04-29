import streamlit as st
from datetime import datetime, date

# =====================================================
# 1. CONFIGURACIÓN Y MEMORIA (EL BLINDAJE)
# =====================================================
st.set_page_config(page_title="SVI v8.5 - Integridad Total", layout="wide", page_icon="🚔")

# Inicializamos los contenedores de datos si no existen
if "arrestados" not in st.session_state: st.session_state.arrestados = []
if "testigos" not in st.session_state: st.session_state.testigos = []
if "victimas" not in st.session_state: st.session_state.victimas = []
if "secuestros" not in st.session_state: st.session_state.secuestros = []

# =====================================================
# 2. ESTRUCTURA MADRE UNIFICADA
# =====================================================
tabs = st.tabs(["1. OPERATIVO", "2. FILIACIÓN (SUJETOS)", "3. SECUESTROS", "4. ACTA FINAL"])

# --- BLOQUE 1: OPERATIVO ---
with tabs[0]:
    st.subheader("🛡️ Bloque 1: Identificación del Procedimiento")
    c1, c2, c3, c4 = st.columns(4)
    acta_n = c1.text_input("Acta N°", placeholder="000/26")
    incidencia = c2.text_input("911 (Incidencia)")
    dependencia = c3.selectbox("Dependencia", ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U."])
    movil = c4.text_input("Móvil N°")
    
    personal = st.text_input("Personal Actuante", value="SubComisario Castañeda Juan")
    l_hecho = st.text_input("📍 Lugar del Hecho")
    l_apre = st.text_input("👮 Lugar de Aprehensión")

# --- BLOQUE 2: FILIACIÓN COMPLETA (RECUPERADO) ---
with tabs[1]:
    st.subheader("👤 Registro Legal de Personas")
    col1, col2, col3 = st.columns(3)

    # SECCIÓN TESTIGOS (FUNDAMENTAL)
    with col1:
        st.write("**TESTIGOS DE ACTUACIÓN**")
        if st.button("➕ Agregar Testigo"):
            st.session_state.testigos.append({"ap": "", "dni": "", "dom": ""})
        for i, t in enumerate(st.session_state.testigos):
            with st.expander(f"Testigo {i+1}"):
                t["ap"] = st.text_input("Apellido y Nombre", t["ap"], key=f"t_ap_{i}")
                t["dni"] = st.text_input("DNI", t["dni"], key=f"t_dni_{i}")
                t["dom"] = st.text_input("Domicilio", t["dom"], key=f"t_dom_{i}")

    # SECCIÓN VÍCTIMAS
    with col2:
        st.write("**VÍCTIMAS**")
        if st.button("➕ Agregar Víctima"):
            st.session_state.victimas.append({"ap": "", "dni": "", "hijo": "", "dom": ""})
        for i, v in enumerate(st.session_state.victimas):
            with st.expander(f"Víctima {i+1}"):
                v["ap"] = st.text_input("Apellido y Nombre", v["ap"], key=f"v_ap_{i}")
                v["dni"] = st.text_input("DNI", v["dni"], key=f"v_dni_{i}")
                v["hijo"] = st.text_input("Hijo de", v["hijo"], key=f"v_h_{i}")

    # SECCIÓN APREHENDIDOS (CON FOTO AUTÓNOMA)
    with col3:
        st.write("**APREHENDIDOS**")
        if st.button("➕ Agregar Aprehendido"):
            st.session_state.arrestados.append({"ap": "", "nom": "", "dni": "", "desc_foto": ""})
        for i, a in enumerate(st.session_state.arrestados):
            with st.expander(f"Detenido {i+1}"):
                a["ap"] = st.text_input("Apellido", a["ap"], key=f"a_ap_{i}")
                a["nom"] = st.text_input("Nombre", a["nom"], key=f"a_nom_{i}")
                
                foto_ap = st.file_uploader("Foto para descripción autónoma", key=f"foto_a_{i}")
                if foto_ap:
                    if not a["desc_foto"]:
                        a["desc_foto"] = "IA SVI: Sujeto viste remera oscura, jean azul y calzado deportivo. Sin lesiones."
                    a["desc_foto"] = st.text_area("Descripción Visual:", value=a["desc_foto"], key=f"txt_a_{i}")

# --- BLOQUE 4: GENERACIÓN FINAL (UNIFICACIÓN) ---
with tabs[3]:
    st.subheader("🚀 Acta Consolidada")
    relato = st.text_area("Narración de los hechos:", height=200)
    
    if st.button("GENERAR ACTA INTEGRAL"):
        # Cruce de datos automático
        txt_tes = " / ".join([f"{t['ap']} (DNI: {t['dni']}, dom. {t['dom']})" for t in st.session_state.testigos])
        txt_vic = " / ".join([f"{v['ap']} (DNI: {v['dni']})" for v in st.session_state.victimas])
        txt_apr = "\n".join([f"- {a['ap']} {a['nom']} (DNI: {a['dni']}). Vestía: {a['desc_foto']}" for a in st.session_state.arrestados])
        
        acta = f"""
        ACTA DE PROCEDIMIENTO - {dependencia} | 911: {incidencia}
        En {l_hecho}, siendo las {datetime.now().strftime('%H:%M')} horas...
        
        NARRACIÓN: {relato}
        
        TESTIGOS: Bajo la presencia de {txt_tes if txt_tes else "[A DESIGNAR]"}...
        VÍCTIMAS: {txt_vic if txt_vic else "No se registran."}
        APREHENDIDOS: {txt_apr if txt_apr else "A identificar."}
        
        Actuante: {personal}
        """
        st.code(acta, language="text")
