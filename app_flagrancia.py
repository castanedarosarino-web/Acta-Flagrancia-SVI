import json

# ... (dentro de st.sidebar) ...

with st.sidebar:
    st.title("📂 Central de Recepción")
    st.markdown("### **Creado por Sub Comisario CASTAÑEDA Juan**")
    
    st.divider()
    st.subheader("📥 Cargar Trabajo de Calle")
    archivo_subido = st.file_uploader("Subir archivo JSON", type=["json"], help="200MB per file • JSON")
    
    if archivo_subido is not None:
        try:
            datos_importados = json.load(archivo_subido)
            st.session_state.data_operativa.update(datos_importados)
            st.success("✅ Datos cargados correctamente.")
        except Exception as e:
            st.error(f"Error al cargar: {e}")

    st.divider()
    
    # PREPARACIÓN DEL ARCHIVO PARA DESCARGA
    # Generamos el contenido del JSON basado en lo que hay en pantalla
    data_a_guardar = json.dumps(st.session_state.data_operativa, indent=4)
    nombre_archivo = f"acta_{st.session_state.data_operativa.get('nro_acta', 'sin_numero')}.json"

    # EL BOTÓN CORRECTO: st.download_button
    # Este componente es el único que activa la descarga real en el navegador
    st.download_button(
        label="💾 GUARDAR ACTA (JSON)",
        data=data_a_guardar,
        file_name=nombre_archivo,
        mime="application/json",
        use_container_width=True
    )
