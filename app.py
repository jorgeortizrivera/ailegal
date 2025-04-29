# app.py

import streamlit as st
import re

st.set_page_config(page_title="Generador de Contratos Inteligentes", layout="wide")
st.title("📜 Generador de Contratos Jurídicos Inteligentes")

# Subir archivo .txt de contrato
uploaded_file = st.file_uploader("Sube tu contrato modelo (.txt)", type="txt")

if uploaded_file is not None:
    # Leer contenido del archivo
    contrato = uploaded_file.read().decode('utf-8')

    # Dividir contrato en cláusulas
    patron = r'\b(PRIMERO|SEGUNDO|TERCERO|CUARTO|QUINTO|SEXTO|SÉPTIMO|OCTAVO|NOVENO|DÉCIMO|UNDÉCIMO|DUODÉCIMO|DECIMOTERCERO|DECIMOCUARTO|DECIMOQUINTO|DECIMOSEXTO)\b\.'
    partes = re.split(patron, contrato)

    clausulas = []
    i = 1
    while i < len(partes):
        titulo = partes[i].strip() + "."
        contenido = partes[i+1].strip()
        clausulas.append(f"{titulo} {contenido}")
        i += 2

    st.header("🧩 Ordena las cláusulas seleccionando manualmente:")

    clausulas_mostradas = [f"{i+1}. {clausula[:80]}..." for i, clausula in enumerate(clausulas)]

    st.write("Selecciona las cláusulas en el orden que quieras que aparezcan:")

    nueva_orden = []
    for idx in range(len(clausulas)):
        opcion = st.selectbox(
            f"Posición {idx+1}:",
            options=[""] + clausulas_mostradas,
            key=f"select_{idx}"
        )
        nueva_orden.append(opcion)

    nueva_orden = [c for c in nueva_orden if c != ""]

    st.divider()

    if nueva_orden:
        # Reconstruir el contrato final
        clausulas_seleccionadas = []
        for seleccionada in nueva_orden:
            numero = int(seleccionada.split(".")[0]) - 1
            clausulas_seleccionadas.append(clausulas[numero])

        contrato_final = "\n\n".join(clausulas_seleccionadas)

        st.header("📄 Contrato Final Reordenado:")
        st.text_area("Aquí tienes el contrato final:", contrato_final, height=500)

        # Botón para descargar
        st.download_button(
            label="📥 Descargar contrato como .txt",
            data=contrato_final,
            file_name="Contrato_Generado.txt",
            mime="text/plain"
        )

