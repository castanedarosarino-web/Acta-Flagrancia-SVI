import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN DE SEGURIDAD Y ESTILO ---
st.set_page_config(page_title="SVI - Procedimiento Profesional", layout="wide")

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 5px; }
    .stTabs [aria-selected="true"] { background-color: #002d52 !important; color: white !important; }
    .stExpander { border: 1px solid #002d52; border-radius: 10px; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema SVI: Acta de Procedimiento")
st.caption("Autoría: SubComisario Castañeda Juan | Estándar de Filiación Completa")

# --- MEMORIA OPERATIVA ---
if 'relato_final' not in st.session_state: st.session_state.relato_final = ""

tab1, tab2, tab3, tab4 = st.tabs(["📝 RELATO", "👥 FILIACIÓN DETENIDOS", "📦 SECUESTROS", "📄 ACTA FINAL"])

# --- TAB 1: NARRATIVA ---
with tab1:
    st.subheader("📍 Inicio del Procedimiento")
    c1, c2 = st.columns(2)
    with c1:
        cuij = st.text_input("CUIJ / Nro Acta", value="21-")
        dependencia = st.selectbox("Unidad Operativa", ["Comisaría 22°", "Subcomisaría 18°", "Comando Pérez", "PAT"])
    with c2:
        lugar = st.text_input("Lugar del Hecho (Calle, Altura, Localidad)")
        preventor = st.text_input("Oficial Actuante", value="SubComisario Castañeda Juan")

    relato_raw = st.text_area("Dictado del hecho:", height=150)
    if st.button("✨ PROFESIONALIZAR"):
        # Lógica de traducción técnica
        t = relato_raw.lower().replace("vago", "masculino").replace("fierro", "arma de fuego")
        st.session_state.relato_final = t.capitalize()
        st.success("Relato técnico generado.")

# --- TAB 2: FILIACIÓN COMPLETA (MODELO 10 BIS) ---
with tab2:
    st.subheader("👤 Datos de los Aprehendidos")
    cant_det = st.number_input("Cantidad de sujetos a identificar", min_value=1, max_value=10, value=1)
    
    lista_detenidos = []
    
    for i in range(cant_det):
        with st.expander(f"FORMULARIO DE FILIACIÓN - SUJETO N° {i+1}", expanded=True):
            # FOTO PRIMERO (Opción B: Robusta)
            foto = st.file_uploader(f"Capturar Fotografía (Sujeto {i+1})", type=['jpg','jpeg','png'], key=f"f_{i}")
            if foto: st.image(foto, width=150)
            
            # FILA 1: Identidad Básica
            f1_c1, f1_c2, f1_c3, f1_c4 = st.columns([2, 3, 3, 2])
            dni = f1_c1.text_input("DNI", key=f"dni_{i}")
            ape = f1_c2.text_input("Apellido", key=f"ape_{i}")
            nom = f1_c3.text_input("Nombre", key=f"nom_{i}")
            apo = f1_c4.text_input("Apodo", key=f"apo_{i}")
            
            # FILA 2: Familia y Origen
            f2_c1, f2_c2, f2_c3, f2_c4 = st.columns(4)
            papa = f2_c1.text_input("Hijo de (Padre)", key=f"pa_{i}")
            mama = f2_c2.text_input("Hijo de (Madre)", key=f"ma_{i}")
            ciudad = f2_c3.text_input("Ciudad Nac.", key=f"ciu_{i}")
            prov = f2_c4.text_input("Provincia", key=f"prov_{i}")
            
            # FILA 3: Datos Personales
            f3_c1, f3_c2, f3_c3, f3_c4, f3_c5 = st.columns([1,1,1,2,2])
            edad = f3_c1.text_input("Edad", key=f"ed_{i}")
            est_civil = f3_c2.selectbox("Est. Civil", ["Soltero/a", "Casado/a", "Divorciado/a", "Conviviente"], key=f"ec_{i}")
            instruccion = f3_c3.selectbox("Lee/Escribe", ["SI", "NO"], key=f"le_{i}")
            profesion = f3_c4.text_input("Profesión/Oficio", key=f"prof_{i}")
            domicilio = f3_c5.text_input("Domicilio Real", key=f"dom_{i}")
            
            lista_detenidos.append({
                "full": f"{ape} {nom}", "dni": dni, "dom": domicilio, "padres": f"{papa} y {mama}",
                "datos": f"{edad} años, {est_civil}, instruido ({instruccion}), de ocupación {profesion}"
            })

# --- TAB 3: SECUESTROS ---
with tab3:
    st.subheader("📦 Secuestros e Inspección Ocular")
    st.file_uploader("Fotos del Secuestro / Evidencia", type=['jpg','png'], accept_multiple_files=True)
    detalles_sec = st.text_area("Detalle técnico de los elementos secuestrados:")

# --- TAB 4: ACTA FINAL ---
with tab4:
    st.subheader("📄 Acta de Procedimiento Consolidada")
    ahora = datetime.now()
    
    # Construcción del párrafo de detenidos
    texto_sujetos = ""
    for d in lista_detenidos:
        texto_sujetos += f"el llamado {d['full'].upper()}, DNI {d['dni']}, hijo de {d['padres']}, de {d['datos']}, domiciliado en {d['dom']}; "

    acta = f"""En la ciudad de Pérez, a los {ahora.day} días del mes de Abril de {ahora.year}, siendo las {ahora.strftime('%H:%M')} horas, el suscripto {preventor.upper()}, personal de la {dependencia}, hace constar: Que en circunstancias de {st.session_state.relato_final}, en {lugar}. 

Que ante lo expuesto, se procede a la identificación y aprehensión de: {texto_sujetos}

Se procede al SECUESTRO de: {detalles_sec}. 

Se da por finalizada la presente, previa lectura y ratificación de los intervinientes."""

    st.code(acta, language=None)
    st.button("📋 COPIAR ACTA")
