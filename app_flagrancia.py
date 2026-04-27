# =========================================================
# BLOQUE 1: NARRATIVA TÁCTICA (CORAZÓN DEL SISTEMA)
# =========================================================
with st.expander("📝 BLOQUE 1: DATOS Y NARRATIVA POR AUDIO", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        fecha_proc = st.date_input("Fecha del Hecho", datetime.now())
        unidad_interviniente = st.text_input("Dependencia", "COMANDO RADIOELÉCTRICO PÉREZ")
    with col2:
        hora_proc = st.time_input("Hora de Intervención", datetime.now())
        oficial_actuante = st.text_input("Oficial Actuante", "Sub Comisario Castañeda Juan")
    
    st.markdown("---")
    st.subheader("🎙️ Dictado de Acta (Narrativa)")
    st.info("Presione el micrófono y relate el procedimiento. La IA transformará su voz en texto jurídico.")
    
    # Componente de entrada de audio
    audio_file = st.audio_input("Grabar relato de flagrancia")
    
    if audio_file:
        st.success("Audio recibido. Procesando transcripción técnica...")
        # Aquí se vincula con el motor de transcripción (Whisper/SpeechToText)
        # Por ahora, dejamos el espacio para que el texto aparezca abajo
        narrativa_voz = st.text_area(
            "Texto Transcripto (Editable)", 
            value="[Aquí aparecerá el relato del oficial convertido a texto automáticamente]",
            height=200
        )
    else:
        narrativa_manual = st.text_area(
            "Narrativa Manual (si no usa audio)", 
            placeholder="En circunstancias que el móvil se encontraba patrullando...",
            height=200
        )

    st.caption("Autoría reservada: Sub Comisario Castañeda Juan")
