import streamlit as st
from datetime import datetime

# 1. CONFIGURACIÓN E IDENTIFICACIÓN
st.set_page_config(page_title="Sistema de Flagrancia", layout="wide")

st.title("⚖️ Acta de Procedimiento de Flagrancia")
st.subheader("Autoría: SubComisario Castañeda Juan")

# --- MÓDULOS DEL ACTA ---
with st.expander("👮 1. PERSONAL INTERVINIENTE", expanded=True):
    oficial_actuante = st.text_input("Oficial Actuante", value="SubComisario Castañeda Juan")
    personal_dotacion = st.text_area("Personal de dotación")
    lugar = st.text_input("Lugar del procedimiento")

with st.expander("📖 2. RESEÑA DEL HECHO"):
    fecha_procedimiento = st.date_input("Fecha")
    relato_hecho = st.text_area("Relato de la intervención")

with st.expander("👤 3. APREHENDIDO Y LESIONES"):
    nombre_detenido = st.text_input("Nombre y Apellido")
    dni_detenido = st.text_input("DNI")
    presenta_lesiones = st.radio("¿Presenta lesiones?", ["NO", "SÍ"])

with st.expander("🚗 4. SECUESTROS (FORMULARIO 1)"):
    v_datos = st.text_input("Vehículo (Marca/Patente)")
    v_obs = st.text_area("Estado/Daños")
    secuestro_otros = st.text_area("Otros elementos (Armas/Celulares)")

with st.expander("📦 5. CADENA DE CUSTODIA"):
    embalaje = st.selectbox("Embalaje", ["Bolsa plástica", "Bolsa papel", "Sobre Lacrado"])
    st.info(f"ENTREGA: {oficial_actuante} (Primer Eslabón)")

# --- CIERRE ---
hora_cierre = st.text_input("Hora de cierre", value=datetime.now().strftime("%H:%M"))
cierre_rosario = f"No siendo para más, se da por finalizado el acto a las {hora_cierre} del día {fecha_procedimiento}. Certifico y firmo: {oficial_actuante}."

# --- GESTIÓN DE SALIDA (COPIAR Y PEGAR) ---
st.write("---")
st.subheader("📥 Acciones Finales")

# Preparamos el texto para WhatsApp
texto_para_pegar = f"""
*ACTA DE PROCEDIMIENTO DE FLAGRANCIA*
*AUTOR:* {oficial_actuante}
*LUGAR:* {lugar}
*FECHA:* {fecha_procedimiento} - {hora_cierre}

*APREHENDIDO:* {nombre_detenido} (DNI: {dni_detenido})
*LESIONES:* {presenta_lesiones}

*RESEÑA:* {relato_hecho}

*SECUESTROS:*
{v_datos}
{v_obs}
{secuestro_otros}

*CIERRE:* {cierre_rosario}
"""

col1, col2 = st.columns(2)

with col1:
    if st.button("📋 PREPARAR TEXTO PARA WHATSAPP"):
        st.write("Seleccioná el texto de abajo, copialo y pegalo en el chat:")
        st.code(texto_para_pegar)

with col2:
    st.download_button(
        label="💾 DESCARGAR ACTA (.TXT)",
        data=texto_para_pegar,
        file_name=f"Acta_{nombre_detenido}.txt",
        mime="text/plain"
    )
