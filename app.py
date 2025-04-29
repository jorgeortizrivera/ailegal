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

    # Dividir contrato en cláusulas detectando encabezados PRIMERO., SEGUNDO., etc.
    patron = r'\b(PRIMERO|SEGUNDO|TERCERO|CUARTO|QUINTO|SEXTO|SÉPTIMO|OCTAVO|NOVENO|DÉCIMO|UNDÉCIMO|DUODÉCIMO|DECIMOTERCERO|DECIMOCUARTO|DECIMOQUINTO|DECIMOSEXTO)\b\.'
    partes = re.split(patron, contrato)

    clausulas = []
    i = 1
    while i < len(partes):
        titulo = partes[i].strip() + "."
        contenido = partes[i+1].strip()
        clausulas.append(f"{titulo} {contenido}")
        i += 2

    st.header("🧩 Selecciona las cláusulas que quieres mantener:")

    clausulas_mostradas = [f"{i+1}. {clausula[:80]}..." for i, clausula in enumerate(clausulas)]

    seleccionadas = st.multiselect(
        "Selecciona las cláusulas que quieras mantener en tu contrato:",
        options=list(range(1, len(clausulas)+1)),
        format_func=lambda x: clausulas_mostradas[x-1],
        default=list(range(1, len(clausulas)+1))
    )

    st.divider()

    if seleccionadas:
        # Generar el contrato final basado en las cláusulas seleccionadas
        contrato_final = "\n\n".join([clausulas[idx-1] for idx in seleccionadas])

        st.header("📄 Contrato Final:")
        st.text_area("Aquí tienes tu contrato final:", contrato_final, height=500)

        # Botón de descarga
        st.download_button(
            label="📥 Descargar contrato como .txt",
            data=contrato_final,
            file_name="Contrato_Generado.txt",
            mime="text/plain"
        )
