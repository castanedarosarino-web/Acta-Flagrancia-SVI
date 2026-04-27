# =========================================================
# BLOQUE 2: IDENTIFICACIÓN, REQUISA Y MESA DE ENLACE
# =========================================================
with st.expander("👤 BLOQUE 2: DATOS DEL DEMORADO Y VALIDACIÓN LEGAL", expanded=True):
    st.subheader("A. Identificación del Sujeto")
    col_suj1, col_suj2 = st.columns(2)
    with col_suj1:
        nombre_sujeto = st.text_input("Nombre y Apellido Completos")
        dni_sujeto = st.text_input("DNI / Prontuario / Pasaporte")
    with col_suj2:
        domicilio_sujeto = st.text_input("Domicilio Declarado")
        edad_sujeto = st.number_input("Edad", min_value=0, max_value=120, step=1)

    st.markdown("---")
    st.subheader("B. Requisa Personal (Art. 225 CPP)")
    st.info("Describa detalladamente los elementos hallados entre las prendas o en poder del demorado.")
    
    col_req1, col_req2 = st.columns(2)
    with col_req1:
        testigo_1 = st.text_input("Testigo Presencial 1 (Nombre y DNI)")
    with col_req2:
        testigo_2 = st.text_input("Testigo Presencial 2 (Nombre y DNI)")
        
    requisa_ia = st.text_area("Cuerpo del Acta de Requisa", 
                             placeholder="Ante la presencia de testigos hables, se procede a la requisa, hallando...",
                             height=150)
    
    st.markdown("---")
    st.subheader("C. Central de Emergencias y Mesa de Enlace")
    st.error("⚠️ PROHIBIDO CONTINUAR SIN VALIDACIÓN DE ANTECEDENTES")
    
    col_val1, col_val2, col_val3 = st.columns(3)
    with col_val1:
        consulta_911 = st.text_input("Operador 911 (N° de Incidencia)")
    with col_val2:
        central_condor = st.text_input("Operador Cóndor (Antecedentes)")
    with col_val3:
        mesa_enlace = st.text_input("Mesa de Enlace (Validación Final)")

    # Lógica de validación visual
    if mesa_enlace:
        st.success(f"Situación legal validada por Mesa de Enlace. Proceda a comunicar al MPA.")
