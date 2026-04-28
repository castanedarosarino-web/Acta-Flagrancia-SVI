import streamlit as st
from datetime import datetime, date
import json
import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI

st.set_page_config(
    page_title="Acta Flagrancia SVI",
    layout="wide",
    page_icon="🚔"
)

# =========================
# CONFIGURACIÓN IA
# =========================

def get_client():
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def ia_disponible():
    return get_client() is not None


def llamar_ia_texto(prompt, sistema="Sos un asistente policial especializado en redacción de actas de procedimiento de Santa Fe. Respondé en español formal, claro y operativo."):
    client = get_client()
    if client is None:
        return "IA no disponible. Configure OPENAI_API_KEY en Streamlit Secrets."

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sistema},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error IA: {e}"


def imagen_a_base64(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def llamar_ia_imagen(uploaded_file, prompt):
    client = get_client()
    if client is None:
        return "IA no disponible. Configure OPENAI_API_KEY en Streamlit Secrets."

    try:
        img_b64 = imagen_a_base64(uploaded_file)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sos un asistente policial. Describís imágenes para actas en español formal. "
                        "No identifiques personas. No diagnostiques lesiones. No digas 'en la imagen se observa' "
                        "si el texto será incorporado al acta; redactá como descripción policial validable."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"},
                        },
                    ],
                },
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error IA imagen: {e}"


# =========================
# ESTADO
# =========================

def inicializar():
    defaults = {
        "victimas": [],
        "testigos": [],
        "arrestados": [],
        "secuestros": [],
        "camara_constancias": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def edad(fecha_nac):
    if not fecha_nac:
        return ""
    hoy = date.today()
    return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))


def persona(p):
    ap = p.get("apellido", "").upper()
    nom = p.get("nombre", "").upper()
    dni = p.get("dni", "")
    base = f"{ap}, {nom}".strip(", ")
    if dni:
        return f"{base}, DNI N° {dni}"
    return base or "persona no identificada"


def agregar_arrestado():
    st.session_state.arrestados.append({
        "dni": "",
        "apodo": "",
        "apellido": "",
        "nombre": "",
        "estado_civil": "No informado",
        "fecha_nac": date(1998, 5, 15),
        "hijo_de": "",
        "profesion": "",
        "domicilio": "",
        "instruccion": "Sí",
        "dictado": "",
        "descripcion": "",
        "lesiones": "No",
        "lesion_detalle": "",
        "traslado": "No",
        "nosocomio": "",
        "diagnostico": "",
        "certificado": "No",
        "requisa": "Pendiente",
        "testigo_requisa": "",
        "urgencia_requisa": "",
    })


def agregar_victima():
    st.session_state.victimas.append({
        "apellido": "",
        "nombre": "",
        "dni": "",
        "domicilio": "",
        "telefono": "",
        "correo": "",
        "rol": "Víctima",
        "manifestacion": "",
    })


def agregar_testigo():
    st.session_state.testigos.append({
        "apellido": "",
        "nombre": "",
        "dni": "",
        "domicilio": "",
        "telefono": "",
        "correo": "",
        "rol": "Testigo del hecho",
        "manifestacion": "",
    })


# =========================
# REDACCIONES
# =========================

def generar_acta(data):
    dep = data["dependencia_otro"] if data["dependencia"] == "OTRO" else data["dependencia"]

    texto = []
    texto.append("ACTA DE PROCEDIMIENTO\n")
    texto.append(
        f"En fecha {data['fecha']}, siendo las {data['hora']} horas, personal de {dep}, "
        f"integrado por {data['personal_actuante']}, con refuerzo/colaboración de {data['refuerzo']}, "
        f"móvil N° {data['movil']}, interviene en relación a un hecho ocurrido en {data['lugar_hecho']}, "
        f"siendo lugar de aprehensión {data['lugar_aprehension']}."
    )
    texto.append(f"Nro. de Acta: {data['nro_acta']}. Nro. de Incidencia: {data['nro_incidencia']}.\n")

    texto.append("RELATO DEL HECHO:")
    texto.append(data["relato"] or "Sin relato cargado.")

    if st.session_state.victimas:
        texto.append("\nVÍCTIMA/S - DAMNIFICADO/S:")
        for v in st.session_state.victimas:
            texto.append(
                f"Se entrevista a {persona(v)}, domiciliado/a en {v['domicilio']}, teléfono {v['telefono']}, "
                f"en carácter de {v['rol']}, quien manifiesta: {v['manifestacion']}."
            )

    if st.session_state.testigos:
        texto.append("\nTESTIGO/S DEL HECHO:")
        for t in st.session_state.testigos:
            texto.append(
                f"Asimismo, se entrevista a {persona(t)}, domiciliado/a en {t['domicilio']}, teléfono {t['telefono']}, "
                f"en carácter de {t['rol']}, quien manifiesta: {t['manifestacion']}."
            )

    if st.session_state.arrestados:
        texto.append("\nAPREHENDIDO/S:")
        for a in st.session_state.arrestados:
            texto.append(
                f"Se identifica al aprehendido como {persona(a)}, alias '{a['apodo']}', "
                f"de estado civil {a['estado_civil']}, nacido en fecha {a['fecha_nac']}, "
                f"de {edad(a['fecha_nac'])} años de edad, hijo de {a['hijo_de']}, "
                f"de profesión {a['profesion']}, domiciliado en {a['domicilio']}, "
                f"quien manifiesta saber leer y escribir: {a['instruccion']}."
            )

            if a["descripcion"]:
                texto.append(f"Respecto de {persona(a)}, se deja constancia de la siguiente descripción externa: {a['descripcion']}.")

            if a["lesiones"] == "Sí":
                texto.append(
                    f"Respecto de {persona(a)}, se deja constancia que {a['lesion_detalle']}. "
                    f"Traslado a nosocomio: {a['traslado']}. Nosocomio: {a['nosocomio']}. "
                    f"Diagnóstico informado por personal médico: {a['diagnostico']}. "
                    f"Certificado médico: {a['certificado']}."
                )

            texto.append(
                f"Requisa personal: {a['requisa']}. Testigo de requisa/secuestro: {a['testigo_requisa']}. "
                f"Justificación si no hubo testigo: {a['urgencia_requisa']}."
            )

    if st.session_state.secuestros:
        texto.append("\nSECUESTROS / DEPÓSITOS:")
        for s in st.session_state.secuestros:
            texto.append(s["texto"])

    texto.append("\nINSPECCIÓN OCULAR Y CROQUIS:")
    texto.append(
        "Se deja constancia que se toman vistas fotográficas, apuntes y relevamiento de cámaras del lugar, "
        "a los fines de la confección de la inspección ocular y croquis demostrativo que se agregan en foja siguiente."
    )

    texto.append("\nCOMUNICACIÓN:")
    texto.append(
        f"Se deja constancia que se entabla comunicación por vía {data['via_comunicacion']}, "
        f"siendo atendido por {data['receptor']}, fiscal informado/interviniente {data['fiscal']}, "
        f"a las {data['hora_comunicacion']} horas, recibiéndose la siguiente resolución/directiva: {data['directivas']}."
    )

    entrega = ", ".join(data["documentos_entregados"])
    if data["otros_entrega"]:
        entrega += ", " + data["otros_entrega"]

    texto.append("\nENTREGA Y CIERRE:")
    texto.append(
        f"Se deja constancia que se hace entrega de las presentes actuaciones y elementos relacionados al procedimiento "
        f"al Oficial de Guardia {data['oficial_guardia']}, numerario de {data['dependencia_receptora']}, "
        f"consistentes en {entrega}, para su prosecución conforme trámite de rigor. "
        "No siendo para más, se da por finalizada la presente acta de procedimiento, previa íntegra lectura "
        "y ratificación de su contenido, firmando al pie para debida constancia.-"
    )

    return "\n".join(texto)


def generar_inspeccion(data):
    texto = []
    texto.append("ACTA DE INSPECCIÓN OCULAR Y CROQUIS DEMOSTRATIVO\n")
    texto.append(
        f"En fecha {data['fecha']}, siendo las {data['hora']} horas, personal actuante se constituye en "
        f"{data['lugar_hecho']}, a los fines de realizar inspección ocular, toma de apuntes, vistas fotográficas, "
        f"relevamiento de cámaras y croquis demostrativo."
    )

    texto.append("\nDESCRIPCIÓN TÉCNICA DEL LUGAR:")
    texto.append(data["descripcion_lugar"])

    texto.append("\nVISTAS FOTOGRÁFICAS:")
    texto.append("Vista N° 1: panorámica general del lugar del hecho.")
    texto.append("Vista N° 2: vista media o de relación entre sectores relevantes.")
    texto.append("Vista N° 3: vista de detalle de rastros, daños, indicios o elementos de interés.")
    texto.append("Vista N° 4: vista de orientación o reconstrucción del recorrido, fuga o aprehensión.")

    texto.append("\nRELEVAMIENTO DE CÁMARAS:")
    texto.append(data["camara_estado"])
    for c in st.session_state.camara_constancias:
        texto.append(c)

    texto.append("\nCROQUIS DEMOSTRATIVO:")
    texto.append(data["croquis"])

    texto.append(
        "\nNo siendo para más, se da por finalizada la presente inspección ocular, quedando las vistas fotográficas, "
        "apuntes y croquis demostrativo agregados a las actuaciones correspondientes.-"
    )
    return "\n".join(texto)


# =========================
# UI
# =========================

inicializar()

st.title("🚔 Asistente de Actas en Flagrancia")

if ia_disponible():
    st.success("IA activa: clave OPENAI_API_KEY detectada.")
else:
    st.warning("IA no activa: falta OPENAI_API_KEY en Streamlit Secrets.")

tabs = st.tabs(["1. Encabezado", "2. Arrestado", "3. Inspección", "4. Cierre", "Vista final"])

with tabs[0]:
    st.header("BLOQUE 1 — Encabezado, relato, víctimas y testigos")

    c1, c2 = st.columns(2)
    nro_acta = c1.text_input("Nro. de Acta")
    nro_incidencia = c2.text_input("Nro. de Incidencia")

    dependencia = c1.selectbox("Dependencia", [
        "CRE PÉREZ - SOLDINI - ZAVALLA",
        "CRE FUNES",
        "CRE ROSARIO",
        "B.O.U.",
        "G.T.M.",
        "OTRO"
    ])
    dependencia_otro = c2.text_input("Dependencia si eligió OTRO")

    personal_actuante = c1.text_input("Personal actuante (grado, apellido y nombre)")
    refuerzo = c2.text_input("Refuerzo / colaboración")
    movil = c1.text_input("Nro. de móvil")

    fecha = c1.date_input("Fecha", date.today())
    hora = c2.time_input("Hora", datetime.now().time().replace(second=0, microsecond=0))

    lugar_hecho = c1.text_input("Lugar del hecho")
    lugar_aprehension = c2.text_input("Lugar de la aprehensión")

    relato = st.text_area(
        "Relato del hecho",
        placeholder="Relate brevemente qué ocurrió, dónde, cuándo y cómo intervino el personal policial."
    )

    if st.button("Analizar relato con IA"):
        prompt = f"""
Analizá este relato policial y devolvé:
1. Hecho aparente.
2. Lugar del hecho.
3. Lugar de aprehensión.
4. Si hay arrestados y cuántos.
5. Si hay víctima.
6. Si hay testigos.
7. Si hay requisa.
8. Si hay secuestros.
9. Si hay cámaras.
10. Motivo de flagrancia.
11. Faltantes importantes.

Relato:
{relato}
"""
        st.text_area("Resultado IA del relato", llamar_ia_texto(prompt), height=260)

    st.subheader("Víctima/s o damnificado/s")
    if st.button("Agregar víctima / damnificado"):
        agregar_victima()

    for i, v in enumerate(st.session_state.victimas):
        with st.expander(f"Víctima {i+1}"):
            v["apellido"] = st.text_input("Apellido", key=f"v_ap_{i}")
            v["nombre"] = st.text_input("Nombre", key=f"v_nom_{i}")
            v["dni"] = st.text_input("DNI", key=f"v_dni_{i}")
            v["domicilio"] = st.text_input("Domicilio", key=f"v_dom_{i}")
            v["telefono"] = st.text_input("Teléfono", key=f"v_tel_{i}")
            v["correo"] = st.text_input("Correo", key=f"v_cor_{i}")
            v["rol"] = st.text_input("Rol", value=v["rol"], key=f"v_rol_{i}")
            v["manifestacion"] = st.text_area("Qué manifestó", key=f"v_man_{i}")

    st.subheader("Testigo/s del hecho")
    if st.button("Agregar testigo del hecho"):
        agregar_testigo()

    for i, t in enumerate(st.session_state.testigos):
        with st.expander(f"Testigo {i+1}"):
            t["apellido"] = st.text_input("Apellido", key=f"t_ap_{i}")
            t["nombre"] = st.text_input("Nombre", key=f"t_nom_{i}")
            t["dni"] = st.text_input("DNI", key=f"t_dni_{i}")
            t["domicilio"] = st.text_input("Domicilio", key=f"t_dom_{i}")
            t["telefono"] = st.text_input("Teléfono", key=f"t_tel_{i}")
            t["correo"] = st.text_input("Correo", key=f"t_cor_{i}")
            t["rol"] = st.text_input("Rol", value=t["rol"], key=f"t_rol_{i}")
            t["manifestacion"] = st.text_area("Qué observó o informó", key=f"t_man_{i}")

with tabs[1]:
    st.header("BLOQUE 2 — Arrestado")

    if st.button("Agregar arrestado"):
        agregar_arrestado()

    for i, a in enumerate(st.session_state.arrestados):
        with st.expander(f"Arrestado {i+1} — {persona(a)}", expanded=True):
            st.caption("Arrestado 1/2 es solo referencia interna. En el acta se redacta con nombre y DNI.")

            a["dictado"] = st.text_area("Dictado rápido opcional", key=f"a_dic_{i}")

            if st.button(f"Procesar dictado con IA - Arrestado {i+1}"):
                prompt = f"""
Separá este dictado en datos filiatorios:
DNI, apodo, apellido, nombre, estado civil, fecha nacimiento, hijo de, profesión, domicilio, instrucción.

Dictado:
{a['dictado']}
"""
                st.text_area(f"Resultado IA dictado arrestado {i+1}", llamar_ia_texto(prompt), height=220)

            c1, c2, c3 = st.columns(3)
            a["dni"] = c1.text_input("DNI", key=f"a_dni_{i}")
            a["apodo"] = c2.text_input("Apodo", key=f"a_apodo_{i}")
            a["estado_civil"] = c3.selectbox("Estado civil", ["Soltero", "Casado", "Divorciado", "Viudo", "Unión convivencial", "No informado"], key=f"a_ec_{i}")

            a["apellido"] = c1.text_input("Apellido", key=f"a_ap_{i}")
            a["nombre"] = c2.text_input("Nombre", key=f"a_nom_{i}")
            a["fecha_nac"] = c3.date_input("Nacido el", value=a["fecha_nac"], key=f"a_fn_{i}")

            st.metric("Edad calculada", edad(a["fecha_nac"]))

            a["hijo_de"] = st.text_input("Hijo de", key=f"a_hijo_{i}")
            a["profesion"] = st.text_input("Profesión", key=f"a_prof_{i}")
            a["domicilio"] = st.text_input("Domicilio", key=f"a_dom_{i}")
            a["instruccion"] = st.radio("Sabe leer/escribir", ["Sí", "No", "No informado"], key=f"a_inst_{i}", horizontal=True)

            foto_arrestado = st.file_uploader("Foto del arrestado para descripción externa", type=["jpg", "jpeg", "png"], key=f"foto_ar_{i}")

            if foto_arrestado and st.button(f"Describir arrestado con IA - {i+1}"):
                prompt = """
Generá una descripción policial breve y editable de vestimenta y aspecto externo visible.
No identifiques a la persona.
No describas lesiones.
No digas 'en la imagen se observa'.
Redacción directa para acta.
"""
                a["descripcion"] = llamar_ia_imagen(foto_arrestado, prompt)

            a["descripcion"] = st.text_area("Descripción externa validada", value=a["descripcion"], key=f"a_desc_{i}")

            st.subheader("Lesiones / asistencia médica")
            a["lesiones"] = st.radio("¿Resultó lesionado o refiere dolencias?", ["No", "Sí", "Pendiente"], key=f"a_les_{i}", horizontal=True)
            if a["lesiones"] == "Sí":
                a["lesion_detalle"] = st.text_input("Detalle sin diagnóstico policial", key=f"a_lesdet_{i}")
                a["traslado"] = st.radio("¿Fue trasladado a nosocomio?", ["No", "Sí", "Pendiente"], key=f"a_tras_{i}", horizontal=True)
                a["nosocomio"] = st.text_input("Nosocomio", key=f"a_noso_{i}")
                a["diagnostico"] = st.text_input("Diagnóstico médico informado", key=f"a_diag_{i}")
                a["certificado"] = st.radio("¿Se obtuvo certificado médico?", ["No", "Sí", "Pendiente"], key=f"a_cert_{i}", horizontal=True)

            st.subheader("Requisa")
            a["requisa"] = st.selectbox("Resultado de requisa", ["Pendiente", "No se realizó", "Sí, negativa", "Sí, positiva"], key=f"a_req_{i}")
            a["testigo_requisa"] = st.text_input("Testigo de requisa/secuestro", key=f"a_treq_{i}")
            a["urgencia_requisa"] = st.text_input("Justificación si no hubo testigo", key=f"a_urg_{i}")

    st.subheader("Secuestros / depósitos")

    with st.form("nuevo_secuestro"):
        vinculado = st.text_input("A quién pertenece / en poder de quién se halló")
        tipo = st.selectbox("Tipo", ["Arma de fuego", "Arma blanca", "Dinero", "Teléfono celular", "Efectos personales", "Otro"])
        caracter = st.selectbox("Carácter", ["Elemento de interés para la causa", "Depósito", "Pendiente"])
        foto_sec = st.file_uploader("Foto del secuestro o panorámica de efectos", type=["jpg", "jpeg", "png"])
        texto_sec = st.text_area("Redacción final del secuestro / depósito")

        analizar = st.form_submit_button("Agregar secuestro")

        if analizar:
            st.session_state.secuestros.append({
                "vinculado": vinculado,
                "tipo": tipo,
                "caracter": caracter,
                "texto": texto_sec
            })

    st.info("Para análisis IA de secuestro: cargue foto y use el generador debajo.")
    foto_sec_ia = st.file_uploader("Foto para analizar secuestro con IA", type=["jpg", "jpeg", "png"], key="sec_ia")
    if foto_sec_ia and st.button("Analizar secuestro con IA"):
        prompt = """
Describí técnicamente el elemento para acta policial.
Si son efectos personales, redactá directo sin decir que proviene de foto.
Sugerí si parece elemento de interés para la causa o depósito.
No afirmes calibre, funcionamiento o aptitud si no es verificable.
"""
        st.text_area("Descripción IA secuestro", llamar_ia_imagen(foto_sec_ia, prompt), height=240)

with tabs[2]:
    st.header("BLOQUE 3 — Inspección ocular, croquis y cámaras")

    st.info(
        "Se deja constancia que se toman vistas fotográficas, apuntes y relevamiento de cámaras del lugar, "
        "a los fines de la confección de la inspección ocular y croquis demostrativo que se agregan en foja siguiente."
    )
    st.warning("El protocolo requiere dejar constancia del relevamiento de cámaras o justificar su imposibilidad.")

    descripcion_lugar = st.text_area("Descripción técnica del lugar")

    vista1 = st.file_uploader("Vista 1 — Panorámica general", type=["jpg", "jpeg", "png"], key="v1")
    vista2 = st.file_uploader("Vista 2 — Media / relación", type=["jpg", "jpeg", "png"], key="v2")
    vista3 = st.file_uploader("Vista 3 — Detalle", type=["jpg", "jpeg", "png"], key="v3")
    vista4 = st.file_uploader("Vista 4 — Orientación / reconstrucción", type=["jpg", "jpeg", "png"], key="v4")

    if st.button("Generar descripción de inspección ocular con IA"):
        fotos = [x for x in [vista1, vista2, vista3, vista4] if x]
        if fotos:
            prompt = """
Generá una descripción técnica policial de inspección ocular con base en la vista aportada.
Redactá como constatación del personal actuante.
No digas 'en la imagen se observa'.
Incluí lugar, accesos, iluminación, daños, rastros, cámaras, indicios y relación espacial si surge.
"""
            resultado = llamar_ia_imagen(fotos[0], prompt)
            st.text_area("Descripción IA inspección", resultado, height=280)
        else:
            st.error("Cargue al menos una vista fotográfica.")

    camara_estado = st.selectbox("Relevamiento de cámaras", [
        "Sí, cámaras públicas",
        "Sí, cámaras privadas",
        "Sí, públicas y privadas",
        "No se observaron cámaras",
        "No fue posible relevar",
        "Pendiente"
    ])

    nueva_constancia = st.text_area("Constancia de cámara / material de interés")
    if st.button("Agregar constancia de cámara"):
        st.session_state.camara_constancias.append(nueva_constancia)

    croquis = st.text_area(
        "Croquis demostrativo",
        placeholder="Describa croquis no a escala: flecha norte, calles, veredas, lugar del hecho, aprehensión, secuestros, cámaras, dirección de fuga."
    )

with tabs[3]:
    st.header("BLOQUE 4 — Comunicación y cierre")

    via_comunicacion = st.selectbox("Vía de comunicación", [
        "Mesa de Enlace",
        "0800 MPA",
        "Fiscal directamente",
        "Pendiente",
        "No corresponde",
        "No se logró comunicación"
    ])

    hora_comunicacion = st.text_input("Hora de comunicación")
    medio = st.text_input("Medio utilizado")
    receptor = st.text_input("Persona que atendió")
    fiscal = st.text_input("Fiscal informado/interviniente")
    numero_comunicacion = st.text_input("Número de comunicación, si existe")
    directivas = st.text_area("Resolución / directivas recibidas")

    oficial_guardia = st.text_input("Oficial de Guardia que recibe")
    dependencia_receptora = st.text_input("Dependencia receptora")
    hora_entrega = st.text_input("Hora de entrega")

    documentos_entregados = st.multiselect("Actuaciones y elementos entregados", [
        "Acta de aprehensión",
        "Acta de procedimiento",
        "Acta de secuestro",
        "Cadena de custodia",
        "Inspección ocular",
        "Croquis demostrativo",
        "Fotografías",
        "Acta/s de entrevista/s",
        "Certificado/s médico/s",
        "Elementos secuestrados",
        "Efectos en carácter de depósito",
        "Capturas fotográficas de cámaras",
        "Filmación obtenida con teléfono celular",
        "Constancia de remisión por WhatsApp",
        "Constancia de comunicación con Mesa de Enlace / 0800 MPA / Fiscalía",
        "Otro"
    ])
    otros_entrega = st.text_input("Otros")

with tabs[4]:
    st.header("Vista final")

    data = locals()

    acta = generar_acta(data)
    inspeccion = generar_inspeccion(data)

    acta_editada = st.text_area("Acta principal editable", acta, height=420)
    inspeccion_editada = st.text_area("Inspección ocular editable", inspeccion, height=320)

    respaldo = {
        "acta": acta_editada,
        "inspeccion": inspeccion_editada,
        "victimas": st.session_state.victimas,
        "testigos": st.session_state.testigos,
        "arrestados": [{k: str(v) for k, v in a.items()} for a in st.session_state.arrestados],
        "secuestros": st.session_state.secuestros,
    }

    st.download_button("Descargar acta TXT", acta_editada, "acta_procedimiento.txt")
    st.download_button("Descargar inspección TXT", inspeccion_editada, "inspeccion_ocular.txt")
    st.download_button(
        "Descargar respaldo JSON",
        json.dumps(respaldo, ensure_ascii=False, indent=2),
        "respaldo_acta.json",
        "application/json"
    )
