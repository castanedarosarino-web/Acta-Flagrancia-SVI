import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN DE SEGURIDAD ---
st.set_page_config(page_title="SVI - Original 10bis", layout="wide")

st.markdown("""
    <style>
    .stHeader { background-color: #002d52; }
    .stButton>button { border-radius: 5px; height: 3em; background-color: #002d52; color: white; font-weight: bold; }
    .reportview-container { background: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema SVI: Acta de Procedimiento")
st.caption("Autoría: SubComisario Castañeda Juan | Versión Táctica Robusta")

# --- MEMORIA DEL SISTEMA ---
if 'relato' not in st.session_state: st.session_state.relato = ""

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs(["📝 RELATO", "👥 SUJETOS", "📦 SECUESTROS", "📄 ACTA FINAL"])

with tab1:
    st.subheader("📍 Inicio y Narrativa")
    col1, col2 = st.columns(2)
    with col1:
        cuij = st.text_input("CUIJ / Nro Acta", placeholder="Ej: 21-000456-1")
        dependencia = st.selectbox("Unidad Operativa", ["Comisaría 22°", "Subcomisaría 18°", "Comando Radioeléctrico", "PAT"])
    with col2:
        lugar = st.text_input("Lugar del Hecho")
        preventor = st.text_input("Oficial Actuante", value="SubComisario Castañeda Juan")

    st.info("🎙️ Use el dictado por voz de su teclado para el relato 'en caliente'.")
    relato_raw = st.text_area("Describa el hecho (sin filtros):", height=150)
    
    if st.button("✨ PROFESIONALIZAR TEXTO"):
        # Diccionario táctico de traducción
        traduccion = {
            "vago": "masculino", "fierro": "arma de fuego", "chata": "unidad móvil",
            "le dimos la voz de alto": "se le imparte la voz de alto policía",
            "se dio a la fuga": "emprende veloz carrera", "lo enganchamos": "se logra la aprehensión"
        }
        texto_limpio = relato_raw.lower()
        for k, v in traduccion.items():
            texto_limpio = texto_limpio.replace(k, v)
        st.session_state.relato = texto_limpio.capitalize()
        st.success("Relato convertido a lenguaje policial.")

with tab2:
    st.subheader("👥 Identificación de Aprehendidos")
    # OPCIÓN B: Carga de archivos (esto abre la cámara del celu o la galería)
    foto_det = st.file_uploader("Capturar Foto del Detenido", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)
    if foto_det:
        st.image(foto_det, caption="Imagen registrada correctamente", width=300)
    
    nombre_det = st.text_input("Nombre y Apellido")
    dni_det = st.text_input("DNI / Documento")
    desc_det = st.text_area("Descripción física / Vestimenta")

with tab3:
    st.subheader("📦 Secuestros e Inspección")
    foto_sec = st.file_uploader("Capturar Foto del Secuestro / Lugar", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    if foto_sec:
        st.write(f"✅ {len(foto_sec)} imágenes cargadas.")
    
    detalles_sec = st.text_area("Detalle de los elementos secuestrados (Marcas, numeración, estado):")

with tab4:
    st.subheader("📄 Acta de Procedimiento Consolidada")
    
    ahora = datetime.now()
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    cuerpo_acta = f"""En la ciudad de Pérez, Provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} de {ahora.year}, siendo las {ahora.strftime('%H:%M')} horas, el que suscribe {preventor.upper()}, personal policial de la {dependencia}, hace constar: Que en circunstancias de encontrarse en cumplimiento de funciones específicas, más precisamente en {lugar}, se procede a lo siguiente: {st.session_state.relato}. 

Seguidamente, se procede a la identificación del involucrado como {nombre_det.upper()}, DNI {dni_det}, quien vestía {desc_det}. Asimismo, se hace constar el SECUESTRO de: {detalles_sec}. 

Se labra la presente para su remisión a la fiscalía en turno, previa lectura y ratificación."""

    st.code(cuerpo_acta, language=None)
    st.button("📋 COPIAR PARA WHATSAPP / SIGE")
