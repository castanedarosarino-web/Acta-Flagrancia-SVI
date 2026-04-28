import streamlit as st
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Acta Flagrancia", layout="wide", page_icon="🚔")

# Estilo personalizado para mejorar la visualización
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚔 Asistente de Actas en Flagrancia")
st.info("Complete los campos para generar el borrador del acta de procedimiento.")

# -------------------------------
# BLOQUE 1 - Encabezado
# -------------------------------
with st.expander("BLOQUE 1 — Encabezado y Relato", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        nro_acta = st.text_input("Nro. de Acta")
        dependencia = st.selectbox("Dependencia", [
            "CRE PÉREZ - SOLDINI - ZAVALLA", "CRE FUNES", "CRE ROSARIO", 
            "B.O.U.", "G.T.M.", "OTRO"
        ])
        personal = st.text_input("Personal actuante (Grado, Apellido y Nombre)")
        fecha = st.date_input("Fecha", datetime.now())
        lugar_hecho = st.text_input("Lugar del hecho")
    
    with col2:
        nro_inc = st.text_input("Nro. de Incidencia")
        movil = st.text_input("Nro. de móvil")
        refuerzo = st.text_input("Refuerzo / Colaboración")
        hora = st.time_input("Hora", datetime.now().time())
        lugar_aprehension = st.text_input("Lugar de la aprehensión")

    relato = st.text_area("Relato del hecho (Sea descriptivo)", height=150)

# -------------------------------
# BLOQUE 2 - Aprehendido
# -------------------------------
with st.expander("BLOQUE 2 — Datos del Arrestado"):
    c1, c2, c3 = st.columns([2, 2, 1])
    apellido = c1.text_input("Apellido(s)")
    nombre = c2.text_input("Nombre(s)")
    dni = c3.text_input("DNI/Documento")
    
    domicilio = st.text_input("Domicilio")
    profesion = st.text_input("Profesión/Ocupación")
    efectos = st.text_area("Efectos personales y Secuestros", placeholder="Ej: 1 teléfono celular, llave de vehículo, etc.")

# -------------------------------
# BLOQUE 3 - Inspección y Cámaras
# -------------------------------
with st.expander("BLOQUE 3 — Inspección Ocular"):
    st.write("Relevamiento de pruebas en el lugar:")
    camaras = st.radio("Cámaras de seguridad:", [
        "Se relevaron cámaras en las inmediaciones.",
        "No se observaron dispositivos de videovigilancia.",
        "No fue posible relevar cámaras en el momento."
    ], horizontal=True)

# -------------------------------
# BLOQUE 4 - Comunicación y Cierre
# -------------------------------
with st.expander("BLOQUE 4 — Comunicación y Entrega"):
    col_a, col_b = st.columns(2)
    with col_a:
        via = st.selectbox("Vía de comunicación", ["Mesa de Enlace", "0800 MPA", "Fiscal directamente", "Pendiente"])
        oficial = st.text_input("Oficial de Guardia que recibe")
    with col_b:
        dependencia_recibe = st.text_input("Dependencia receptora")
        
    directiva = st.text_area("Directivas fiscales recibidas")

    st.markdown("**Documentación adjunta:**")
    check_cols = st.columns(4)
    acta_apreh = check_cols[0].checkbox("Acta Aprehensión")
    acta_sec = check_cols[1].checkbox("Acta Secuestro")
    cadena = check_cols[2].checkbox("Cadena Custodia")
    fotos = check_cols[3].checkbox("Fotografías")

# -------------------------------
# GENERAR ACTA
# -------------------------------
if st.button("GENERAR ACTA PARA DESCARGAR"):
    
    # Formateo de fecha y hora para el texto
    f_str = fecha.strftime('%d/%m/%Y')
    h_str = hora.strftime('%H:%M')

    texto_final = f"""ACTA DE PROCEDIMIENTO POLICIAL
------------------------------------------
ACTA NRO: {nro_acta} | INCIDENCIA: {nro_inc}
DEPENDENCIA: {dependencia}
MÓVIL: {movil} | PERSONAL: {personal}
REFUERZO: {refuerzo}

En la ciudad de Rosario y/o alrededores, siendo fecha {f_str} a las {h_str} horas, el personal actuante arriba mencionado hace constar que interviene en un hecho ocurrido en {lugar_hecho}.

RELATO DE LOS HECHOS:
{relato}

LUGAR DE APREHENSIÓN: {lugar_aprehension}

DATOS DEL APREHENDIDO:
- Apellido y Nombre: {apellido.upper()}, {nombre.upper()}
- DNI: {dni}
- Domicilio: {domicilio}
- Profesión: {profesion}

EFECTOS PERSONALES / SECUESTROS:
{efectos}

INSPECCIÓN OCULAR Y CÁMARAS:
Se deja constancia que se toman vistas fotográficas y apuntes del lugar. 
Estado de cámaras: {camaras}

COMUNICACIÓN JUDICIAL:
Comunicado vía {via}.
Directivas: {directiva}

ENTREGA DEL PROCEDIMIENTO:
Se hace entrega del procedimiento, aprehendido y efectos al Oficial {oficial} de la dependencia {dependencia_recibe}.

No siendo para más, se da por finalizada la presente acta, previa íntegra lectura y ratificación de su contenido, firmando los intervinientes para debida constancia.
"""

    st.subheader("Vista Previa")
    st.text_area("Copia el texto o descarga el archivo:", texto_final, height=300)
    
    st.download_button(
        label="📥 Descargar Acta en .TXT",
        data=texto_final,
        file_name=f"Acta_{apellido}_{f_str}.txt",
        mime="text/plain"
    )
