# app.py

import streamlit as st

# Título de la app
st.title("Generador de Contratos Jurídicos 📜")

# Subir archivo .txt de contrato
uploaded_file = st.file_uploader("Sube tu contrato modelo (.txt)", type="txt")

if uploaded_file is not None:
    # Leer el contenido del archivo
    contrato = uploaded_file.read().decode('utf-8')

    # Dividir en cláusulas por encabezados (PRIMERO., SEGUNDO., etc.)
    import re
    patron = r'\b(PRIMERO|SEGUNDO|TERCERO|CUARTO|QUINTO|SEXTO|SÉPTIMO|OCTAVO|NOVENO|DÉCIMO|UNDÉCIMO|DUODÉCIMO|DECIMOTERCERO|DECIMOCUARTO|DECIMOQUINTO|DECIMOSEXTO)\b\.'
    partes = re.split(patron, contrato)

    clausulas = []
    i = 1
    while i < len(partes):
        titulo = partes[i].strip() + "."
        contenido = partes[i+1].strip()
        clausulas.append(f"{titulo} {contenido}")
        i += 2

    st.header("Cláusulas detectadas:")
    # Mostrar cláusulas y permitir reordenarlas
    orden = st.multiselect(
        'Reordena las cláusulas seleccionando el nuevo orden',
        options=list(range(1, len(clausulas)+1)),
        default=list(range(1, len(clausulas)+1))
    )

    if orden:
        contrato_final = ""
        for idx in orden:
            contrato_final += clausulas[idx-1] + "\n\n"

        st.header("Contrato Final:")
        st.text_area("Aquí tienes el contrato final:", contrato_final, height=500)

        # Descargar como TXT
        st.download_button(
            label="Descargar contrato como .txt",
            data=contrato_final,
            file_name='Contrato_Generado.txt',
            mime='text/plain'
        )
