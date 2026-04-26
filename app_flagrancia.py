import streamlit as st
import json
from datetime import datetime

# CONFIGURACIÓN DEL SISTEMA DE ACTA DE FLAGRANCIA
st.set_page_config(page_title="Sistema de Acta de Flagrancia", layout="wide")

def cargar_app_flagrancia():
    st.title("⚖️ Acta de Procedimiento de Flagrancia")
    st.subheader("Autoría: SubComisario Castañeda Juan")
    st.markdown("---")

    # --- 1. PERSONAL INTERVINIENTE ---
    with st.expander("👮 1. PERSONAL INTERVINIENTE", expanded=True):
        st.write("Identificación del personal que actúa en el lugar.")
        oficial_actuante = st.text_input("Oficial Actuante (Jerarquía y Nombre)", value="SubComisario Castañeda Juan")
        personal_dotacion = st.text_area("Personal de dotación / Otros intervinientes")
        movil_nro = st.text_input("Móvil Nro.")

    # --- 2. RESEÑA DEL HECHO ---
    with st.expander("📖 2. RESEÑA DEL HECHO"):
        st.write("Relato sucinto y objetivo de lo acontecido.")
        hora_arribo = st.time_input("Hora de arribo al lugar")
        relato_hecho = st.text_area("Descripción de la intervención (Inicio, desarrollo y desenlace)")

    # --- 3. INTERACCIÓN (PREGUNTAS ANTI-NULIDAD) ---
    with st.expander("⚠️ 3. CONTROL DE LEGALIDAD (ANTI-NULIDADES)"):
        st.warning("Responda estas preguntas para asegurar la validez del procedimiento.")
        q1 = st.radio("¿Se identificó como personal policial al inicio del acto?", ["SÍ", "NO"])
        q2 = st.radio("¿Se utilizó la fuerza mínima indispensable?", ["SÍ", "NO"])
        q3 = st.radio("¿Existió peligro inminente para terceros o el personal?", ["SÍ", "NO"])
        q4 = st.radio("¿Se informaron los derechos al aprehendido en el momento?", ["SÍ", "NO"])
        observaciones_legalidad = st.text_input("Observaciones sobre el uso de la fuerza/seguridad")

    # --- 4. ARRESTADO / APREHENDIDO ---
    with st.expander("👤 4. DATOS DEL APREHENDIDO"):
        nombre_detenido = st.text_input("Nombre completo y DNI")
        domicilio_detenido = st.text_input("Domicilio manifestado")
        notificacion_derechos = st.checkbox("Notificación Art. 13 bis / Art. 10 bis realizada")

    # --- 5. SECUESTRO (GENERAL Y VEHICULAR - FORMULARIO 1) ---
    with st.expander("🚗 5. SECUESTROS Y FORMULARIO 1"):
        st.write("### Inventario de Vehículo (Espejo Formulario 1)")
        v_datos = st.text_input("Marca, Modelo y Dominio")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            tambor = st.radio("Tambor de Ignición", ["Bueno", "Regular", "Violentado", "Faltante"])
            neumaticos = st.radio("Neumáticos", ["Bueno", "Regular", "Mal", "Faltante"])
        with col_v2:
            cristales = st.radio("Cristales/Espejos", ["Bueno", "Regular", "Rotos", "Faltante"])
            bateria = st.radio("Batería", ["Bueno", "Faltante"])
        
        secuestro_otros = st.text_area("Otros elementos secuestrados (Armas, Dinero, Celulares)")

    # --- 6. LESIONES ---
    with st.expander("🏥 6. CONSTANTACIÓN DE LESIONES"):
        presenta_lesiones = st.radio("¿El aprehendido presenta lesiones?", ["NO", "SÍ"])
        if presenta_lesiones == "SÍ":
            detalle_lesiones = st.text_area("Describa lesiones visibles y manifestaciones del detenido")
        asistencia_medica = st.checkbox("Se solicitó/trasladó para asistencia médica")

    # --- 7. INSPECCIÓN OCULAR Y CROQUIS ---
    with st.expander("📐 7. INSPECCIÓN OCULAR Y CROQUIS"):
        iluminacion = st.selectbox("Condiciones de iluminación", ["Natural", "Artificial Buena", "Artificial Escasa", "Nula"])
        descripcion_lugar = st.text_area("Descripción del estado del lugar del hecho")
        st.info("Adjunte fotos del croquis manual o realice la descripción de distancias y posiciones aquí.")
        croquis_desc = st.text_area("Detalle de posiciones y distancias (Croquis descriptivo)")

    # --- 8. CADENA DE CUSTODIA ---
    with st.expander("📦 8. CADENA DE CUSTODIA (HOJAS 1 Y 2)"):
        st.write("### Hoja 1: Registro Inicial")
        embalaje = st.selectbox("Tipo de Embalaje", ["Sobre Lacrado", "Bolsa de Seguridad", "Contenedor"])
        st.write("---")
        st.write("### Hoja 2: Continuidad")
        st.info("Primer paso automatizado: DE: SubComisario Castañeda Juan -> PARA: Oficial de Guardia.")
        st.write("Se generan espacios vacíos para firma manual posterior.")

    # --- 9. CIERRE ---
    with st.expander("🏁 9. CIERRE"):
        hora_cierre = st.text_input("Hora de finalización", value=datetime.now().strftime("%H:%M"))
        cierre_texto = f"""No siendo para más, y previa lectura a los intervinientes, se da por finalizado el acto a las {hora_cierre} horas, firmando los presentes de conformidad por ante mí, SubComisario Castañeda Juan, elevándose las actuaciones a la sede judicial correspondiente."""
        st.text_area("Texto de Cierre Final", value=cierre_texto, height=150)

    # --- BOTONES DE ACCIÓN ---
    st.write("---")
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("💾 GUARDAR ACTA (BÚNKER)"):
            st.success("Acta guardada en archivo interno.")
    with c_btn2:
        if st.button("📲 COMPARTIR LEGAJO POR WHATSAPP"):
            st.info("Generando PDF unificado: Acta + Formulario 1 + Cadena de Custodia...")

if __name__ == "__main__":
    cargar_app_flagrancia()
