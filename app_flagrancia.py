import streamlit as st
import json
from fpdf import FPDF
import datetime

# --- FUNCIÓN GENERADORA DE PDF ---
def generar_pdf_bloque_1(datos):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado Institucional
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "POLICIA DE LA PROVINCIA DE SANTA FE", ln=True, align='C')
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "BLOQUE 1: PROTOCOLO DE ACTUACION E INICIO", ln=True, align='C')
    pdf.ln(10)

    # Cuerpo del Acta
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "1. DATOS DEL ARRIBO Y PERSONAL:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Fecha/Hora: {datos['fecha_hora']}", ln=True)
    pdf.cell(0, 8, f"Primer Interviniente: {datos['interviniente']}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "2. PRESERVACION DEL LUGAR:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Lugar Preservado: {datos['preservado']}", ln=True)
    pdf.cell(0, 8, f"Perimetro establecido: {datos['perimetro']}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "3. RELEVAMIENTO DE CAMARAS Y ENTORNO:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Camaras Publicas (911/Muni): {datos['cam_pub']}", ln=True)
    pdf.cell(0, 8, f"Camaras Privadas: {datos['cam_priv']}", ln=True)
    if datos['detalle_cam']:
        pdf.multi_cell(0, 8, f"Detalle de Camaras: {datos['detalle_cam']}")
    pdf.cell(0, 8, f"Iluminacion: {datos['iluminacion']}", ln=True)
    pdf.cell(0, 8, f"Clima: {datos['clima']}", ln=True)

    # Firma
    pdf.set_y(-30)
    pdf.set_font("Arial", 'I', 9)
    pdf.cell(0, 10, f"Autor: Sub-Comisario Castaneda Juan - S.I.V.", align='R')
    
    return pdf.output()

# --- INTERFAZ DEL PROGRAMA ---
st.title("🚓 Bloque 1: Aseguramiento y Entorno")
st.write("---")

# Fila 1: Arribo
col1, col2 = st.columns(2)
with col1:
    fecha_hoy = st.date_input("Fecha del Hecho", datetime.date.today())
    hora_arribo = st.time_input("Hora de Arribo")
with col2:
    personal = st.text_input("Primer Interviniente (Grado y Apellido)", placeholder="Ej: Of. Ppal. Perez")

st.write("---")

# Fila 2: Preservación
st.subheader("🛡️ Medidas de Seguridad")
c1, c2 = st.columns(2)
with c1:
    preservado_op = st.radio("¿Se preservó el lugar?", ["SÍ", "NO"], horizontal=True)
with c2:
    perimetro_op = st.radio("¿Se estableció perímetro (Cinta)?", ["SÍ", "NO"], horizontal=True)

st.write("---")

# Fila 3: Cámaras
st.subheader("📹 Relevamiento de Cámaras y Visibilidad")
ca1, ca2 = st.columns(2)
with ca1:
    pub = st.checkbox("Cámaras Públicas Detectadas")
    priv = st.checkbox("Cámaras Privadas Detectadas")
with ca2:
    ilumina = st.selectbox("Condiciones de Iluminación", ["Óptima", "Regular", "Escasa", "Nula (Oscuridad)"])
    clima = st.selectbox("Condiciones Climáticas", ["Despejado", "Lluvia", "Niebla", "Viento Fuerte"])

det_cam = st.text_area("Ubicación detallada de cámaras (Dirección/Local):")

st.write("---")

# BOTONES DE ACCIÓN
if st.button("🚀 FINALIZAR BLOQUE 1 Y GENERAR ARCHIVOS"):
    datos_completos = {
        "fecha_hora": f"{fecha_hoy} {hora_arribo}",
        "interviniente": personal,
        "preservado": preservado_op,
        "perimetro": perimetro_op,
        "cam_pub": "SÍ" if pub else "NO",
        "cam_priv": "SÍ" if priv else "NO",
        "detalle_cam": det_cam,
        "iluminacion": ilumina,
        "clima": clima
    }

    json_data = json.dumps(datos_completos, indent=4)
    pdf_final = generar_pdf_bloque_1(datos_completos)
    
    st.success("✅ Bloque 1 consolidado correctamente.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button("📥 Descargar PDF Bloque 1", data=pdf_final, file_name="Bloque_1_Inicio.pdf", mime="application/pdf")
    with col_b:
        st.download_button("📥 Descargar JSON para Actante", data=json_data, file_name="bloque_1.json", mime="application/json")
