import streamlit as st
from datetime import datetime, date
import json
import base64
import os
from io import BytesIO
from PIL import Image
import google.generativeai as genai

st.set_page_config(
    page_title="Acta Flagrancia SVI",
    layout="wide",
    page_icon="🚔"
)

# =====================================================
# CONFIGURACIÓN IA - GEMINI / RENDER
# =====================================================

def get_gemini_model():
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash-latest")


def ia_disponible():
    return get_gemini_model() is not None


def llamar_ia_texto(prompt):
    model = get_gemini_model()
    if model is None:
        return "IA no disponible. Configure GEMINI_API_KEY en Render Environment."

    sistema = (
        "Sos un asistente policial especializado en redacción de actas de procedimiento "
        "de la Policía de la Provincia de Santa Fe. Respondé en español formal, claro, "
        "operativo y con estilo de acta policial. No uses lenguaje de IA ni de formulario. "
        "No inventes datos. Si falta información, indicá que debe completarse."
    )

    try:
        resp = model.generate_content(f"{sistema}\n\n{prompt}")
        return resp.text.strip()
    except Exception as e:
        return f"Error IA Gemini: {e}"


def imagen_a_pil(uploaded_file):
    return Image.open(uploaded_file).convert("RGB")


def llamar_ia_imagen(uploaded_file, prompt):
    model = get_gemini_model()
    if model is None:
        return "IA no disponible. Configure GEMINI_API_KEY en Render Environment."

    sistema = (
        "Sos un asistente policial. Describís imágenes para actas en español formal. "
        "No identifiques personas. No diagnostiques lesiones. No digas 'en la imagen se observa'. "
        "Redactá como constatación policial validable por el personal actuante. "
        "No inventes marcas, numeraciones, calibres o datos no visibles."
    )

    try:
        img = imagen_a_pil(uploaded_file)
        resp = model.generate_content([sistema + "\n\n" + prompt, img])
        return resp.text.strip()
    except Exception as e:
        return f"Error IA imagen Gemini: {e}"


# =====================================================
# DATOS FIJOS / UTILIDADES
# =====================================================

MESES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

DEPENDENCIAS = [
    "COMANDO RADIOELÉCTRICO REGIONAL PÉREZ - ZAVALLA - SOLDINI",
    "COMANDO RADIOELÉCTRICO ROSARIO",
    "COMANDO RADIOELÉCTRICO FUNES",
    "COMISARÍA 22 PÉREZ",
    "COMISARÍA",
    "SUBCOMISARÍA",
    "B.O.U.",
    "G.T.M.",
    "OTRO",
]

DOCUMENTOS_ENTREGA = [
    "acta de aprehensión",
    "acta de procedimiento",
    "acta de secuestro",
    "cadena de custodia",
    "inspección ocular",
    "croquis demostrativo",
    "fotografías",
    "acta/s de entrevista/s",
    "certificado/s médico/s",
    "elementos secuestrados",
    "efectos en carácter de depósito",
    "capturas fotográficas de cámaras",
    "filmación obtenida con teléfono celular",
    "constancia de remisión por WhatsApp",
    "constancia de comunicación con Mesa de Enlace / 0800 MPA / Fiscalía",
    "otro",
]


def formato_fecha_larga(fecha):
    return f"{fecha.day} días del mes de {MESES[fecha.month]} del año {fecha.year}"


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
    ap = p.get("apellido", "").upper().strip()
    nom = p.get("nombre", "").upper().strip()
    dni = p.get("dni", "").strip()
    base = f"{ap}, {nom}".strip(", ")
    if dni and base:
        return f"{base}, DNI N° {dni}"
    return base or "persona no identificada"


def limpiar_texto(texto):
    return (texto or "").strip()


def agregar_arrestado():
    st.session_state.arrestados.append(
        {
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
        }
    )


def agregar_victima():
    st.session_state.victimas.append(
        {
            "apellido": "",
            "nombre": "",
            "dni": "",
            "domicilio": "",
            "telefono": "",
            "correo": "",
            "rol": "damnificado/a",
            "manifestacion": "",
        }
    )


def agregar_testigo():
    st.session_state.testigos.append(
        {
            "apellido": "",
            "nombre": "",
            "dni": "",
            "domicilio": "",
            "telefono": "",
            "correo": "",
            "rol": "testigo del hecho",
            "manifestacion": "",
        }
    )


def dependencia_texto(dependencia, dependencia_otro):
    return dependencia_otro.strip() if dependencia == "OTRO" and dependencia_otro.strip() else dependencia


def encabezado_institucional(data):
    dependencia = data["dependencia"]
    unidad_regional = limpiar_texto(data["unidad_regional"]) or "UR II"
    dependencia_manual = limpiar_texto(data["dependencia_otro"])

    if dependencia == "COMANDO RADIOELÉCTRICO REGIONAL PÉREZ - ZAVALLA - SOLDINI":
        return (
            "POLICÍA DE LA PROVINCIA DE SANTA FE\n"
            "COMANDO RADIOELÉCTRICO REGIONAL\n"
            f"PÉREZ - ZAVALLA - SOLDINI — {unidad_regional}"
        )

    if dependencia == "COMANDO RADIOELÉCTRICO ROSARIO":
        return (
            "POLICÍA DE LA PROVINCIA DE SANTA FE\n"
            f"COMANDO RADIOELÉCTRICO ROSARIO — {unidad_regional}"
        )

    if dependencia == "COMANDO RADIOELÉCTRICO FUNES":
        return (
            "POLICÍA DE LA PROVINCIA DE SANTA FE\n"
            f"COMANDO RADIOELÉCTRICO FUNES — {unidad_regional}"
        )

    if dependencia == "COMISARÍA 22 PÉREZ":
        return (
            "POLICÍA DE LA PROVINCIA DE SANTA FE\n"
            f"COMISARÍA 22 PÉREZ — {unidad_regional}"
        )

    if dependencia == "COMISARÍA":
        nombre_comisaria = dependencia_manual or "COMISARÍA"
        return (
            "POLICÍA DE LA PROVINCIA DE SANTA FE\n"
            f"{nombre_comisaria.upper()} — {unidad_regional}"
        )

    if dependencia == "SUBCOMISARÍA":
        nombre_sub = dependencia_manual or "SUBCOMISARÍA"
        return (
            "POLICÍA DE LA PROVINCIA DE SANTA FE\n"
            f"{nombre_sub.upper()} — {unidad_regional}"
        )

    if dependencia == "B.O.U.":
        return (
            "POLICÍA DE LA PROVINCIA DE SANTA FE\n"
            f"B.O.U. — {unidad_regional}"
        )

    if dependencia == "G.T.M.":
        return (
            "POLICÍA DE LA PROVINCIA DE SANTA FE\n"
            f"G.T.M. — {unidad_regional}"
        )

    if dependencia == "OTRO":
        return (
            "POLICÍA DE LA PROVINCIA DE SANTA FE\n"
            f"{(dependencia_manual or 'DEPENDENCIA A CONSIGNAR').upper()} — {unidad_regional}"
        )

    return (
        "POLICÍA DE LA PROVINCIA DE SANTA FE\n"
        f"{dependencia.upper()} — {unidad_regional}"
    )


def generar_encabezado(data):
    dep = dependencia_texto(data["dependencia"], data["dependencia_otro"])
    unidad_regional = limpiar_texto(data["unidad_regional"]) or "UR II"
    organismo = limpiar_texto(data["organismo_superior"]) or "A.U.O.P."
    ciudad = limpiar_texto(data["ciudad"]) or "Pérez"
    departamento = limpiar_texto(data["departamento"]) or "Rosario"
    provincia = limpiar_texto(data["provincia"]) or "Santa Fe"

    nro_acta = limpiar_texto(data["nro_acta"]) or "S/N"
    nro_inc = limpiar_texto(data["nro_incidencia"]) or "S/N"

    funcion_actuante = limpiar_texto(data["funcion_actuante"]) or "a cargo y chofer"
    personal = limpiar_texto(data["personal_actuante"]) or "personal actuante no consignado"
    refuerzo = limpiar_texto(data["refuerzo"])
    movil = limpiar_texto(data["movil"]) or "S/N"

    encabezado = []
    encabezado.append(encabezado_institucional(data))
    encabezado.append("")
    encabezado.append(f"Acta de procedimiento Nro. {nro_acta} / C.I. {nro_inc}")
    encabezado.append("")
    encabezado.append(
        f"En la ciudad de {ciudad}, departamento {departamento}, provincia de {provincia}, "
        f"a los {formato_fecha_larga(data['fecha'])}, siendo las {data['hora'].strftime('%H:%M')} horas, "
        f"el funcionario policial actuante quien suscribe {personal}, {funcion_actuante} de la unidad {movil}"
    )

    if refuerzo:
        encabezado[-1] += f", contando como refuerzo a {refuerzo}"

    encabezado[-1] += (
        f", perteneciente/s a {dep}, dependiente de {organismo} {unidad_regional}, "
        "a los fines legales que dieran lugar, SE HACE CONSTAR:"
    )

    return "\n".join(encabezado)


def generar_cuerpo_hecho(data):
    relato = limpiar_texto(data["relato"])
    if not relato:
        return (
            "Que en el día de la fecha, en circunstancias que deberán ser ampliadas por el personal actuante, "
            "se deja constancia de la intervención policial motivada por un hecho comunicado a la dependencia, "
            "quedando pendiente la ampliación circunstanciada del procedimiento."
        )

    return (
        "Que en el día de la fecha, en momentos en que personal actuante se encontraba en servicio, "
        f"se toma conocimiento de un hecho ocurrido en {data['lugar_hecho'] or 'lugar a determinar'}, "
        f"procediéndose a intervenir conforme las circunstancias que seguidamente se detallan: {relato}"
    )


def generar_personas_iniciales():
    partes = []

    for v in st.session_state.victimas:
        if any(limpiar_texto(v.get(k, "")) for k in ["apellido", "nombre", "manifestacion"]):
            partes.append(
                f"En el lugar se entrevista a {persona(v)}, domiciliado/a en {v.get('domicilio','')}, "
                f"teléfono {v.get('telefono','')}, quien en carácter de {v.get('rol','damnificado/a')} "
                f"manifiesta {v.get('manifestacion','')}."
            )

    for t in st.session_state.testigos:
        if any(limpiar_texto(t.get(k, "")) for k in ["apellido", "nombre", "manifestacion"]):
            partes.append(
                f"Asimismo, se entrevista a {persona(t)}, domiciliado/a en {t.get('domicilio','')}, "
                f"teléfono {t.get('telefono','')}, quien en carácter de {t.get('rol','testigo del hecho')} "
                f"manifiesta {t.get('manifestacion','')}."
            )

    return "\n".join(partes)


def generar_aprehendidos():
    partes = []

    for a in st.session_state.arrestados:
        if not any(limpiar_texto(str(a.get(k, ""))) for k in ["apellido", "nombre", "dni", "domicilio"]):
            continue

        partes.append(
            f"Seguidamente se procede a identificar al aprehendido como {persona(a)}, alias '{a.get('apodo','')}', "
            f"de estado civil {a.get('estado_civil','')}, nacido en fecha {a.get('fecha_nac')}, "
            f"de {edad(a.get('fecha_nac'))} años de edad, hijo de {a.get('hijo_de','')}, "
            f"de profesión {a.get('profesion','')}, domiciliado en {a.get('domicilio','')}, "
            f"quien manifiesta saber leer y escribir: {a.get('instruccion','')}."
        )

        if limpiar_texto(a.get("descripcion", "")):
            partes.append(
                f"Respecto de {persona(a)}, se deja constancia de su descripción externa y vestimenta: "
                f"{a.get('descripcion')}."
            )

        if a.get("lesiones") == "Sí":
            partes.append(
                f"Respecto de {persona(a)}, se deja constancia que {a.get('lesion_detalle','')}. "
                f"Consultado sobre asistencia médica, traslado a nosocomio: {a.get('traslado','')}; "
                f"nosocomio: {a.get('nosocomio','')}; diagnóstico informado por personal médico: "
                f"{a.get('diagnostico','')}; certificado médico: {a.get('certificado','')}."
            )

        if a.get("requisa") and a.get("requisa") != "Pendiente":
            partes.append(
                f"Practicada la medida correspondiente, se deja constancia que la requisa personal respecto de "
                f"{persona(a)} arroja como resultado: {a.get('requisa')}. "
                f"Testigo de requisa/secuestro: {a.get('testigo_requisa','')}. "
                f"En caso de ausencia de testigo, se deja asentada la siguiente justificación: "
                f"{a.get('urgencia_requisa','')}."
            )

    return "\n".join(partes)


def generar_secuestros():
    if not st.session_state.secuestros:
        return ""

    partes = []
    for s in st.session_state.secuestros:
        texto = limpiar_texto(s.get("texto", ""))
        if texto:
            partes.append(texto)

    return "\n".join(partes)


def generar_constancia_inspeccion():
    return (
        "Se deja constancia que se toman vistas fotográficas, apuntes y relevamiento de cámaras del lugar, "
        "a los fines de la confección de la inspección ocular y croquis demostrativo que se agregan en foja siguiente."
    )


def generar_comunicacion_y_cierre(data):
    entrega = ", ".join(data["documentos_entregados"])
    if data["otros_entrega"]:
        entrega = (entrega + ", " if entrega else "") + data["otros_entrega"]

    partes = []

    if data["via_comunicacion"] not in ["Pendiente", "No corresponde", "No se logró comunicación"]:
        partes.append(
            f"Seguidamente se entabla comunicación por vía {data['via_comunicacion']}, "
            f"siendo atendido por {data['receptor']}, fiscal informado/interviniente {data['fiscal']}, "
            f"a las {data['hora_comunicacion']} horas, recibiéndose la siguiente resolución y/o directiva: "
            f"{data['directivas']}."
        )
    elif data["via_comunicacion"] == "Pendiente":
        partes.append(
            "Se deja constancia que la comunicación con el MPA/Fiscalía queda pendiente de cumplimiento "
            "o ampliación, debiendo asentarse oportunamente la vía utilizada, receptor y directivas impartidas."
        )
    elif data["via_comunicacion"] == "No se logró comunicación":
        partes.append(
            "Se deja constancia que no se logró comunicación inmediata con MPA/Fiscalía, quedando asentada "
            "dicha circunstancia a los fines de su posterior regularización conforme protocolo."
        )

    partes.append(
        f"Se deja constancia que se hace entrega de las presentes actuaciones y elementos relacionados al procedimiento "
        f"al Oficial de Guardia {data['oficial_guardia']}, numerario de {data['dependencia_receptora']}, "
        f"consistentes en {entrega}, para su prosecución conforme trámite de rigor. "
        "No siendo para más, se da por finalizada la presente acta de procedimiento, previa íntegra lectura "
        "y ratificación de su contenido, firmando al pie para debida constancia.-"
    )

    return "\n".join(partes)


def generar_acta(data):
    secciones = [
        generar_encabezado(data),
        "",
        generar_cuerpo_hecho(data),
        "",
        generar_personas_iniciales(),
        "",
        generar_aprehendidos(),
        "",
        generar_secuestros(),
        "",
        generar_constancia_inspeccion(),
        "",
        generar_comunicacion_y_cierre(data),
    ]

    texto = "\n".join([s for s in secciones if limpiar_texto(s)])
    return texto.replace("\n\n\n", "\n\n")


def generar_inspeccion(data):
    texto = []
    texto.append("ACTA DE INSPECCIÓN OCULAR Y CROQUIS DEMOSTRATIVO")
    texto.append("")
    texto.append(
        f"En la ciudad de {data['ciudad']}, departamento {data['departamento']}, provincia de {data['provincia']}, "
        f"a los {formato_fecha_larga(data['fecha'])}, siendo las {data['hora'].strftime('%H:%M')} horas, "
        f"personal actuante se constituye en {data['lugar_hecho']}, a los fines de realizar inspección ocular, "
        "toma de apuntes, vistas fotográficas, relevamiento de cámaras y croquis demostrativo."
    )

    texto.append("")
    texto.append("DESCRIPCIÓN TÉCNICA DEL LUGAR:")
    texto.append(data["descripcion_lugar"] or "Pendiente de descripción técnica del lugar.")

    texto.append("")
    texto.append("VISTAS FOTOGRÁFICAS:")
    texto.append("Vista N° 1: panorámica general del lugar del hecho.")
    texto.append("Vista N° 2: vista media o de relación entre sectores relevantes.")
    texto.append("Vista N° 3: vista de detalle de rastros, daños, indicios o elementos de interés.")
    texto.append("Vista N° 4: vista de orientación o reconstrucción del recorrido, fuga o aprehensión.")

    texto.append("")
    texto.append("RELEVAMIENTO DE CÁMARAS:")
    texto.append(data["camara_estado"])
    for c in st.session_state.camara_constancias:
        if limpiar_texto(c):
            texto.append(c)

    texto.append("")
    texto.append("CROQUIS DEMOSTRATIVO:")
    texto.append(
        data["croquis"]
        or "Se confecciona croquis demostrativo no a escala, con indicación de arterias, orientación, punto del hecho, lugar de aprehensión, secuestros, cámaras y dirección de fuga si correspondiere."
    )

    texto.append("")
    texto.append(
        "No siendo para más, se da por finalizada la presente inspección ocular, quedando las vistas fotográficas, "
        "apuntes y croquis demostrativo agregados a las actuaciones correspondientes.-"
    )

    return "\n".join(texto)


# =====================================================
# INTERFAZ
# =====================================================

inicializar()

st.title("🚔 Asistente de Actas en Flagrancia")
st.caption("Creado por SubComisario CASTAÑEDA Juan")

if ia_disponible():
    st.success("IA activa: GEMINI_API_KEY detectada en Render.")
else:
    st.warning("IA no activa: falta GEMINI_API_KEY en Render Environment.")

tabs = st.tabs(["1. Encabezado", "2. Arrestado", "3. Inspección", "4. Cierre", "Vista final"])

with tabs[0]:
    st.header("BLOQUE 1 — Encabezado, relato, víctimas y testigos")

    st.subheader("Encabezado institucional dinámico")
    c1, c2, c3 = st.columns(3)

    ciudad = c1.text_input("Ciudad", value="Pérez")
    departamento = c2.text_input("Departamento", value="Rosario")
    provincia = c3.text_input("Provincia", value="Santa Fe")

    unidad_regional = c1.text_input("Unidad Regional", value="UR II")
    organismo_superior = c2.text_input("Organismo superior", value="A.U.O.P.")
    funcion_actuante = c3.text_input("Función del actuante", value="a cargo y chofer")

    st.subheader("Datos del acta")
    c1, c2 = st.columns(2)

    nro_acta = c1.text_input("Acta de procedimiento Nro.", placeholder="Ej: 442/2026")
    nro_incidencia = c2.text_input("C.I. / Nro. de Incidencia", placeholder="Ej: 34982734")

    dependencia = c1.selectbox("Dependencia", DEPENDENCIAS)
    dependencia_otro = c2.text_input(
        "Dependencia manual si corresponde",
        placeholder="Ej: COMISARÍA 13 ROSARIO / SUBCOMISARÍA 18 / otra dependencia"
    )

    personal_actuante = c1.text_input("Funcionario policial actuante", placeholder="SUB INSPECTOR CANCIANI CARINA")
    refuerzo = c2.text_input("Refuerzo / colaboración", placeholder="SOP GATTI MARTÍN")
    movil = c1.text_input("Unidad / Móvil", placeholder="10802")

    fecha = c1.date_input("Fecha", date.today())
    hora = c2.time_input("Hora", datetime.now().time().replace(second=0, microsecond=0))

    lugar_hecho = c1.text_input("Lugar del hecho")
    lugar_aprehension = c2.text_input("Lugar de la aprehensión")

    st.subheader("Relato base")
    relato = st.text_area(
        "Ingrese o dicte lo ocurrido",
        placeholder=(
            "Relate brevemente qué ocurrió, dónde, cuándo y cómo intervino el personal policial. "
            "El acta final lo incorporará como redacción corrida luego de SE HACE CONSTAR."
        ),
        height=160,
    )

    if st.button("Analizar relato con IA"):
        prompt = f"""
Analizá este relato policial y devolvé en formato claro:
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
12. Propuesta de redacción policial corrida, sin poner título 'Relato del hecho' y empezando con 'Que...'.

Relato:
{relato}
"""
        st.text_area("Resultado IA del relato", llamar_ia_texto(prompt), height=320)

    st.subheader("Víctima/s o damnificado/s")
    if st.button("Agregar víctima / damnificado"):
        agregar_victima()

    for i, v in enumerate(st.session_state.victimas):
        with st.expander(f"Víctima/Damnificado {i+1}: {persona(v)}", expanded=True):
            c1, c2 = st.columns(2)
            v["apellido"] = c1.text_input("Apellido", value=v.get("apellido", ""), key=f"v_ap_{i}")
            v["nombre"] = c2.text_input("Nombre", value=v.get("nombre", ""), key=f"v_nom_{i}")
            v["dni"] = c1.text_input("DNI", value=v.get("dni", ""), key=f"v_dni_{i}")
            v["domicilio"] = c2.text_input("Domicilio", value=v.get("domicilio", ""), key=f"v_dom_{i}")
            v["telefono"] = c1.text_input("Teléfono", value=v.get("telefono", ""), key=f"v_tel_{i}")
            v["correo"] = c2.text_input("Correo", value=v.get("correo", ""), key=f"v_cor_{i}")
            v["rol"] = st.text_input("Rol", value=v.get("rol", "damnificado/a"), key=f"v_rol_{i}")
            v["manifestacion"] = st.text_area("Qué manifestó", value=v.get("manifestacion", ""), key=f"v_man_{i}")

    st.subheader("Testigo/s del hecho")
    if st.button("Agregar testigo del hecho"):
        agregar_testigo()

    for i, t in enumerate(st.session_state.testigos):
        with st.expander(f"Testigo {i+1}: {persona(t)}", expanded=True):
            c1, c2 = st.columns(2)
            t["apellido"] = c1.text_input("Apellido", value=t.get("apellido", ""), key=f"t_ap_{i}")
            t["nombre"] = c2.text_input("Nombre", value=t.get("nombre", ""), key=f"t_nom_{i}")
            t["dni"] = c1.text_input("DNI", value=t.get("dni", ""), key=f"t_dni_{i}")
            t["domicilio"] = c2.text_input("Domicilio", value=t.get("domicilio", ""), key=f"t_dom_{i}")
            t["telefono"] = c1.text_input("Teléfono", value=t.get("telefono", ""), key=f"t_tel_{i}")
            t["correo"] = c2.text_input("Correo", value=t.get("correo", ""), key=f"t_cor_{i}")
            t["rol"] = st.text_input("Rol", value=t.get("rol", "testigo del hecho"), key=f"t_rol_{i}")
            t["manifestacion"] = st.text_area("Qué observó o informó", value=t.get("manifestacion", ""), key=f"t_man_{i}")

with tabs[1]:
    st.header("BLOQUE 2 — Arrestado")

    if st.button("Agregar arrestado"):
        agregar_arrestado()

    if not st.session_state.arrestados:
        st.info("Agregue arrestados si corresponde. La referencia Arrestado 1/2 será solo interna y no aparecerá en el acta final.")

    for i, a in enumerate(st.session_state.arrestados):
        with st.expander(f"Arrestado {i+1} — {persona(a)}", expanded=True):
            st.caption("Arrestado 1/2 es solo referencia interna. En el acta se redacta con nombre, apellido y DNI.")

            a["dictado"] = st.text_area("Dictado rápido opcional", value=a.get("dictado", ""), key=f"a_dic_{i}")

            if st.button(f"Procesar dictado con IA - Arrestado {i+1}"):
                prompt = f"""
Separá este dictado en datos filiatorios:
DNI, apodo, apellido, nombre, estado civil, fecha nacimiento, hijo de, profesión, domicilio, instrucción.
Devolvé también una redacción policial breve de identificación.

Dictado:
{a['dictado']}
"""
                st.text_area(f"Resultado IA dictado arrestado {i+1}", llamar_ia_texto(prompt), height=240)

            c1, c2, c3 = st.columns(3)
            a["dni"] = c1.text_input("DNI", value=a.get("dni", ""), key=f"a_dni_{i}")
            a["apodo"] = c2.text_input("Apodo", value=a.get("apodo", ""), key=f"a_apodo_{i}")
            a["estado_civil"] = c3.selectbox(
                "Estado civil",
                ["Soltero", "Casado", "Divorciado", "Viudo", "Unión convivencial", "No informado"],
                key=f"a_ec_{i}",
            )

            a["apellido"] = c1.text_input("Apellido", value=a.get("apellido", ""), key=f"a_ap_{i}")
            a["nombre"] = c2.text_input("Nombre", value=a.get("nombre", ""), key=f"a_nom_{i}")
            a["fecha_nac"] = c3.date_input("Nacido el", value=a.get("fecha_nac", date(1998, 5, 15)), key=f"a_fn_{i}")

            st.metric("Edad calculada", edad(a["fecha_nac"]))

            a["hijo_de"] = st.text_input("Hijo de", value=a.get("hijo_de", ""), key=f"a_hijo_{i}")
            a["profesion"] = st.text_input("Profesión", value=a.get("profesion", ""), key=f"a_prof_{i}")
            a["domicilio"] = st.text_input("Domicilio", value=a.get("domicilio", ""), key=f"a_dom_{i}")
            a["instruccion"] = st.radio(
                "Sabe leer/escribir",
                ["Sí", "No", "No informado"],
                key=f"a_inst_{i}",
                horizontal=True,
            )

            foto_arrestado = st.file_uploader(
                "Foto del arrestado para descripción externa",
                type=["jpg", "jpeg", "png"],
                key=f"foto_ar_{i}",
            )

            if foto_arrestado and st.button(f"Describir arrestado con IA - {i+1}"):
                prompt = """
Generá una descripción policial breve y editable de vestimenta y aspecto externo visible.
No identifiques a la persona.
No describas lesiones.
No digas 'en la imagen se observa'.
Redacción directa para acta.
"""
                a["descripcion"] = llamar_ia_imagen(foto_arrestado, prompt)

            a["descripcion"] = st.text_area(
                "Descripción externa validada",
                value=a.get("descripcion", ""),
                key=f"a_desc_{i}",
            )

            st.subheader("Lesiones / asistencia médica")
            a["lesiones"] = st.radio(
                "¿Resultó lesionado o refiere dolencias?",
                ["No", "Sí", "Pendiente"],
                key=f"a_les_{i}",
                horizontal=True,
            )
            if a["lesiones"] == "Sí":
                a["lesion_detalle"] = st.text_input("Detalle sin diagnóstico policial", value=a.get("lesion_detalle", ""), key=f"a_lesdet_{i}")
                a["traslado"] = st.radio("¿Fue trasladado a nosocomio?", ["No", "Sí", "Pendiente"], key=f"a_tras_{i}", horizontal=True)
                a["nosocomio"] = st.text_input("Nosocomio", value=a.get("nosocomio", ""), key=f"a_noso_{i}")
                a["diagnostico"] = st.text_input("Diagnóstico médico informado", value=a.get("diagnostico", ""), key=f"a_diag_{i}")
                a["certificado"] = st.radio("¿Se obtuvo certificado médico?", ["No", "Sí", "Pendiente"], key=f"a_cert_{i}", horizontal=True)

            st.subheader("Requisa")
            a["requisa"] = st.selectbox(
                "Resultado de requisa",
                ["Pendiente", "No se realizó", "Sí, negativa", "Sí, positiva"],
                key=f"a_req_{i}",
            )
            a["testigo_requisa"] = st.text_input("Testigo de requisa/secuestro", value=a.get("testigo_requisa", ""), key=f"a_treq_{i}")
            a["urgencia_requisa"] = st.text_input("Justificación si no hubo testigo", value=a.get("urgencia_requisa", ""), key=f"a_urg_{i}")

    st.subheader("Secuestros / depósitos")

    with st.form("nuevo_secuestro"):
        vinculado = st.text_input("A quién pertenece / en poder de quién se halló")
        tipo = st.selectbox("Tipo", ["Arma de fuego", "Arma blanca", "Dinero", "Teléfono celular", "Efectos personales", "Otro"])
        caracter = st.selectbox("Carácter", ["Elemento de interés para la causa", "Depósito", "Pendiente"])
        st.file_uploader("Foto del secuestro o panorámica de efectos", type=["jpg", "jpeg", "png"])
        texto_sec = st.text_area(
            "Redacción final del secuestro / depósito",
            placeholder=(
                "Ej: Respecto de PÉREZ, JUAN, DNI N° 12.345.678, se deja constancia del resguardo "
                "en carácter de depósito de una billetera color negro, un juego de llaves, documentación personal "
                "y un teléfono celular color negro, elementos que quedan individualizados y bajo custodia."
            ),
        )

        if st.form_submit_button("Agregar secuestro"):
            st.session_state.secuestros.append(
                {
                    "vinculado": vinculado,
                    "tipo": tipo,
                    "caracter": caracter,
                    "texto": texto_sec,
                }
            )

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

    descripcion_lugar = st.text_area("Descripción técnica del lugar", height=140)

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

    camara_estado = st.selectbox(
        "Relevamiento de cámaras",
        [
            "Sí, cámaras públicas",
            "Sí, cámaras privadas",
            "Sí, públicas y privadas",
            "No se observaron cámaras",
            "No fue posible relevar",
            "Pendiente",
        ],
    )

    nueva_constancia = st.text_area("Constancia de cámara / material de interés")
    if st.button("Agregar constancia de cámara"):
        st.session_state.camara_constancias.append(nueva_constancia)

    croquis = st.text_area(
        "Croquis demostrativo",
        placeholder=(
            "Describa croquis no a escala: flecha norte, calles, veredas, lugar del hecho, "
            "aprehensión, secuestros, cámaras, dirección de fuga."
        ),
        height=140,
    )

with tabs[3]:
    st.header("BLOQUE 4 — Comunicación y cierre")

    via_comunicacion = st.selectbox(
        "Vía de comunicación",
        ["Mesa de Enlace", "0800 MPA", "Fiscal directamente", "Pendiente", "No corresponde", "No se logró comunicación"],
    )

    hora_comunicacion = st.text_input("Hora de comunicación")
    medio = st.text_input("Medio utilizado")
    receptor = st.text_input("Persona que atendió")
    fiscal = st.text_input("Fiscal informado/interviniente")
    numero_comunicacion = st.text_input("Número de comunicación, si existe")
    directivas = st.text_area("Resolución / directivas recibidas")

    oficial_guardia = st.text_input("Oficial de Guardia que recibe")
    dependencia_receptora = st.text_input("Dependencia receptora")
    hora_entrega = st.text_input("Hora de entrega")

    documentos_entregados = st.multiselect("Actuaciones y elementos entregados", DOCUMENTOS_ENTREGA)
    otros_entrega = st.text_input("Otros")

with tabs[4]:
    st.header("Vista final")

    data = {
        "ciudad": ciudad,
        "departamento": departamento,
        "provincia": provincia,
        "unidad_regional": unidad_regional,
        "organismo_superior": organismo_superior,
        "funcion_actuante": funcion_actuante,
        "nro_acta": nro_acta,
        "nro_incidencia": nro_incidencia,
        "dependencia": dependencia,
        "dependencia_otro": dependencia_otro,
        "personal_actuante": personal_actuante,
        "refuerzo": refuerzo,
        "movil": movil,
        "fecha": fecha,
        "hora": hora,
        "lugar_hecho": lugar_hecho,
        "lugar_aprehension": lugar_aprehension,
        "relato": relato,
        "descripcion_lugar": descripcion_lugar,
        "camara_estado": camara_estado,
        "croquis": croquis,
        "via_comunicacion": via_comunicacion,
        "hora_comunicacion": hora_comunicacion,
        "medio": medio,
        "receptor": receptor,
        "fiscal": fiscal,
        "numero_comunicacion": numero_comunicacion,
        "directivas": directivas,
        "oficial_guardia": oficial_guardia,
        "dependencia_receptora": dependencia_receptora,
        "hora_entrega": hora_entrega,
        "documentos_entregados": documentos_entregados,
        "otros_entrega": otros_entrega,
    }

    acta = generar_acta(data)
    inspeccion = generar_inspeccion(data)

    st.subheader("Acta principal editable")
    acta_editada = st.text_area("Acta principal", acta, height=520)

    st.subheader("Inspección ocular editable")
    inspeccion_editada = st.text_area("Inspección ocular", inspeccion, height=360)

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
        "application/json",
    )
