# app.py

import streamlit as st
import re

# Configuración de la página
st.set_page_config(page_title="Generador de Contratos Inteligentes", layout="wide")
st.title("📜 Generador de Contratos Jurídicos Inteligentes")

# Subir archivo .txt de contrato
uploaded_file = st.file_uploader("Sube tu contrato modelo (.txt)", type="txt")

if uploaded_file is not None:
    # Leer contenido del archivo
    contrato = uploaded_file.read().decode('utf-8')

    # Dividir contrato en cláusulas detectando encabezados tipo PRIMERO., SEGUNDO., etc.
    patron = r'\b(PRIMERO|SEGUNDO|TERCERO|CUARTO|QUINTO|SEXTO|SÉPTIMO|OCTAVO|NOVENO|DÉCIMO|UNDÉCIMO|DUODÉCIMO|DECIMOTERCERO|DECIMOCUARTO|DECIMOQUINTO|DECIMOSEXTO)\b\.'
    partes = re.split(patron, contrato)

    # Agrupar títulos y contenidos
    clausulas = []
    i = 1
    while i < len(partes):
        titulo = partes[i].strip() + "."
        contenido = partes[i+1].strip()
        clausulas.append(f"{titulo} {contenido}")
        i += 2

    st.header("🧩 Ordena las cláusulas seleccionando el nuevo orden:")

    # Mostrar lista numerada
    clausulas_mostradas = [f"Cláusula {i+1}: {clausula[:80]}..." for i, clausula in enumerate(clausulas)]

    # Permitir selección múltiple en el orden que elija el usuario
    orden = st.multiselect(
        "Selecciona las cláusulas en el orden que quieras que aparezcan:",
        options=list(range(1, len(clausulas)+1)),
        format_func=lambda x: clausulas_mostradas[x-1],
        default=list(range(1, len(clausulas)+1))
    )

    st.divider()

    if orden:
        contrato_final = "\n\n".join([clausulas[idx-1] for idx in orden])

        st.header("📄 Contrato Final Reordenado:")
        st.text_area("Aquí tienes el contrato final:", contrato_final, height=500)

        # Botón de descarga
        st.download_button(
            label="📥 Descargar contrato como .txt",
            data=contrato_final,
            file_name="Contrato_Generado.txt",
            mime="text/plain"
        )
