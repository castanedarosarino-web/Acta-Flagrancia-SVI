import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Acta Flagrancia", layout="wide")

st.title("🚔 Asistente de Actas en Flagrancia")

# -------------------------------
# BLOQUE 1
# -------------------------------
st.header("BLOQUE 1 — Encabezado y Relato")

nro_acta = st.text_input("Nro. de Acta")
nro_inc = st.text_input("Nro. de Incidencia")

dependencia = st.selectbox("Dependencia", [
    "CRE PÉREZ - SOLDINI - ZAVALLA",
    "CRE FUNES",
    "CRE ROSARIO",
    "B.O.U.",
    "G.T.M.",
    "OTRO"
])

personal = st.text_input("Personal actuante (grado, apellido y nombre)")
refuerzo = st.text_input("Refuerzo")

movil = st.text_input("Nro. de móvil")

fecha = st.date_input("Fecha", datetime.now())
hora = st.time_input("Hora", datetime.now().time())

lugar_hecho = st.text_input("Lugar del hecho")
lugar_aprehension = st.text_input("Lugar de la aprehensión")

relato = st.text_area("Relato del hecho")

# -------------------------------
# BLOQUE 2
# -------------------------------
st.header("BLOQUE 2 — Arrestado")

apellido = st.text_input("Apellido")
nombre = st.text_input("Nombre")
dni = st.text_input("DNI")
domicilio = st.text_input("Domicilio")
profesion = st.text_input("Profesión")

st.subheader("Efectos personales")

efectos = st.text_area("Describir efectos personales")

# -------------------------------
# BLOQUE 3
# -------------------------------
st.header("BLOQUE 3 — Inspección ocular")

st.write("Se deja constancia que se toman vistas fotográficas, apuntes y relevamiento de cámaras del lugar, a los fines de la confección de la inspección ocular y croquis demostrativo que se agregan en foja siguiente.")

camaras = st.selectbox("Cámaras", [
    "Se relevaron",
    "No se observaron",
    "No fue posible relevar"
])

# -------------------------------
# BLOQUE 4
# -------------------------------
st.header("BLOQUE 4 — Comunicación y Cierre")

via = st.selectbox("Vía de comunicación", [
    "Mesa de Enlace",
    "0800 MPA",
    "Fiscal directamente",
    "Pendiente"
])

directiva = st.text_area("Directivas recibidas")

oficial = st.text_input("Oficial de Guardia que recibe")
dependencia_recibe = st.text_input("Dependencia receptora")

st.subheader("Documentación entregada")

acta_apreh = st.checkbox("Acta de aprehensión")
acta_sec = st.checkbox("Acta de secuestro")
cadena = st.checkbox("Cadena de custodia")
inspeccion = st.checkbox("Inspección ocular")
croquis = st.checkbox("Croquis")
fotos = st.checkbox("Fotografías")
entrevistas = st.checkbox("Actas de entrevistas")

# -------------------------------
# GENERAR ACTA
# -------------------------------
if st.button("GENERAR ACTA"):

    texto = f"""
ACTA DE PROCEDIMIENTO

En fecha {fecha} a las {hora}, personal de {dependencia}, {personal}, móvil {movil}, interviene en {lugar_hecho}.

RELATO:
{relato}

APREHENDIDO:
{apellido}, {nombre}, DNI {dni}, domiciliado en {domicilio}, de profesión {profesion}.

EFECTOS:
{efectos}

INSPECCIÓN:
Se deja constancia que se toman vistas fotográficas, apuntes y relevamiento de cámaras del lugar, a los fines de la confección de la inspección ocular y croquis demostrativo que se agregan en foja siguiente.

COMUNICACIÓN:
Vía: {via}
Directiva: {directiva}

ENTREGA:
Se hace entrega al Oficial {oficial}, de {dependencia_recibe}.

CIERRE:
No siendo para más, se da por finalizada la presente acta de procedimiento, previa íntegra lectura y ratificación de su contenido firmando al pie para debida constancia.
"""

    st.download_button("Descargar Acta", texto, file_name="acta.txt")
