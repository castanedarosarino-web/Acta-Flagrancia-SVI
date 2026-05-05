import streamlit as st
import json
from fpdf import FPDF

st.set_page_config(layout="wide")

# =========================
# AUTORÍA GLOBAL
# =========================
AUTOR = "Creado por Sub-Comisario Castañeda Juan - S.I.V."


# =========================
# FUNCION PDF BASE
# =========================
def crear_pdf(titulo, cuerpo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "POLICIA DE LA PROVINCIA DE SANTA FE", ln=True, align="C")
    pdf.cell(0, 10, titulo, ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 7, cuerpo)

    pdf.set_y(-20)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, AUTOR, align="R")

    return bytes(pdf.output())


# =========================
# INTERFAZ GENERAL
# =========================
st.title("🚓 ACTA DE PROCEDIMIENTO")
st.subheader("PROTOCOLO DE ACTIVACIÓN AUTOMÁTICA POLICIAL PARA DELITOS DE FLAGRANCIA")

tabs = st.tabs([
    "1. Inicio",
    "2. Arrestado",
    "3. Víctima",
    "4. Testigo",
    "5. Consulta",
    "6. Inspección",
    "7. Secuestros",
    "8. Cierre"
])

# =====================================================
# BLOQUE 1 — INICIO (BASE)
# =====================================================
with tabs[0]:
    st.header("BLOQUE 1 — DATOS BASE")

    nro = st.text_input("N° Acta")
    lugar = st.text_input("Lugar del hecho")
    personal = st.text_input("Personal actuante")
    relato = st.text_area("Relato base")

    if st.button("Guardar Bloque 1"):
        st.session_state["b1"] = {
            "nro": nro,
            "lugar": lugar,
            "personal": personal,
            "relato": relato
        }
        st.success("Guardado")

    if "b1" in st.session_state:
        texto = f"""
ACTA N° {st.session_state['b1']['nro']}

Lugar: {st.session_state['b1']['lugar']}
Personal: {st.session_state['b1']['personal']}

RELATO:
{st.session_state['b1']['relato']}
"""
        pdf = crear_pdf("BLOQUE 1 - INICIO", texto)

        st.download_button("📥 PDF BLOQUE 1", pdf, "bloque1.pdf")
        st.download_button("📥 JSON BLOQUE 1", json.dumps(st.session_state["b1"]), "b1.json")


# =====================================================
# BLOQUE 2 — ARRESTADO
# =====================================================
with tabs[1]:
    st.header("BLOQUE 2 — ARRESTADO")

    nombre = st.text_input("Nombre")
    dni = st.text_input("DNI")

    if st.button("Guardar Arrestado"):
        st.session_state["b2"] = {"nombre": nombre, "dni": dni}

    if "b2" in st.session_state:
        texto = f"Aprehendido: {nombre} DNI {dni}"
        pdf = crear_pdf("ARRESTADO", texto)

        st.download_button("📥 PDF", pdf, "b2.pdf")
        st.download_button("📥 JSON", json.dumps(st.session_state["b2"]), "b2.json")


# =====================================================
# BLOQUE 3 — VÍCTIMA
# =====================================================
with tabs[2]:
    st.header("BLOQUE 3 — VÍCTIMA")

    v_nom = st.text_input("Nombre víctima")
    v_rel = st.text_area("Relato víctima")

    if st.button("Guardar Víctima"):
        st.session_state["b3"] = {"nombre": v_nom, "relato": v_rel}

    if "b3" in st.session_state:
        texto = f"Víctima: {v_nom}\n\nRelato:\n{v_rel}"
        pdf = crear_pdf("VÍCTIMA", texto)

        st.download_button("📥 PDF", pdf, "b3.pdf")
        st.download_button("📥 JSON", json.dumps(st.session_state["b3"]), "b3.json")


# =====================================================
# BLOQUE 4 — TESTIGO
# =====================================================
with tabs[3]:
    st.header("BLOQUE 4 — TESTIGO")

    t_nom = st.text_input("Nombre testigo")
    t_tel = st.text_input("Teléfono")
    t_mail = st.text_input("Correo")

    if st.button("Guardar Testigo"):
        st.session_state["b4"] = {
            "nombre": t_nom,
            "telefono": t_tel,
            "correo": t_mail
        }

    if "b4" in st.session_state:
        texto = f"Testigo: {t_nom}\nTel: {t_tel}\nMail: {t_mail}"
        pdf = crear_pdf("TESTIGO", texto)

        st.download_button("📥 PDF", pdf, "b4.pdf")
        st.download_button("📥 JSON", json.dumps(st.session_state["b4"]), "b4.json")


# =====================================================
# BLOQUE 5 — CONSULTA
# =====================================================
with tabs[4]:
    st.header("BLOQUE 5 — CONSULTA")

    fiscal = st.text_input("Fiscal")
    directivas = st.text_area("Directivas")

    if st.button("Guardar Consulta"):
        st.session_state["b5"] = {
            "fiscal": fiscal,
            "directivas": directivas
        }

    if "b5" in st.session_state:
        texto = f"Fiscal: {fiscal}\n\nDirectivas:\n{directivas}"
        pdf = crear_pdf("CONSULTA", texto)

        st.download_button("📥 PDF", pdf, "b5.pdf")
        st.download_button("📥 JSON", json.dumps(st.session_state["b5"]), "b5.json")


# =====================================================
# BLOQUE 6 — INSPECCIÓN (ANEXO)
# =====================================================
with tabs[5]:
    st.header("BLOQUE 6 — INSPECCIÓN OCULAR (ANEXO)")

    ins = st.text_area("Relato inspección")

    if st.button("Guardar Inspección"):
        st.session_state["b6"] = {"inspeccion": ins}

    if "b6" in st.session_state:
        pdf = crear_pdf("INSPECCIÓN OCULAR", ins)

        st.download_button("📥 PDF", pdf, "b6.pdf")
        st.download_button("📥 JSON", json.dumps(st.session_state["b6"]), "b6.json")


# =====================================================
# BLOQUE 7 — SECUESTROS (MULTIPLE)
# =====================================================
with tabs[6]:
    st.header("BLOQUE 7 — SECUESTROS")

    if "sec" not in st.session_state:
        st.session_state["sec"] = []

    desc = st.text_input("Descripción")
    ubi = st.text_input("Ubicación")

    if st.button("➕ Agregar Secuestro"):
        st.session_state["sec"].append({"desc": desc, "ubi": ubi})

    st.write(st.session_state["sec"])

    if st.session_state["sec"]:
        texto = "\n".join([f"{i+1}) {s['desc']} - {s['ubi']}" for i, s in enumerate(st.session_state["sec"])])
        pdf = crear_pdf("SECUESTROS", texto)

        st.download_button("📥 PDF", pdf, "b7.pdf")
        st.download_button("📥 JSON", json.dumps(st.session_state["sec"]), "b7.json")


# =====================================================
# BLOQUE 8 — CIERRE (CONSOLIDA)
# =====================================================
with tabs[7]:
    st.header("BLOQUE 8 — CIERRE")

    if st.button("📄 Generar Acta Final"):
        datos = st.session_state

        texto = f"""
ACTA FINAL

{datos.get('b1', {}).get('relato', '')}

Aprehendido:
{datos.get('b2', {}).get('nombre', '')}

Testigo:
{datos.get('b4', {}).get('nombre', '')}

INSPECCIÓN:
Se deja constancia que obra acta de inspección ocular como ANEXO.

SECUESTROS:
{datos.get('sec', [])}
"""

        pdf = crear_pdf("ACTA FINAL", texto)

        st.download_button("📥 ACTA FINAL PDF", pdf, "acta_final.pdf")
