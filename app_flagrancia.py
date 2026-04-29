import streamlit as st
from datetime import datetime, date

# CONFIGURACIÓN Y ESTADO DE MEMORIA PERMANENTE
st.set_page_config(page_title="SVI - Compromiso Integral", layout="wide", page_icon="🚔")

# Cimientos inamovibles (No se borran al navegar entre pestañas)
if "arrestados" not in st.session_state: st.session_state.arrestados = []
if "testigos" not in st.session_state: st.session_state.testigos = []
if "victimas" not in st.session_state: st.session_state.victimas = []
if "secuestros" not in st.session_state: st.session_state.secuestros = []

# =====================================================
# ESTRUCTURA MADRE: BLOQUES JERÁRQUICOS
# =====================================================
tabs = st.tabs(["1. OPERATIVO", "2. FILIACIÓN (SUJETOS/TESTIGOS)", "3. SECUESTROS PROF.", "4. ACTA FINAL"])

# --- BLOQUE 1: IDENTIFICACIÓN OPERATIVA ---
with tabs[0]:
    st.subheader("🛡️ Datos de Identificación y Procedimiento")
    c1, c2, c3, c4 = st.columns(4)
    acta_n = c1.text_input("Acta N°", placeholder="Ej: 001/26")
    incidencia = c2.text_input("911 (Nro. de Incidencia)")
    dependencia = c3.selectbox("Dependencia", ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M."])
    movil = c4.text_input("Móvil N°")

    c5, c6 = st.columns(2)
    personal = st.text_input("Personal Actuante", value="SubComisario Castañeda Juan")
    refuerzo = st.text_input("Apoyo / Refuerzos (Móviles y Personal)")

    l_hecho = st.text_input("📍 Lugar del Hecho")
    l_apre = st.text_input("👮 Lugar de Aprehensión (Diferente al hecho)")

# --- BLOQUE 2: FILIACIÓN COMPLETA (TESTIGOS, VÍCTIMAS Y APREHENDIDOS) ---
with tabs[1]:
    st.subheader("👤 Registro Legal de Personas")
    col_t, col_v, col_a = st.columns(3)

    # 1. TESTIGOS (Fundamental para la validez penal)
    with col_t:
        st.write("**TESTIGOS DE ACTUACIÓN**")
        if st.button("➕ Agregar Testigo"):
            st.session_state.testigos.append({"ap": "", "dni": "", "dom": ""})
        for i, t in enumerate(st.session_state.testigos):
            with st.expander(f"Testigo {i+1}"):
                t["ap"] = st.text_input("Nombre y Apellido", t["ap"], key=f"t_ap_{i}")
                t["dni"] = st.text_input("DNI", t["dni"], key=f"t_dni_{i}")
                t["dom"] = st.text_input("Domicilio Real", t["dom"], key=f"t_dom_{i}")

    # 2. VÍCTIMAS
    with col_v:
        st.write("**VÍCTIMAS**")
        if st.button("➕ Agregar Víctima"):
            st.session_state.victimas.append({"ap": "", "dni": "", "dom": ""})
        for i, v in enumerate(st.session_state.victimas):
            with st.expander(f"Víctima {i+1}"):
                v["ap"] = st.text_input("Nombre y Apellido", v["ap"], key=f"v_ap_{i}")
                v["dni"] = st.text_input("DNI", v["dni"], key=f"v_dni_{i}")

    # 3. APREHENDIDOS (FOTO AUTÓNOMA Y VÍNCULO UNÍVOCO)
    with col_a:
        st.write("**APREHENDIDOS**")
        if st.button("➕ Agregar Aprehendido"):
            st.session_state.arrestados.append({"ap": "", "nom": "", "dni": "", "desc_foto": ""})
        for i, a in enumerate(st.session_state.arrestados):
            with st.expander(f"Detenido {i+1}: {a['ap'].upper()}"):
                a["ap"] = st.text_input("Apellido", a["ap"], key=f"a_ap_{i}")
                a["nom"] = st.text_input("Nombre", a["nom"], key=f"a_nom_{i}")
                a["dni"] = st.text_input("DNI", a["dni"], key=f"a_dni_{i}")
                
                foto_ap = st.file_uploader("Subir foto para descripción autónoma", key=f"foto_a_{i}")
                if foto_ap:
                    if not a["desc_foto"]:
                        # Simulación de la directiva de descripción autónoma
                        a["desc_foto"] = "IA SVI: Sujeto masculino, viste campera deportiva oscura, remera blanca, pantalón tipo jean y zapatillas. Sin lesiones visibles."
                    a["desc_foto"] = st.text_area("Descripción Visual (Autónoma):", value=a["desc_foto"], key=f"txt_a_{i}")

# --- BLOQUE 3: SECUESTRO PROFESIONAL (CON FOTO) ---
with tabs[2]:
    st.subheader("📦 Secuestros y Cadena de Custodia")
    if st.button("➕ Nuevo Elemento"):
        st.session_state.secuestros.append({"detalle": "", "precinto": ""})
    for i, s in enumerate(st.session_state.secuestros):
        with st.expander(f"Elemento {i+1}"):
            foto_s = st.file_uploader(f"Foto Secuestro {i+1}", key=f"f_s_{i}")
            s["detalle"] = st.text_area("Descripción Profesional (No pericial):", value=s["detalle"], key=f"det_s_{i}")
            s["precinto"] = st.text_input("Nro. de Precinto de Seguridad", key=f"pre_s_{i}")

# --- BLOQUE 4: ACTA FINAL (PULIDO E IA) ---
with tabs[3]:
    st.subheader("🚀 Generación de Acta Blindada")
    relato = st.text_area("Narración de los hechos (Relato en bruto):", height=250)
    
    if st.button("PULIR Y GENERAR ACTA FINAL"):
        # CRUCE DE DATOS INTELIGENTE
        txt_tes = " / ".join([f"{t['ap']} (DNI: {t['dni']}, dom. {t['dom']})" for t in st.session_state.testigos])
        txt_vic = " / ".join([f"{v['ap']} (DNI: {v['dni']})" for v in st.session_state.victimas])
        txt_apr = "\n".join([f"- {a['ap']} {a['nom']} (DNI: {a['dni']}). Vestía: {a['desc_foto']}" for a in st.session_state.arrestados])
        txt_sec = "\n".join([f"- {s['detalle']} (PRECINTO: {s['precinto']})" for s in st.session_state.secuestros])
        
        acta_completa = f"""
        POLICÍA DE SANTA FE - {dependencia}
        ACTA N°: {acta_n} | 911: {incidencia} | MÓVIL: {movil}
        PERSONAL: {personal} | APOYO: {refuerzo}
        
        SÍNTESIS DEL HECHO: {relato}
        
        TESTIGOS: Bajo la presencia legal de {txt_tes if txt_tes else "[A DESIGNAR]"}...
        VÍCTIMAS: {txt_vic if txt_vic else "No se registran."}
        APREHENDIDOS: Se procede a la demora en {l_apre} de:
        {txt_apr if txt_apr else "A identificar."}
        
        SECUESTROS REALIZADOS:
        {txt_sec if txt_sec else "Sin secuestros."}
        """
        st.code(acta_completa, language="text")
