import streamlit as st
from PyPDF2 import PdfReader
from collections import Counter
import math
import pandas as pd

# ==============================
# Configuración de la página
# ==============================

st.set_page_config(
    page_title="Teoría de la Información",
    page_icon="icono.png",
    layout="centered"
)

# ==============================
# ESTILO NEÓN FUTURISTA
# ==============================

st.markdown("""
<style>

/* Fondo general */
body {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: #e5e7eb;
}

/* Títulos */
h1 {
    color: #00ffff;
    text-align: center;
    text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
}

h2, h3 {
    color: #7c3aed;
    text-shadow: 0 0 8px #7c3aed;
    text-align: center;
}

/* Etiquetas */
label {
    color: #22d3ee !important;
}

/* Quitar estilo de caja del título del radio */
.stRadio label:first-child {
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin-bottom: 12px;
    font-size: 1.2rem;
    font-weight: 600;
    color: #22d3ee;
    cursor: default;
}

/* Evitar que parezca clickeable */
.stRadio label:first-child:hover {
    background: none !important;
}


/* TextArea */
.stTextArea textarea {
    background-color: #020617;
    color: #00ffff;
    border: 2px solid #00ffff;
    border-radius: 10px;
    font-family: monospace;
    box-shadow: 0 0 15px rgba(0,255,255,0.5);
}

/* File uploader */
.stFileUploader {
    background-color: #020617;
    border: 2px dashed #7c3aed;
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0 0 15px rgba(124,58,237,0.5);
}

/* Tablas */
table {
    background-color: #020617;
    border-collapse: collapse;
    box-shadow: 0 0 20px rgba(0,255,255,0.3);
}

thead tr th {
    background-color: #020617;
    color: #00ffff;
    border-bottom: 2px solid #00ffff;
    text-shadow: 0 0 6px #00ffff;
}

tbody tr td {
    color: #e5e7eb;
    border-bottom: 1px solid #1f2937;
}

tbody tr:hover {
    background-color: rgba(124,58,237,0.2);
}

/* Mensajes de éxito */
.stSuccess {
    background-color: #020617;
    color: #22d3ee;
    border-left: 6px solid #22d3ee;
    box-shadow: 0 0 15px rgba(34,211,238,0.6);
}

/* Texto normal */
p {
    color: #e5e7eb;
}

/* Scroll */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(#00ffff, #7c3aed);
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.title("Calculadora – Teoría de la Información")

# ==============================
# Funciones matemáticas
# ==============================

def info_hartley(p):
    return -math.log10(p)

def entropia_shannon(p):
    return -p * math.log2(p)

# ==============================
# Opción de entrada
# ==============================

opcion = st.radio(
    "Seleccione el método de entrada",
    ["Subir archivo", "Escribir texto"]
)

texto = ""

# ==============================
# Subida de archivo
# ==============================

if opcion == "Subir archivo":
    archivo = st.file_uploader(
        "Suba su archivo (.txt o .pdf)",
        type=["txt", "pdf"]
    )

    if archivo:
        if archivo.type == "application/pdf":
            reader = PdfReader(archivo)
            for page in reader.pages:
                texto += page.extract_text()
        else:
            texto = archivo.read().decode("utf-8")

# ==============================
# Texto escrito manualmente
# ==============================

elif opcion == "Escribir texto":
    texto = st.text_area("Escriba el texto aquí")

# ==============================
# Procesamiento del texto
# ==============================

if texto:
    texto = texto.upper()
    texto = "".join(c for c in texto if c.isalpha())

    st.subheader("Texto procesado")
    st.text(texto)

    # ==============================
    # Conteo de símbolos
    # ==============================

    frecuencias = Counter(texto)
    N = sum(frecuencias.values())
    M = len(frecuencias)

    st.subheader("Tabla de frecuencias")

    datos = []
    for letra, f in sorted(frecuencias.items()):
        p = f / N
        datos.append((letra, f, p))

    st.table(pd.DataFrame(
        datos,
        columns=["Letra", "Frecuencia", "Probabilidad"]
    ))

    st.write(f"Total de símbolos (N): {N}")
    st.write(f"Símbolos distintos (M): {M}")

    # ==============================
    # Información I (Hartleys)
    # ==============================

    st.subheader("Información por símbolo (Hartleys)")

    info_total = 0
    info_tabla = []

    for letra, f, p in datos:
        I = info_hartley(p)
        info_total += I
        info_tabla.append((letra, p, I))

    st.table(pd.DataFrame(
        info_tabla,
        columns=["Letra", "Probabilidad", "I = -log10(p)"]
    ))

    st.success(f"Información total I_total = {round(info_total,4)} Hartleys")

    # ==============================
    # Entropía H
    # ==============================

    st.subheader("Entropía de Shannon")

    H = 0
    entropia_tabla = []

    for letra, f, p in datos:
        h_i = entropia_shannon(p)
        H += h_i
        entropia_tabla.append((letra, p, h_i))

    st.table(pd.DataFrame(
        entropia_tabla,
        columns=["Letra", "Probabilidad", "-p·log2(p)"]
    ))

    st.success(f"Entropía H = {round(H,2)} bits/símbolo")

    # ==============================
    # r y T
    # ==============================

    r = 0.7
    T = H / r

    # ==============================
    # Resumen final
    # ==============================

    st.subheader("Resumen final")

    resumen = pd.DataFrame({
        "Magnitud": [
            "Información total (I_total)",
            "Entropía (H)",
            "Duración del pulso (r)",
            "Tasa de información (T)"
        ],
        "Valor": [
            f"{round(info_total,4)} Hartleys",
            f"{round(H,2)} bits/símbolo",
            f"{r} ms",
            f"{round(T,2)} bits/ms"
        ]
    })

    st.table(resumen)
