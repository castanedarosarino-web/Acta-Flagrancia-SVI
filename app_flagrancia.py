import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="SVI - Acta de Procedimiento", layout="wide")

# Estilo para que se vea profesional en el celular
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stTabs [aria-selected="true"] { background-color: #002d52 !important; color: white !important; font-weight: bold; }
    .stExpander { border: 1px solid #002d52; border-radius: 10px; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema SVI: Acta de Procedimiento")
st.caption("Autoría: SubComisario Castañeda Juan | Jurisdicción UR II")

# Inicializamos el relato en la memoria del programa
if 'relato_final' not in st.session_state:
    st.session_state.relato_final = ""

tabs = st.tabs(["📝 1. Inicio y Relato", "👥 2. Detenidos", "🔍 3. Secuestros/Salud", "📄 4. Acta Final"])

# --- TAB 1: INICIO Y RELATO ---
with tabs[0]:
    st.subheader("📍 Inicio del Procedimiento")
    c1, c2 = st.columns(2)
    with c1:
        nro_acta = st.text_input("CUIJ / Nro Acta", placeholder="Ej: 221/26")
        dependencia = st.selectbox("Dependencia", ["Comisaría 22°", "Subcomisaría 18°", "Comando Pérez", "PAT"])
    with c2:
        lugar = st.text_input("Lugar del Hecho (Calle y Altura)")
        preventor = st.text_input("Preventor Actuante", value="SubComisario Castañeda Juan")

    relato_raw = st.text_area("Narrativa del hecho (Dictado rápido):", height=150)
    if st.button("✨ PROFESIONALIZAR TEXTO"):
        # Limpieza técnica del lenguaje
        t = relato_raw.lower().replace("vago", "masculino").replace("fierro", "arma de fuego").replace("chata", "unidad móvil")
        st.session_state.relato_final = t.capitalize()
        st.success("Relato técnico generado con éxito.")

# --- TAB 2: DETENIDOS Y CONSULTA 911 ---
with tabs[1]:
    st.subheader("👤 Identificación de Aprehendidos")
    cant_det = st.number_input("¿Cuántos detenidos?", min_value=1, max_value=10, value=1)
    
    lista_detenidos = []
    
    for i in range(cant_det):
        with st.expander(f"DATOS DEL DETENIDO N° {i+1}", expanded=True):
            # 1. Cámara / Foto (Uso de st.camera_input para mayor compatibilidad)
            foto_det = st.camera_input(f"Foto Detenido {i+1}", key=f"cam_{i}")
            
            # 2. Datos según su planilla de Excel
            col1, col2, col3 = st.columns(3)
            dni_i = col1.text_input("DNI", key=f"dni_{i}")
            ape_i = col2.text_input("Apellido", key=f"ape_{i}")
            nom_i = col3.text_input("Nombre", key=f"nom_{i}")
            
            col4, col5, col6 = st.columns(3)
            apo_i = col4.text_input("Apodo", key=f"apo_{i}")
            papa_i = col5.text_input("Hijo de (Padre)", key=f"pa_{i}")
            mama_i = col6.text_input("Hijo de (Madre)", key=f"ma_{i}")
            
            col7, col8, col9 = st.columns(3)
            edad_i = col7.text_input("Edad", key=f"ed_{i}")
            prof_i = col8.text_input("Profesión", key=f"prof_{i}")
            dom_i = col9.text_input("Domicilio", key=f"dom_{i}")

            # 3. Consulta al 911 (Cóndor) integrada
            st.markdown("---")
            st.markdown("**📞 Consulta Sistema Cóndor / 911**")
            c_911_a, c_911_b = st.columns([1, 2])
            op_i = c_911_a.text_input("Operador Nro", key=f"op_{i}", placeholder="Ej: 45")
            res_i = c_911_b.selectbox("Resultado Consulta", 
                                     ["SIN REQUERIMIENTO", "CON PEDIDO DE CAPTURA ACTIVO", "PEDIDO DE PARADERO"], 
                                     key=f"res_{i}")
            
            # Solo agregamos a la lista si hay un DNI o Apellido para evitar el NameError
            if dni_i or ape_i:
                lista_detenidos.append({
                    "dni": dni_i, "full": f"{ape_i} {nom_i}", "papa": papa_i, "mama": mama_i,
                    "edad": edad_i, "prof": prof_i, "dom": dom_i, "op": op_i, "res": res_i
                })

# --- TAB 3: SECUESTROS Y SALUD ---
with tabs[2]:
    st.subheader("🚗 Vehículos e Inspección Ocular")
    con_vehiculo = st.checkbox("¿Hubo vehículo involucrado?")
    vehiculo_data = {}
    
    if con_vehiculo:
        v1, v2 = st.columns(2)
        dominio = v1.text_input("Dominio (Patente)")
        modelo = v2.text_input("Marca y Modelo")
        
        v3, v4 = st.columns(2)
        op_v = v3.text_input("Operador 911 (Vehicular)")
        res_v = v4.selectbox("Estado Rodado", ["SIN NOVEDAD", "CON PEDIDO DE SECUESTRO"])
        vehiculo_data = {"dom": dominio, "mod": modelo, "op": op_v, "res": res_v}

    st.divider()
    st.subheader("🩹 Integridad Física (Lesiones)")
    lesiones_det = st.text_area("Lesiones en Detenidos (Descripción y fotos):")
    lesiones_pol = st.text_area("Lesiones en Personal Policial (si las hubiera):")

# --- TAB 4: ACTA FINAL ---
with tabs[3]:
    st.subheader("📄 Acta de Procedimiento Consolidada")
    ahora = datetime.now()
    
    # Construcción narrativa de las consultas 911
    txt_911 = ""
    for d in lista_detenidos:
        txt_911 += f"Que consultado el sistema 911 a través del operador {d['op']}, el mismo informa que sobre el llamado {d['full'].upper()}, DNI {d['dni']}, pesa un resultado de {d['res']}. "
    
    txt_v = ""
    if con_vehiculo and vehiculo_data.get('dom'):
        txt_v = f"Asimismo, se consulta sobre el rodado {vehiculo_data['mod']} dominio {vehiculo_data['dom']}, informando el operador {vehiculo_data['op']} que el mismo se encuentra {vehiculo_data['res']}. "

    # Acta final integrada
    acta_final = f"""En la ciudad de Pérez, a los {ahora.day} días del mes de Abril de {ahora.year}, siendo las {ahora.strftime('%H:%M')} horas, el suscripto {preventor.upper()}, personal de la {dependencia}, hace constar: Que en circunstancias de {st.session_state.relato_final}, en {lugar}. 

{txt_911}
{txt_v}

CONSTATACIÓN DE LESIONES: Se deja constancia que {lesiones_det if lesiones_det else 'no se observan lesiones a simple vista en los causantes'}. Por parte del personal, {lesiones_pol if lesiones_pol else 'no se registran novedades físicas'}.

Se procede al traslado de los mismos a sede policial para los trámites de rigor."""

    st.code(acta_final, language=None)
    st.button("📋 COPIAR ACTA")
