# app.py

import streamlit as st
from streamlit_sortables import sortables
import re

# Configuración de página
st.set_page_config(page_title="Generador de Contratos Inteligentes", layout="wide")
st.title("📜 Generador de Contratos Jurídicos Inteligentes")

# Subir archivo .txt de contrato
uploaded_file = st.file_uploader("Sube tu contrato modelo (.txt)", type="txt")

if uploaded_file is not None:
    # Leer contenido del archivo
    contrato = uploaded_file.read().decode('utf-8')

    # Dividir el contrato en cláusulas detectando encabezados como PRIMERO., SEGUNDO., etc.
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

    st.header("🧩 Reordena las cláusulas arrastrándolas:")

    # Drag & Drop real
    new_order = sortables(
        items=clausulas,
        direction="vertical",
        label="Cláusulas",
        key="sortable_clausulas"
    )

    st.divider()

    if new_order:
        # Armar el contrato final reordenado
        contrato_final = "\n\n".join(new_order)

        st.header("📄 Contrato Final Reordenado:")

        st.text_area("Aquí tienes el contrato final:", contrato_final, height=500)

        # Botón de descarga en TXT
        st.download_button(
            label="📥 Descargar contrato como .txt",
            data=contrato_final,
            file_name="Contrato_Generado.txt",
            mime="text/plain"
        )
