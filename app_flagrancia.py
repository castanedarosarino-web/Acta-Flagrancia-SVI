import streamlit as st
import json
import datetime
from fpdf import FPDF
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import tempfile
import os


st.set_page_config(
    page_title="ACTA DE PROCEDIMIENTO - S.I.V.",
    layout="wide"
)


# =========================
# FUNCIONES BASE
# =========================

def limpiar_texto(texto):
    if texto is None:
        return ""
    reemplazos = {
        "ñ": "n", "Ñ": "N",
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U",
        "°": "Nro."
    }
    texto = str(texto)
    for k, v in reemplazos.items():
        texto = texto.replace(k, v)
    return texto


def firma_a_tempfile(canvas_result):
    if canvas_result is None or canvas_result.image_data is None:
        return None

    img = Image.fromarray(canvas_result.image_data.astype("uint8"), "RGBA")
    fondo = Image.new("RGB", img.size, (255, 255, 255))
    fondo.paste(img, mask=img.split()[3])

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    fondo.save(tmp.name, format="JPEG")
    return tmp.name


def init_state():
    defaults = {
        "bloque1": {},
        "bloque2": {},
        "bloque3": {},
        "bloque4": {},
        "bloque5": {},
        "bloque6": {},
        "bloque7": {},
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()


# =========================
# PDF FINAL - BLOQUE 8
# =========================

def generar_acta_aprehension_testigo_secuestro(datos, firma_testigo=None):
    pdf = FPDF()
    pdf.set_margins(18, 18, 15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "POLICIA DE LA PROVINCIA DE SANTA FE", ln=True, align="C")
    pdf.cell(0, 8, "UNIDAD REGIONAL II", ln=True, align="C")
    pdf.cell(0, 8, "AGRUPACION UNIDADES DE ORDEN PUBLICO", ln=True, align="C")
    pdf.ln(8)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, f"ACTA DE APREHENSION CON TESTIGO Y SECUESTRO Nro. {datos['nro_acta']}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "", 11)

    texto_inicio = (
        f"En la localidad de {datos['localidad']}, departamento {datos['departamento']}, "
        f"Provincia de Santa Fe, a los {datos['fecha']} y siendo las {datos['hora']} horas, "
        f"el funcionario policial actuante {datos['personal_actuante']}, numerario de "
        f"{datos['dependencia']}, a los fines legales que diere lugar, hace constar las "
        f"siguientes circunstancias y comprobaciones."
    )
    pdf.multi_cell(0, 8, limpiar_texto(texto_inicio))
    pdf.ln(3)

    if datos["relato"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 8, "RELATO CIRCUNSTANCIADO:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, limpiar_texto(datos["relato"]))
        pdf.ln(3)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "DATOS DEL APREHENDIDO:", ln=True)
    pdf.set_font("Arial", "", 11)

    ap = datos["aprehendido"]
    pdf.multi_cell(
        0,
        8,
        limpiar_texto(
            f"Se procede a la aprehension de quien consultado por sus datos filiatorios "
            f"dice llamarse {ap.get('apellido', '')} {ap.get('nombre', '')}, DNI {ap.get('dni', '')}, "
            f"de nacionalidad {ap.get('nacionalidad', '')}, estado civil {ap.get('estado_civil', '')}, "
            f"edad {ap.get('edad', '')}, domiciliado en {ap.get('domicilio', '')}."
        )
    )
    pdf.ln(3)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "VICTIMA / ENTREVISTADO:", ln=True)
    pdf.set_font("Arial", "", 11)

    vic = datos["victima"]
    if vic.get("nombre"):
        pdf.multi_cell(
            0,
            8,
            limpiar_texto(
                f"Se registra como victima/entrevistado a {vic.get('nombre', '')}, "
                f"DNI {vic.get('dni', '')}, telefono {vic.get('telefono', '')}, "
                f"correo electronico {vic.get('correo', '')}, domiciliado/a en "
                f"{vic.get('domicilio', '')}. Relato: {vic.get('relato', '')}"
            )
        )
    else:
        pdf.multi_cell(0, 8, limpiar_texto("No se registra victima entrevistada en esta instancia."))
    pdf.ln(3)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "TESTIGO DE ACTUACION:", ln=True)
    pdf.set_font("Arial", "", 11)

    t = datos["testigo"]
    pdf.multi_cell(
        0,
        8,
        limpiar_texto(
            f"Se hace presente y acredita identidad el/la llamado/a {t.get('nombre', '')}, "
            f"DNI {t.get('dni', '')}, domiciliado/a en {t.get('domicilio', '')}, "
            f"telefono {t.get('telefono', '')}, correo electronico {t.get('correo', '')}."
        )
    )
    pdf.ln(3)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "DERECHOS DEL APREHENDIDO:", ln=True)
    pdf.set_font("Arial", "", 11)

    derechos = (
        "Se procede a dar lectura y hacer saber los derechos que le confiere el Art. 268 inc. 13 "
        "del Codigo Procesal Penal de la Provincia de Santa Fe, incluyendo nombrar abogado defensor, "
        "conferenciar en forma privada con su defensor, abstenerse de declarar y solicitar ser escuchado "
        "por el Fiscal interviniente."
    )
    pdf.multi_cell(0, 8, limpiar_texto(derechos))
    pdf.ln(3)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "INSPECCION OCULAR:", ln=True)
    pdf.set_font("Arial", "", 11)

    inspeccion_resumida = (
        "Se realiza inspeccion ocular del lugar del hecho, dejandose constancia que el acta especifica "
        "de inspeccion ocular, registro fotografico y croquis demostrativo se adjuntan como anexo "
        "independiente del presente legajo."
    )
    pdf.multi_cell(0, 8, limpiar_texto(inspeccion_resumida))
    pdf.ln(3)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "SECUESTRO:", ln=True)
    pdf.set_font("Arial", "", 11)

    sec = datos["secuestro"]
    pdf.multi_cell(
        0,
        8,
        limpiar_texto(
            f"Se constata el hallazgo y secuestro de: {sec.get('descripcion', '')}. "
            f"Ubicacion: {sec.get('ubicacion', '')}. "
            f"Destino: {sec.get('destino', '')}. "
            f"Tipo: {sec.get('tipo', '')}."
        )
    )
    pdf.ln(3)

    if datos["consulta"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 8, "CONSULTA FISCAL / DIRECTIVAS:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, limpiar_texto(datos["consulta"]))
        pdf.ln(3)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "ANEXOS QUE SE ACOMPANAN:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(
        0,
        8,
        limpiar_texto(
            "Se deja constancia que se acompanan como anexos independientes las actuaciones generadas "
            "por los bloques correspondientes: entrevista de victima si correspondiere, testigos, "
            "consulta fiscal, inspeccion ocular, croquis demostrativo, registro fotografico, acta de "
            "secuestro y demas constancias producidas por el personal interviniente."
        )
    )
    pdf.ln(3)

    cierre = (
        "Por lo que no siendo para mas se da por finalizada la presente y de concluido el acto, "
        "que previa lectura de su contenido en forma individual firman el testigo y el personal "
        "actuante para debida constancia."
    )
    pdf.multi_cell(0, 8, limpiar_texto(cierre))

    pdf.ln(20)

    y_firma = pdf.get_y()

    if firma_testigo:
        pdf.image(firma_testigo, x=25, y=y_firma - 12, w=60)

    pdf.cell(85, 8, "____________________________", 0, 0, "C")
    pdf.cell(85, 8, "____________________________", 0, 1, "C")
    pdf.cell(85, 6, "FIRMA TESTIGO", 0, 0, "C")
    pdf.cell(85, 6, "FIRMA PERSONAL ACTUANTE", 0, 1, "C")

    pdf.ln(8)
    pdf.set_font("Arial", "I", 9)
    pdf.cell(0, 8, "Creado por Sub-Comisario Castaneda Juan - S.I.V.", ln=True, align="R")

    salida = bytes(pdf.output())

    if firma_testigo:
        os.unlink(firma_testigo)

    return salida


# =========================
# CABECERA GENERAL
# =========================

st.title("🚓 ACTA DE PROCEDIMIENTO")
st.subheader("PROTOCOLO DE ACTIVACIÓN AUTOMÁTICA POLICIAL PARA DELITOS DE FLAGRANCIA")
st.caption("Sistema S.I.V. — Bloques independientes con consolidación final por actante")
st.write("---")


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


# =========================
# BLOQUE 1
# =========================

with tabs[0]:
    st.header("BLOQUE 1 — INICIO / DATOS BASE")

    c1, c2, c3 = st.columns(3)

    with c1:
        nro_acta = st.text_input("Nro. de Acta")
        fecha = st.date_input("Fecha", datetime.date.today())
        hora = st.time_input("Hora")

    with c2:
        localidad = st.text_input("Localidad")
        departamento = st.text_input("Departamento", value="Rosario")
        dependencia = st.text_input("Dependencia")

    with c3:
        personal_actuante = st.text_input("Personal actuante")
        movil = st.text_input("Móvil policial")
        lugar_hecho = st.text_input("Lugar del hecho")

    relato = st.text_area("Relato circunstanciado inicial", height=250)

    if st.button("💾 Guardar Bloque 1"):
        st.session_state.bloque1 = {
            "nro_acta": nro_acta,
            "fecha": str(fecha),
            "hora": str(hora),
            "localidad": localidad,
            "departamento": departamento,
            "dependencia": dependencia,
            "personal_actuante": personal_actuante,
            "movil": movil,
            "lugar_hecho": lugar_hecho,
            "relato": relato,
        }
        st.success("✅ Bloque 1 guardado.")


# =========================
# BLOQUE 2
# =========================

with tabs[1]:
    st.header("BLOQUE 2 — ARRESTADO / APREHENDIDO")

    c1, c2, c3 = st.columns(3)

    with c1:
        dni_ap = st.text_input("DNI aprehendido")
        apellido_ap = st.text_input("Apellido").upper()
        nombre_ap = st.text_input("Nombre").upper()

    with c2:
        nacionalidad_ap = st.text_input("Nacionalidad", value="ARGENTINA")
        estado_civil_ap = st.selectbox(
            "Estado civil",
            ["SOLTERO/A", "CASADO/A", "CONCUBINO/A", "DIVORCIADO/A", "VIUDO/A"]
        )
        edad_ap = st.text_input("Edad")

    with c3:
        domicilio_ap = st.text_input("Domicilio")
        derechos = st.radio("Lectura de derechos", ["SÍ", "NO"], horizontal=True)
        consulta_911 = st.radio("Consulta 911", ["SÍ", "NO"], horizontal=True)

    lesiones = st.radio("¿Presenta lesiones visibles?", ["NO", "SÍ"], horizontal=True)
    detalle_lesiones = ""

    if lesiones == "SÍ":
        detalle_lesiones = st.text_area("Detalle de lesiones / asistencia médica")

    if st.button("💾 Guardar Bloque 2"):
        st.session_state.bloque2 = {
            "dni": dni_ap,
            "apellido": apellido_ap,
            "nombre": nombre_ap,
            "nacionalidad": nacionalidad_ap,
            "estado_civil": estado_civil_ap,
            "edad": edad_ap,
            "domicilio": domicilio_ap,
            "derechos": derechos,
            "consulta_911": consulta_911,
            "lesiones": lesiones,
            "detalle_lesiones": detalle_lesiones,
        }
        st.success("✅ Bloque 2 guardado.")


# =========================
# BLOQUE 3
# =========================

with tabs[2]:
    st.header("BLOQUE 3 — VÍCTIMA / ACTA DE ENTREVISTA")

    c1, c2 = st.columns(2)

    with c1:
        victima_nombre = st.text_input("Nombre y apellido víctima")
        victima_dni = st.text_input("DNI víctima")
        victima_tel = st.text_input("Teléfono víctima")

    with c2:
        victima_correo = st.text_input("Correo electrónico víctima")
        victima_dom = st.text_input("Domicilio víctima")
        victima_fecha_nac = st.text_input("Fecha nacimiento víctima")

    relato_victima = st.text_area("Relato de la víctima / entrevista", height=200)

    if st.button("💾 Guardar Bloque 3"):
        st.session_state.bloque3 = {
            "nombre": victima_nombre,
            "dni": victima_dni,
            "telefono": victima_tel,
            "correo": victima_correo,
            "domicilio": victima_dom,
            "fecha_nac": victima_fecha_nac,
            "relato": relato_victima,
        }
        st.success("✅ Bloque 3 guardado.")


# =========================
# BLOQUE 4
# =========================

with tabs[3]:
    st.header("BLOQUE 4 — TESTIGO Y PERSONAL INTERVINIENTE")

    c1, c2 = st.columns(2)

    with c1:
        testigo_nombre = st.text_input("Nombre y apellido testigo")
        testigo_dni = st.text_input("DNI testigo")
        testigo_dom = st.text_input("Domicilio testigo")

    with c2:
        testigo_tel = st.text_input("Teléfono testigo")
        testigo_correo = st.text_input("Correo electrónico testigo")
        testigo_ocupacion = st.text_input("Ocupación testigo")

    personal_interviniente = st.text_area("Personal policial interviniente")

    st.subheader("Firma digital del testigo")

    firma_testigo_canvas = st_canvas(
        fill_color="rgba(255,255,255,1)",
        stroke_width=3,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=150,
        width=500,
        drawing_mode="freedraw",
        key="firma_testigo_b4"
    )

    if st.button("💾 Guardar Bloque 4"):
        st.session_state.bloque4 = {
            "nombre": testigo_nombre,
            "dni": testigo_dni,
            "domicilio": testigo_dom,
            "telefono": testigo_tel,
            "correo": testigo_correo,
            "ocupacion": testigo_ocupacion,
            "personal_interviniente": personal_interviniente,
            "firma_canvas": firma_testigo_canvas,
        }
        st.success("✅ Bloque 4 guardado.")


# =========================
# BLOQUE 5
# =========================

with tabs[4]:
    st.header("BLOQUE 5 — CONSULTA")

    delitos_criticos = [
        "muerte", "cadáver", "cadaver", "cráneo", "craneo",
        "restos", "homicidio", "bala", "disparo",
        "fallecido", "abuso", "sexual"
    ]

    resena = st.text_area("Reseña del hecho para consulta", height=150)

    autoridad = st.selectbox(
        "Autoridad consultada",
        [
            "Mesa de Enlace",
            "Flagrancia (0800-MPA)",
            "Fiscalía de Homicidios",
            "Fiscalía de Género / Integridad Sexual",
            "Justicia de Menores"
        ]
    )

    nombre_autoridad = st.text_input("Nombre del fiscal / secretario / operador")
    directivas = st.text_area("Directivas impartidas", height=120)

    hecho_critico = any(w in resena.lower() for w in delitos_criticos)

    if hecho_critico and autoridad == "Flagrancia (0800-MPA)":
        st.error("🚨 ALERTA: posible error de competencia. Verificar intervención fiscal correspondiente.")

    if st.button("💾 Guardar Bloque 5"):
        st.session_state.bloque5 = {
            "resena": resena,
            "autoridad": autoridad,
            "nombre_autoridad": nombre_autoridad,
            "directivas": directivas,
            "hecho_critico": "SÍ" if hecho_critico else "NO",
        }
        st.success("✅ Bloque 5 guardado.")


# =========================
# BLOQUE 6
# =========================

with tabs[5]:
    st.header("BLOQUE 6 — INSPECCIÓN OCULAR")

    st.info(
        "Este bloque genera su propia acta de inspección ocular, croquis y registro fotográfico. "
        "En el acta principal del Bloque 8 solo se incorporará una mención resumida como anexo."
    )

    preservado = st.radio("¿Lugar preservado?", ["SÍ", "NO"], horizontal=True)
    cam_pub = st.checkbox("Cámaras públicas")
    cam_priv = st.checkbox("Cámaras privadas")

    ubicacion_camaras = st.text_area("Ubicación de cámaras")
    relato_inspeccion = st.text_area("Relato completo de inspección ocular", height=200)

    img_croquis = st.file_uploader("Cargar croquis / foto del lugar", type=["jpg", "jpeg", "png"])

    if img_croquis:
        st.image(img_croquis, caption="Croquis / imagen cargada", use_container_width=True)

    if st.button("💾 Guardar Bloque 6"):
        st.session_state.bloque6 = {
            "preservado": preservado,
            "camaras_publicas": "SÍ" if cam_pub else "NO",
            "camaras_privadas": "SÍ" if cam_priv else "NO",
            "ubicacion_camaras": ubicacion_camaras,
            "relato_inspeccion": relato_inspeccion,
            "anexo": "Acta especifica de inspeccion ocular, croquis y registro fotografico."
        }
        st.success("✅ Bloque 6 guardado como anexo independiente.")


# =========================
# BLOQUE 7
# =========================

with tabs[6]:
    st.header("BLOQUE 7 — SECUESTROS")

    tipo_sec = st.radio(
        "Tipo de secuestro",
        ["Secuestro de la causa", "Secuestro por depósito"],
        horizontal=True
    )

    codigo_sec = st.text_input("Código interno", value="SEC-01")
    descripcion_sec = st.text_area("Descripción policial del elemento", height=150)
    ubicacion_sec = st.text_area("Ubicación exacta del secuestro")
    destino_sec = st.text_input("Destino / depósito")
    estado_sec = st.selectbox("Estado", ["Bueno", "Regular", "Dañado", "Inutilizado", "No determinado"])

    foto_sec = st.file_uploader("Foto del elemento secuestrado", type=["jpg", "jpeg", "png"])

    if foto_sec:
        st.image(foto_sec, caption="Elemento secuestrado", use_container_width=True)

    elementos_no_manipular = [
        "arma", "pistola", "revólver", "revolver", "escopeta",
        "vaina", "cartucho", "munición", "municion", "bala",
        "explosivo", "granada", "sangre", "celular", "teléfono",
        "telefono", "computadora", "notebook", "estupefaciente", "droga"
    ]

    if any(w in descripcion_sec.lower() for w in elementos_no_manipular):
        st.error("🚨 ALERTA DE NO MANIPULACIÓN: preservar elemento, no manipular y dar intervención correspondiente.")

    if st.button("💾 Guardar Bloque 7"):
        st.session_state.bloque7 = {
            "tipo": tipo_sec,
            "codigo": codigo_sec,
            "descripcion": descripcion_sec,
            "ubicacion": ubicacion_sec,
            "destino": destino_sec,
            "estado": estado_sec,
        }
        st.success("✅ Bloque 7 guardado.")


# =========================
# BLOQUE 8
# =========================

with tabs[7]:
    st.header("BLOQUE 8 — CIERRE Y ACTA FINAL")

    st.info(
        "Este bloque consolida la información enviada por los demás bloques. "
        "No reemplaza las actas individuales: las resume y las menciona como anexos."
    )

    tipo_documento = st.selectbox(
        "Documento final a generar",
        [
            "Acta de aprehensión con testigo y secuestro",
            "Remito de entrega de actuaciones"
        ]
    )

    st.subheader("Vista previa de datos cargados")

    st.json({
        "bloque1": st.session_state.bloque1,
        "bloque2": st.session_state.bloque2,
        "bloque3": st.session_state.bloque3,
        "bloque4": {
            k: v for k, v in st.session_state.bloque4.items() if k != "firma_canvas"
        },
        "bloque5": st.session_state.bloque5,
        "bloque6": st.session_state.bloque6,
        "bloque7": st.session_state.bloque7,
    })

    st.subheader("Vista previa del texto de inspección que irá al acta principal")

    st.text_area(
        "Resumen de inspección ocular para acta principal",
        value=(
            "Se realiza inspección ocular del lugar del hecho, dejándose constancia que el acta específica "
            "de inspección ocular, registro fotográfico y croquis demostrativo se adjuntan como anexo "
            "independiente del presente legajo."
        ),
        height=120
    )

    if st.button("📄 GENERAR ACTA FINAL"):
        faltantes = []

        b1 = st.session_state.bloque1
        b2 = st.session_state.bloque2
        b3 = st.session_state.bloque3
        b4 = st.session_state.bloque4
        b5 = st.session_state.bloque5
        b6 = st.session_state.bloque6
        b7 = st.session_state.bloque7

        if not b1.get("nro_acta"):
            faltantes.append("Bloque 1: Nro. de acta")
        if not b1.get("personal_actuante"):
            faltantes.append("Bloque 1: Personal actuante")
        if not b1.get("dependencia"):
            faltantes.append("Bloque 1: Dependencia")
        if not b1.get("relato"):
            faltantes.append("Bloque 1: Relato circunstanciado")

        if not b2.get("apellido") or not b2.get("nombre"):
            faltantes.append("Bloque 2: Datos del aprehendido")

        if not b4.get("nombre"):
            faltantes.append("Bloque 4: Nombre del testigo")
        if not b4.get("dni"):
            faltantes.append("Bloque 4: DNI del testigo")
        if not b4.get("telefono"):
            faltantes.append("Bloque 4: Teléfono del testigo")
        if not b4.get("correo"):
            faltantes.append("Bloque 4: Correo electrónico del testigo")

        if not b7.get("descripcion"):
            faltantes.append("Bloque 7: Descripción del secuestro")
        if not b7.get("ubicacion"):
            faltantes.append("Bloque 7: Ubicación del secuestro")
        if not b7.get("destino"):
            faltantes.append("Bloque 7: Destino del secuestro")

        firma_canvas = b4.get("firma_canvas")

        if firma_canvas is None or firma_canvas.image_data is None:
            faltantes.append("Bloque 4: Firma digital del testigo")

        if not b6.get("relato_inspeccion"):
            st.warning(
                "⚠️ Bloque 6 no tiene relato completo de inspección ocular. "
                "El acta final puede generarse, pero recordá adjuntar el anexo si corresponde."
            )

        if faltantes:
            st.error("⚠️ No se puede generar el acta. Faltan campos obligatorios:")
            for f in faltantes:
                st.write(f"- {f}")

        else:
            firma_tmp = firma_a_tempfile(firma_canvas)

            datos_finales = {
                "nro_acta": b1.get("nro_acta", ""),
                "localidad": b1.get("localidad", ""),
                "departamento": b1.get("departamento", ""),
                "fecha": b1.get("fecha", ""),
                "hora": b1.get("hora", ""),
                "personal_actuante": b1.get("personal_actuante", ""),
                "dependencia": b1.get("dependencia", ""),
                "relato": b1.get("relato", ""),
                "aprehendido": b2,
                "victima": b3,
                "testigo": b4,
                "consulta": b5.get("directivas", ""),
                "inspeccion": (
                    "Se realiza inspección ocular del lugar del hecho, dejándose constancia que el acta específica "
                    "de inspección ocular, registro fotográfico y croquis demostrativo se adjuntan como anexo."
                ),
                "secuestro": b7,
                "anexos": {
                    "bloque3_victima": "Acta de entrevista de víctima si correspondiere.",
                    "bloque6_inspeccion": "Acta específica de inspección ocular, croquis y registro fotográfico.",
                    "bloque7_secuestro": "Acta de secuestro / cadena de custodia."
                }
            }

            pdf_final = generar_acta_aprehension_testigo_secuestro(
                datos_finales,
                firma_testigo=firma_tmp
            )

            json_final = json.dumps(datos_finales, indent=4, ensure_ascii=False, default=str)

            st.success("✅ Acta final generada correctamente.")

            c1, c2 = st.columns(2)

            with c1:
                st.download_button(
                    "📥 Descargar ACTA FINAL PDF",
                    data=pdf_final,
                    file_name="Acta_Aprehension_Testigo_Secuestro.pdf",
                    mime="application/pdf"
                )

            with c2:
                st.download_button(
                    "📥 Descargar JSON FINAL",
                    data=json_final,
                    file_name="acta_final_siv.json",
                    mime="application/json"
                )
