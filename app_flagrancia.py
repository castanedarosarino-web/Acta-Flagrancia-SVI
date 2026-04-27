import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="SVI - Acta Policial Perfecta", layout="wide")

# Estilo para simular entorno profesional
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #002d52; color: white; }
    .stTextArea>div>div>textarea { font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema SVI: Acta de Procedimiento")
st.caption("Autoría: SubComisario Castañeda Juan | Jurisdicción UR II")

# --- INICIALIZACIÓN DE MEMORIA (EL MASTICADOR) ---
if 'pasaje_datos' not in st.session_state:
    st.session_state['pasaje_datos'] = {}

# --- PESTAÑAS OPERATIVAS ---
tab_acta, tab_sujetos, tab_secuestro, tab_inspeccion, tab_final = st.tabs([
    "1. Inicio y Relato", 
    "2. Detenidos", 
    "3. Secuestros/Salud", 
    "4. Inspección Ocular",
    "📄 ACTA FINAL"
])

# --- TAB 1: INICIO Y RELATO ---
with tab_acta:
    st.header("📍 Inicio del Procedimiento")
    col1, col2 = st.columns(2)
    with col1:
        cuij = st.text_input("CUIJ / Nro Acta", placeholder="Ej: 221/26")
        dependencia = st.selectbox("Dependencia", ["Comisaría 22°", "Subcomisaría 18°", "Comisaría 6°", "Comisaría 2°"])
    with col2:
        preventor = st.text_input("Preventor Actuante", value="SubComisario Castañeda Juan")
        lugar = st.text_input("Lugar del Hecho (Calle e Intersección)")

    st.subheader("🎙️ Relato del Hecho (Nudo)")
    st.info("Puede usar el micrófono de su teclado móvil para dictar.")
    relato_crudo = st.text_area("Describa lo sucedido (Adrenalina/Gritos/Corridas):", height=200)
    
    if st.button("✨ PROFESIONALIZAR RELATO"):
        # Diccionario de pulido automático
        reemplazos = {
            "el vago": "el masculino", "tiro": "arroja", "se escapo": "emprende fuga",
            "le pegue": "fuerza mínima", "la chata": "el móvil policial", "vimos": "se observa",
            "en cana": "detenido", "fierro": "arma de fuego"
        }
        texto_pulido = relato_crudo.lower()
        for k, v in reemplazos.items():
            texto_pulido = texto_pulido.replace(k, v)
        st.session_state['relato_final'] = texto_pulido.capitalize()
        st.success("Relato pulido para el acta.")

# --- TAB 2: DETENIDOS ---
with tab_sujetos:
    st.header("👥 Identificación de Aprehendidos")
    cant_det = st.number_input("¿Cuántos detenidos?", min_value=0, max_value=10, step=1)
    
    detenidos_data = []
    for i in range(cant_det):
        st.markdown(f"---")
        col_foto, col_datos = st.columns([1, 2])
        with col_foto:
            foto_det = st.camera_input(f"Foto Detenido {i+1}", key=f"fdet_{i}")
        with col_datos:
            nom = st.text_input(f"Nombre y Apellido", key=f"ndet_{i}")
            dni = st.text_input(f"DNI", key=f"ddet_{i}")
            desc_fisica = st.text_area(f"Descripción (Use la foto de referencia):", key=f"desdet_{i}")
            detenidos_data.append({"nombre": nom, "dni": dni, "desc": desc_fisica})
    st.session_state['detenidos'] = detenidos_data

# --- TAB 3: SECUESTROS Y SALUD ---
with tab_secuestro:
    st.header("📦 Secuestros e Integridad")
    
    col_sec, col_sal = st.columns(2)
    
    with col_sec:
        st.subheader("Elementos de Interés")
        hay_secuestro = st.checkbox("¿Hay elementos secuestrados?")
        secuestros_lista = []
        if hay_secuestro:
            n_obj = st.number_input("Cantidad de objetos", 1, 5)
            for j in range(n_obj):
                f_obj = st.camera_input(f"Foto Objeto {j+1}", key=f"fobj_{j}")
                d_obj = st.text_area(f"Descripción técnica del objeto {j+1}:", key=f"dobj_{j}")
                secuestros_lista.append(d_obj)
        st.session_state['secuestros'] = secuestros_lista

        pertenencias = st.text_area("Pertenencias en Depósito (Billetera, llaves, etc):")
        st.session_state['pertenencias'] = pertenencias

    with col_sal:
        st.subheader("Integridad Física")
        lesiones_det = st.selectbox("¿Detenido con lesiones?", ["No presenta", "Previas", "Por la aprehensión"])
        asistencia = st.checkbox("¿Hubo asistencia médica?")
        medico = ""
        if asistencia:
            medico = st.text_input("Médico / Hospital")
        
        lesion_policial = st.checkbox("¿Personal policial lesionado?")
        det_lesion_pol = ""
        if lesion_policial:
            det_lesion_pol = st.text_area("Detalle lesión del personal:")
        
        st.session_state['salud'] = {
            "estado": lesiones_det, "medico": medico, 
            "policial": det_lesion_pol, "asistencia": asistencia
        }

# --- TAB 4: INSPECCIÓN OCULAR ---
with tab_inspeccion:
    st.header("🔍 Inspección Ocular (Protocolo)")
    st.info("Estas fotos generan el acta separada automáticamente.")
    c1, c2 = st.columns(2)
    with c1:
        f_pan = st.camera_input("Foto Panorámica")
        ilum = st.selectbox("Iluminación", ["Buena", "Deficiente", "Nula"])
    with c2:
        desc_lugar = st.text_area("Descripción del entorno (IA asiste):", 
                                 value="Lugar de visibilidad normal, asfalto seco, zona urbana...")
        st.session_state['inspeccion'] = desc_lugar

# --- TAB 5: GENERACIÓN FINAL (EL BLOQUE) ---
with tab_final:
    st.header("📄 Documentos Listos")
    
    # Lógica de construcción del Párrafo Único
    fecha = datetime.now()
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    # 1. ACTA DE PROCEDIMIENTO
    cuerpo = f"En la ciudad de Pérez, Departamento Rosario, Provincia de Santa Fe, a los {fecha.day} días del mes de {meses[fecha.month-1]} de {fecha.year}, siendo las {fecha.strftime('%H:%M')} horas, el suscripto {preventor.upper()}, con prestación de servicios en la {dependencia} de la UR II, hace constar que: En circunstancias de {st.session_state.get('relato_final', '...')}."
    
    if st.session_state.get('detenidos'):
        cuerpo += " Se procede a la aprehensión de: "
        for d in st.session_state['detenidos']:
            cuerpo += f"{d['nombre'].upper()} (DNI: {d['dni']}), {d['desc']}. "
            
    if st.session_state.get('secuestros'):
        cuerpo += " Se procede al SECUESTRO de interés para la causa de: "
        for s in st.session_state['secuestros']:
            cuerpo += f"{s}. "
            
    if st.session_state.get('pertenencias'):
        cuerpo += f"En carácter de DEPÓSITO se retienen: {st.session_state['pertenencias']}. "
        
    # Salud
    salud = st.session_state.get('salud', {})
    cuerpo += f"En cuanto a la integridad física, el encartado {salud.get('estado', 'no presenta lesiones')}. "
    if salud.get('asistencia'):
        cuerpo += f"Siendo asistido por Dr/a {salud.get('medico')}. "
    if salud.get('policial'):
        cuerpo += f"Resultando lesionado el personal policial: {salud.get('policial')}. "
        
    cuerpo += "No siendo para más, se da por finalizada la presente acta, previa lectura y ratificación de los intervinientes."

    st.subheader("1. Acta de Procedimiento")
    st.code(cuerpo, language=None)
    
    st.subheader("2. Inspección Ocular")
    inspec_txt = f"ACTA DE INSPECCIÓN OCULAR: En el lugar del hecho, se observa: {st.session_state.get('inspeccion')}. Iluminación: {salud.get('ilum', 'Artificial')}. Se realiza fijación fotográfica conforme protocolo."
    st.code(inspec_txt, language=None)
    
    st.warning("⚠️ Estos datos ya están 'masticados'. Al abrir el Módulo de Formulario 1, el vehículo y el CUIJ aparecerán automáticamente.")
