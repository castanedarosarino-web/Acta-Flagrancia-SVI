import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN TÁCTICA ---
st.set_page_config(page_title="SVI - Procedimiento Operativo", layout="wide")

# (Estilos y cabeceras se mantienen...)

tab1, tab2, tab3, tab4 = st.tabs(["📝 RELATO", "👥 DETENIDOS/911", "🚗 VEHÍCULOS/SECUESTROS", "📄 ACTA FINAL"])

# --- TAB 2: DETENIDOS CON CONSULTA 911 ---
with tab2:
    st.subheader("👥 Identificación y Consulta de Requerimientos")
    cant_det = st.number_input("Cantidad de sujetos", min_value=1, value=1)
    
    lista_detenidos = []
    for i in range(cant_det):
        with st.expander(f"FILIACIÓN SUJETO N° {i+1}", expanded=True):
            # ... (campos de filiación completa: DNI, Nombre, Padres, etc.) ...
            
            st.markdown("---")
            st.subheader("📞 Consulta al Sistema Cóndor / 911")
            c_911_1, c_911_2, c_911_3 = st.columns([2, 2, 3])
            
            operador = c_911_1.text_input("Operador 911 Nro/Nombre", key=f"op_{i}", placeholder="Ej: Op. 45 / Local 911")
            resultado_911 = c_911_2.selectbox("Resultado Consulta", 
                                             ["SIN REQUERIMIENTO", "CON PEDIDO DE CAPTURA", "CON PROHIBICIÓN DE PARADERO"], 
                                             key=f"res_{i}")
            detalle_911 = c_911_3.text_input("Nro de Oficio / Juzgado (si posee)", key=f"of_{i}")
            
            lista_detenidos.append({
                "dni": dni, "full": f"{ape} {nom}", "op": operador, "res": resultado_911, "of": detalle_911
            })

# --- TAB 3: VEHÍCULOS Y SECUESTROS ---
with tab3:
    st.subheader("🚗 Relevamiento de Vehículos")
    possee_vehiculo = st.checkbox("¿Hubo vehículo involucrado?")
    
    if possee_vehiculo:
        c_v1, c_v2, c_v3 = st.columns(3)
        dominio = c_v1.text_input("Dominio (Patente)")
        modelo = c_v2.text_input("Marca / Modelo")
        motor_chasis = c_v3.text_input("Nro Motor / Chasis")
        
        st.markdown("🔍 **Consulta de Pedido de Secuestro**")
        cv_911_1, cv_911_2 = st.columns(2)
        op_vehiculo = cv_911_1.text_input("Operador 911 (Consulta Vehicular)")
        res_vehiculo = cv_911_2.selectbox("Estado Vehicular", 
                                         ["SIN NOVEDAD (Limpio)", "CON PEDIDO DE SECUESTRO ACTIVO"])
        
    st.divider()
    st.subheader("📦 Otros Secuestros e Inspección Ocular")
    # ... (lógica de fotos y descripción de IA para el lugar) ...

# --- TAB 4: ACTA FINAL (NARRATIVA INTEGRADA) ---
with tab4:
    # Lógica para redactar el párrafo de las consultas al 911
    texto_consultas = ""
    for d in lista_detenidos:
        texto_consultas += f"Que consultado el sistema de emergencias 911 a través del operador {d['op']}, el mismo informa que sobre el llamado {d['full']} pesa un resultado de: {d['res']} {d['of']}. "
    
    texto_vehiculo = ""
    if possee_vehiculo:
        texto_vehiculo = f"Asimismo, se realiza consulta sobre el rodado {modelo} dominio {dominio}, informando el operador {op_vehiculo} que el mismo se encuentra {res_vehiculo}. "

    # Acta integrada
    cuerpo_acta = f"""{st.session_state.relato_final}. 
    
{texto_consultas}
{texto_vehiculo}

Atento a ello, se procede al traslado de los mismos a sede policial..."""

    st.code(cuerpo_acta, language=None)
