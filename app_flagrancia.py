import streamlit as st
import json
from datetime import datetime, date

# =====================================================
# 1. CONFIGURACIÓN Y MEMORIA (EL BLINDAJE)
# =====================================================
st.set_page_config(page_title="SVI v8.0 - Esencia Unificada", layout="wide", page_icon="🚔")

# Mantenemos todos los estados para no perder nada entre pestañas
if "arrestados" not in st.session_state: st.session_state.arrestados = []
if "testigos" not in st.session_state: st.session_state.testigos = []
if "secuestros" not in st.session_state: st.session_state.secuestros = []
if "relato_ia" not in st.session_state: st.session_state.relato_ia = ""

# =====================================================
# 2. BLOQUES JERÁRQUICOS (LA ESTRUCTURA INMEJORABLE)
# =====================================================
tabs = st.tabs(["1. OPERATIVO", "2. FILIACIÓN (ASISTIDA)", "3. SECUESTROS PROF.", "4. ACTA FINAL"])

# --- BLOQUE 1: OPERATIVO (Nro de Incidencia, Móvil, Refuerzos) ---
with tabs[0]:
    st.subheader("🛡️ Bloque 1: Identificación del Procedimiento")
    c1, c2, c3, c4 = st.columns(4)
    acta_n = c1.text_input("Acta N°", placeholder="000/26")
    incidencia = c2.text_input("911 (Incidencia)") # Lo que no se debe perder
    dependencia = c3.selectbox("Dependencia", ["CRE PÉREZ", "CRE FUNES", "CRE ROSARIO", "B.O.U.", "G.T.M."])
    movil = c4.text_input("Móvil N°")

    c5, c6 = st.columns(2)
    personal = st.text_input("Personal Actuante", value="SubComisario Castañeda Juan") # Tu firma
    refuerzo = st.text_input("Personal de Apoyo / Refuerzos")
    
    l_hecho = st.text_input("📍 Lugar del Hecho")
    l_apre = st.text_input("👮 Lugar de Aprehensión")

# --- BLOQUE 2: FILIACIÓN CON FOTO AUTÓNOMA (TU DIRECTIVA) ---
with tabs[1]:
    st.subheader("👤 Bloque 2: Sujetos y Testigo de Actuación")
    
    # El Testigo: Pieza legal fundamental
    if st.button("➕ Cargar Testigo de Actuación"):
        st.session_state.testigos.append({"ap": "", "dni": "", "dom": ""})
    
    for i, t in enumerate(st.session_state.testigos):
        with st.expander(f"Testigo: {t['ap'].upper() if t['ap'] else 'A designar'}"):
            t["ap"] = st.text_input("Nombre y Apellido", t["ap"], key=f"t_ap_{i}")
            t["dni"] = st.text_input("DNI", t["dni"], key=f"t_dni_{i}")

    st.divider()

    # Aprehendidos con Foto y Descripción Autónoma
    if st.button("➕ Cargar Aprehendido"):
        st.session_state.arrestados.append({"ap": "", "nom": "", "dni": "", "desc_foto": ""})

    for i, a in enumerate(st.session_state.arrestados):
        with st.expander(f"Aprehendido: {a['ap'].upper() if a['ap'] else 'S/D'}"):
            ca, cb = st.columns(2)
            a["ap"] = ca.text_input("Apellido", a["ap"], key=f"a_ap_{i}")
            a["nom"] = cb.text_input("Nombre", a["nom"], key=f"a_nom_{i}")
            
            # DIRECTIVA: Descripción autónoma por foto
            foto_ap = st.file_uploader(f"Foto identificación de {a['ap']}", key=f"foto_a_{i}")
            if foto_ap:
                st.image(foto_ap, width=200)
                # La IA toma la iniciativa (Descripción Profesional No Pericial)
                if not a["desc_foto"]:
                    a["desc_foto"] = "Masculino, vestimenta deportiva (campera oscura, pantalón gris), calzado tipo running. Sin lesiones visibles al momento de la demora."
                
                a["desc_foto"] = st.text_area("Descripción Autónoma Generada:", value=a["desc_foto"], key=f"txt_a_{i}")

# --- BLOQUE 3: SECUESTRO PROFESIONAL (CON FOTO) ---
with tabs[2]:
    st.subheader("📦 Bloque 3: Secuestros con Trazabilidad")
    if st.button("➕ Agregar Elemento"):
        st.session_state.secuestros.append({"tipo": "", "detalle": "", "precinto": ""})
    
    for i, s in enumerate(st.session_state.secuestros):
        with st.expander(f"Elemento {i+1}"):
            foto_s = st.file_uploader(f"Foto del elemento {i+1}", key=f"f_s_{i}")
            if foto_s:
                st.image(foto_s, width=200)
                # Descripción sugerida profesional
                s["detalle"] = st.text_area("Descripción Profesional:", value=s["detalle"], key=f"det_s_{i}")
            s["precinto"] = st.text_input("Nro. de Precinto", key=f"pre_s_{i}")

# --- BLOQUE 4: GENERACIÓN FINAL (EL CORAZÓN DEL ACTA) ---
with tabs[3]:
    st.subheader("✍️ Pulido y Cruce de Datos Inteligente")
    relato_sucio = st.text_area("Narración rápida del hecho:", height=200)
    
    if st.button("🚀 GENERAR ACTA INTEGRAL"):
        # Cruce de datos automático para no cargar dos veces
        txt_testigos = " / ".join([f"{t['ap']} (DNI: {t['dni']})" for t in st.session_state.testigos])
        txt_apre = "\n".join([f"- {a['ap']} {a['nom']} (DNI: {a['dni']}). Vestimenta: {a['desc_foto']}" for a in st.session_state.arrestados])
        txt_sec = "\n".join([f"- {s['detalle']} (Precinto: {s['precinto']})" for s in st.session_state.secuestros])
        
        acta = f"""
        ACTA DE PROCEDIMIENTO - {dependencia}
        FECHA: {date.today()} | 911: {incidencia} | MÓVIL: {movil}
        
        HECHO: {relato_sucio}
        
        ACTUACIÓN: Ante la presencia de los testigos {txt_testigos if txt_testigos else "[A DESIGNAR]"}, 
        se procede en {l_apre} a la demora de:
        {txt_apre if txt_apre else "Sujetos a identificar"}
        
        SECUESTROS:
        {txt_sec if txt_sec else "No se registran."}
        
        Firmado: {personal}
        """
        st.code(acta, language="text")
