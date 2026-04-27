# =========================================================
# MODULO DE FOTOS CON DESCRIPCIÓN IA (PROTOCOLO 4 FOTOS)
# =========================================================
st.header("📸 Registro Fotográfico y Diagnóstico IA")
st.info("Cargue las vistas obligatorias. La IA procesará la descripción técnica para el acta.")

col_f1, col_f2 = st.columns(2)

with col_f1:
    foto_1 = st.file_uploader("1. VISTA PANORÁMICA (Lugar)", type=['jpg', 'png', 'jpeg'])
    if foto_1:
        st.image(foto_1, width=250)
        # Aquí la IA generaría el texto. Simulamos la salida técnica:
        desc_ia_1 = st.text_area("Descripción IA (Panorámica)", 
                                 "Se observa escenario en zona urbana, calzada de asfalto con iluminación artificial activa y visibilidad sin obstrucciones.")

    foto_3 = st.file_uploader("3. PRIMER PLANO (Objeto/Rostro)", type=['jpg', 'png', 'jpeg'])
    if foto_3:
        st.image(foto_3, width=250)
        desc_ia_3 = st.text_area("Descripción IA (Primer Plano)", 
                                 "Enfoque directo sobre elemento secuestrado, permitiendo observar integridad del mismo y características de fabricación.")

with col_f2:
    foto_2 = st.file_uploader("2. PLANO MEDIO (Vínculo)", type=['jpg', 'png', 'jpeg'])
    if foto_2:
        st.image(foto_2, width=250)
        desc_ia_2 = st.text_area("Descripción IA (Plano Medio)", 
                                 "Se establece vínculo espacial entre el sujeto demorado y el elemento del ilícito en el punto de aprehensión.")

    foto_4 = st.file_uploader("4. PRIMERÍSIMO PRIMER PLANO (Detalle)", type=['jpg', 'png', 'jpeg'])
    if foto_4:
        st.image(foto_4, width=250)
        desc_ia_4 = st.text_area("Descripción IA (Detalle/Guarismos)", 
                                 "Toma de detalle sobre numeración de serie/cuadro, observándose guarismos originales sin signos de adulteración a simple vista.")
