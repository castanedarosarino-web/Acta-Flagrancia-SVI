import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN TÁCTICA ---
st.set_page_config(page_title="SVI - Acta de Procedimiento", layout="wide")

# Estilo profesional UR II
st.markdown("""
    <style>
    .stTabs [aria-selected="true"] { background-color: #002d52 !important; color: white !important; }
    .stExpander { border: 1px solid #002d52; border-radius: 10px; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema SVI: Acta de Procedimiento")
st.caption("Autoría: SubComisario Castañeda Juan | Jurisdicción UR II")

# --- MEMORIA OPERATIVA ---
if 'relato_final' not in st.session_state: st.session_state.relato_final = ""

tab1, tab2, tab3, tab4 = st.tabs(["📝 RELATO", "👥 DETENIDOS/911", "🚗 VEHÍCULOS/SECUESTROS", "📄 ACTA FINAL"])

# --- TAB 1: RELATO ---
with tab1:
    st.subheader("📍 Inicio del Procedimiento")
    c1, c2 = st.columns(2)
    with c1:
        cuij = st.text_input("CUIJ / Nro Acta", value="21-")
        dependencia = st.selectbox("Unidad Operativa", ["Comisaría 22°", "Subcomisaría 18°", "Comando Pérez", "PAT"])
    with c2:
        lugar = st.text_input("Lugar del Hecho (Calle, Altura, Localidad)")
        preventor = st.text_input("Oficial Actuante", value="SubComisario Castañeda Juan")

    relato_raw = st.text_area("Narrativa del hecho (Dictado):", height=150)
    if st.button("✨ PROFESIONALIZAR RELATO"):
        t = relato_raw.lower().replace("vago", "masculino").replace("fierro", "arma de fuego").replace("chata", "unidad móvil")
        st.session_state.relato_final = t.capitalize()
        st.success("Relato técnico generado.")

# --- TAB 2: DETENIDOS Y CONSULTA CÓNDOR ---
with tab2:
    st.subheader("👤 Identificación y Consultas 911")
    cant_det = st.number_input("Cantidad de sujetos", min_value=1, max_value=10, value=1)
    
    lista_detenidos = []
    
    for i in range(cant_det):
        with st.expander(f"FILIACIÓN COMPLETA - SUJETO N° {i+1}", expanded=True):
            # Foto Robusta (Opción B)
            foto = st.file_uploader(f"Capturar Fotografía (Sujeto {i+1})", type=['jpg','png'], key=f"foto_{i}")
            if foto: st.image(foto, width=150)
            
            # Datos de Filiación (Según imagen enviada)
            f1, f2, f3, f4 = st.columns([2, 3, 3, 2])
            dni_i = f1.text_input("DNI", key=f"dni_{i}")
            ape_i = f2.text_input("Apellido", key=f"ape_{i}")
            nom_i = f3.text_input("Nombre", key=f"nom_{i}")
            apo_i = f4.text_input("Apodo", key=f"apo_{i}")
            
            f_padres = st.columns(2)
            papa_i = f_padres[0].text_input("Hijo de (Padre)", key=f"pa_{i}")
            mama_i = f_padres[1].text_input("Hijo de (Madre)", key=f"ma_{i}")
            
            f_clase = st.columns(3)
            edad_i = f_clase[0].text_input("Edad", key=f"ed_{i}")
            prof_i = f_clase[1].text_input("Profesión", key=f"prof_{i}")
            dom_i = f_clase[2].text_input("Domicilio", key=f"dom_{i}")

            st.markdown("**🔍 Consulta Sistema Cóndor / 911**")
            c_911 = st.columns([2, 3])
            op_i = c_911[0].text_input("Operador 911", key=f"op_{i}", placeholder="Nro de Operador")
            res_i = c_911[1].selectbox("Resultado", ["SIN REQUERIMIENTO", "CON PEDIDO DE CAPTURA", "PEDIDO DE PARADERO"], key=f"res_{i}")
            
            # Guardamos con nombres únicos para evitar el NameError
            lista_detenidos.append({
                "full": f"{ape_i} {nom_i}", "dni": dni_i, "padres": f"{papa_i} y {mama_i}",
                "datos": f"{edad_i} años, de profesión {prof_i}, domiciliado en {dom_i}",
                "op": op_i, "resultado": res_i
            })

# --- TAB 3: VEHÍCULOS E INSPECCIÓN ---
with tab3:
    st.subheader("🚗 Consulta Vehicular y Secuestros")
    usa_vehiculo = st.checkbox("¿Involucra Vehículo?")
    datos_v = {}
    
    if usa_vehiculo:
        v1, v2, v3 = st.columns(3)
        dominio = v1.text_input("Dominio")
        modelo = v2.text_input("Marca/Modelo")
        op_v = v3.text_input("Operador 911 (Vehicular)")
        res_v = st.selectbox("Resultado Consulta Rodado", ["SIN NOVEDAD", "CON PEDIDO DE SECUESTRO ACTIVO"])
        datos_v = {"dom": dominio, "mod": modelo, "op": op_v, "res": res_v}

    st.divider()
    st.subheader("🔍 Inspección Ocular y Lesiones")
    insp_ocular = st.text_area("Descripción del lugar/escena (Protocolar):")
    lesiones = st.text_area("Constatación de Lesiones (Detenidos/Personal):")

# --- TAB 4: ACTA FINAL ---
with tab4:
    st.subheader("📄 Acta de Procedimiento Consolidada")
    ahora = datetime.now()
    
    # Redacción dinámica de consultas 911
    narrativa_911 = ""
    for d in lista_detenidos:
        if d['dni']: # Solo si se cargó el DNI
            narrativa_911 += f"Que consultado el sistema de emergencias 911 a través del operador {d['op']}, el mismo informa que sobre el llamado {d['full'].upper()} pesa un resultado de {d['resultado']}. "
    
    narrativa_v = ""
    if usa_vehiculo and datos_v.get('dom'):
        narrativa_v = f"Asimismo, se realiza consulta sobre el rodado {datos_v['mod']} dominio {datos_v['dom']}, informando el operador {datos_v['op']} que el mismo se encuentra {datos_v['res']}. "

    # Construcción final
    acta = f"""En la ciudad de Pérez, a los {ahora.day} días del mes de Abril de {ahora.year}, siendo las {ahora.strftime('%H:%M')} horas...

CONSTAR: Que en circunstancias de {st.session_state.relato_final}, en {lugar}.

{narrativa_911}
{narrativa_v}

INSPECCIÓN Y LESIONES: {insp_ocular}. En cuanto a la integridad física, se hace constar que {lesiones}.

Se procede al traslado de los causantes y efectos a sede de la {dependencia} para continuar con las actuaciones de rigor."""

    st.code(acta, language=None)
    st.button("📋 COPIAR ACTA COMPLETA")
