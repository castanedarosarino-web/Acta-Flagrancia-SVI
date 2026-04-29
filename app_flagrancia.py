import streamlit as st
from datetime import datetime, date

# CONFIGURACIÓN DE PÁGINA Y ESTADO
st.set_page_config(page_title="SVI - Versión Integral", layout="wide", page_icon="🚔")

# INICIALIZACIÓN DE MEMORIA (Los cimientos que no se tocan)
for key in ["arrestados", "victimas", "testigos", "relato_bruto"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key != "relato_bruto" else ""

# =====================================================
# ESTRUCTURA MADRE UNIFICADA
# =====================================================
tabs = st.tabs(["1. DATOS OPERATIVOS", "2. FILIACIÓN LEGAL", "3. RELATO E IA"])

with tabs[0]:
    st.subheader("🛡️ Bloque 1: Identificación del Procedimiento")
    c1, c2, c3, c4 = st.columns(4)
    acta_n = c1.text_input("Acta N°", placeholder="000/26")
    incidencia = c2.text_input("911 (Incidencia)")
    dependencia = c3.selectbox("Dependencia", ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U."])
    movil = c4.text_input("Móvil N°")

    personal = st.text_input("Personal Actuante", value="SubComisario Castañeda Juan")
    refuerzo = st.text_input("Refuerzos / Apoyo")
    
    l_hecho = st.text_input("📍 Lugar del Hecho")
    l_apre = st.text_input("👮 Lugar de Aprehensión")

with tabs[1]:
    st.subheader("👤 Bloque 2: Registro de Personas (Carga Única)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**DETENIDOS**")
        if st.button("➕ Aprehendido"): st.session_state.arrestados.append({"ap": "", "nom": "", "dni": "", "hijo": "", "dom": ""})
        for i, a in enumerate(st.session_state.arrestados):
            with st.expander(f"Aprehendido {i+1}"):
                a["ap"] = st.text_input("Apellido", a["ap"], key=f"ap_{i}")
                a["nom"] = st.text_input("Nombre", a["nom"], key=f"nom_{i}")
                a["dni"] = st.text_input("DNI", a["dni"], key=f"dni_{i}")
                a["hijo"] = st.text_input("Hijo de", a["hijo"], key=f"h_{i}")

    with col2:
        st.write("**VÍCTIMAS**")
        if st.button("➕ Víctima"): st.session_state.victimas.append({"ap": "", "dni": ""})
        for i, v in enumerate(st.session_state.victimas):
            with st.expander(f"Víctima {i+1}"):
                v["ap"] = st.text_input("Apellido y Nombre", v["ap"], key=f"v_{i}")
                v["dni"] = st.text_input("DNI", v["dni"], key=f"vd_{i}")

    with col3:
        st.write("**TESTIGOS**")
        if st.button("➕ Testigo"): st.session_state.testigos.append({"ap": "", "dni": "", "dom": ""})
        for i, t in enumerate(st.session_state.testigos):
            with st.expander(f"Testigo {i+1}"):
                t["ap"] = st.text_input("Apellido y Nombre", t["ap"], key=f"t_{i}")
                t["dni"] = st.text_input("DNI", t["dni"], key=f"td_{i}")
                t["dom"] = st.text_input("Domicilio", t["dom"], key=f"tm_{i}")

with tabs[2]:
    st.subheader("✍️ Bloque 3: Pulido de Acta")
    relato = st.text_area("Narración rápida:", height=200)
    
    if st.button("🚀 GENERAR ACTA FINAL"):
        det_str = ", ".join([f"{a['ap']} {a['nom']} (DNI: {a['dni']}, hijo de {a['hijo']})" for a in st.session_state.arrestados])
        tes_str = ", ".join([f"{t['ap']} (DNI: {t['dni']}, dom. {t['dom']})" for t in st.session_state.testigos])
        
        acta = f"""
        PROCEDIMIENTO: {dependencia} | ACTA: {acta_n} | 911: {incidencia}
        PERSONAL: {personal} | MÓVIL: {movil} | APOYO: {refuerzo}
        LUGAR DEL HECHO: {l_hecho}
        
        SÍNTESIS: {relato}
        
        ACTUACIÓN: Ante la presencia del testigo {tes_str if tes_str else "[A DESIGNAR]"}, 
        se procede en {l_apre} a la demora de: {det_str if det_str else "[SIN DATOS]"}.
        """
        st.code(acta, language="text")
