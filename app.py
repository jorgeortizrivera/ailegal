# app.py

import streamlit as st
import re
import openai
from openai import OpenAI
from streamlit_chat import message
import time  # <-- Agregado aquí

# Configuración de la página
st.set_page_config(page_title="Generador de Contratos Inteligentes", layout="wide")
st.title("📜 Generador de Contratos Jurídicos Inteligentes")

# Configurar cliente de OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Subir archivo .txt de contrato
uploaded_file = st.file_uploader("Sube tu contrato modelo (.txt)", type="txt")

contrato_final = ""
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
        contrato_final = "\n\n".join([clausulas[idx-1] for idx in seleccionadas])

        st.header("📄 Contrato Final:")
        st.text_area("Aquí tienes tu contrato final:", contrato_final, height=500)

        st.download_button(
            label="📥 Descargar contrato como .txt",
            data=contrato_final,
            file_name="Contrato_Generado.txt",
            mime="text/plain"
        )

# ----------------- CHATBOT EN BARRA LATERAL -----------------

st.sidebar.title("💬 Asistente Jurídico IA")

# Inicializar historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")

# Entrada de usuario
prompt = st.sidebar.text_input("Escribe tu pregunta o solicitud:")

if prompt:
    # Guardar pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Esperar 1.5 segundos para evitar Rate Limit de OpenAI
    time.sleep(1.5)

    # Construir contexto
    context = contrato_final if contrato_final else "Asiste en temas de contratos jurídicos."

    # Nueva forma de crear la solicitud al modelo OpenAI
    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Actúa como asesor jurídico experto. El contrato actual es: {context}"},
            *st.session_state.messages
        ]
    )

    respuesta_texto = respuesta.choices[0].message.content

    # Guardar respuesta
    st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})

    # Mostrar respuesta
    message(respuesta_texto, is_user=False)
