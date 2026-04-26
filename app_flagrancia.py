# Agregar este bloque al final del código anterior
st.write("---")
st.subheader("📥 Gestión de Salida (Copiar y Pegar)")

# Generamos el texto completo para el portapapeles
texto_completo = f"""
*ACTA DE PROCEDIMIENTO DE FLAGRANCIA*
--------------------------------------
*AUTOR:* {oficial_actuante}
*FECHA/HORA:* {fecha_procedimiento} {hora_cierre}
*LUGAR:* {lugar}

*RESEÑA:*
{relato_hecho}

*APREHENDIDO:*
{nombre_detenido} - DNI: {dni if 'dni' in locals() else 'S/D'}

*SECUESTROS:*
{v_datos}
Obs: {v_obs}
Otros: {secuestro_otros}

*CIERRE:*
{cierre_rosario}
"""

# Botón de Copiado Rápido
if st.button("📋 COPIAR ACTA PARA WHATSAPP"):
    st.write("Texto listo para copiar (Seleccione y pegue en WhatsApp):")
    st.code(texto_completo)
    st.success("Texto generado. Mantenga presionado sobre el cuadro gris, elija 'Seleccionar todo' y 'Copiar'.")

# Botón de Descarga Local
st.download_button(
    label="💾 DESCARGAR ACTA EN CELULAR/PC",
    data=texto_completo,
    file_name=f"Acta_{nombre_detenido.replace(' ', '_')}.txt",
    mime="text/plain"
)
