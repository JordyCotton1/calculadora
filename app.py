import streamlit as st
from PyPDF2 import PdfReader
from collections import Counter
import math
import pandas as pd
from heapq import heappush, heappop

# ==============================
# CONFIGURACIÓN DE LA PÁGINA
# ==============================

st.set_page_config(
    page_title="Teoría de la Información y Huffman",
    page_icon="icono.png",
    layout="centered"
)

# ==============================
# ESTILO NEÓN FUTURISTA
# ==============================

st.markdown("""
<style>

/* ==============================
   Animación Glow en LETRAS
============================== */
@keyframes glowText {
    0% { text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff; }
    50% { text-shadow: 0 0 15px #ff00ff, 0 0 30px #ff00ff; }
    100% { text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff; }
}

body {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: #e5e7eb;
}

h1 {
    color: #00ffff;
    text-align: center;
    text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
    animation: glowText 2s infinite alternate;
}

h2, h3 {
    color: #7c3aed;
    text-shadow: 0 0 8px #7c3aed;
    text-align: center;
    animation: glowText 2s infinite alternate;
}

label {
    color: #22d3ee !important;
}

.stRadio label:first-child {
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin-bottom: 12px;
    font-size: 1.2rem;
    font-weight: 600;
    color: #22d3ee;
}

.stTextArea textarea {
    background-color: #020617;
    color: #00ffff;
    border: 2px solid #00ffff;
    border-radius: 10px;
    font-family: monospace;
}

.stFileUploader {
    background-color: #020617;
    border: 2px dashed #7c3aed;
    border-radius: 10px;
    padding: 10px;
}

/* ==============================
   TABLA COMPLETA CON ESTILO NEÓN
============================== */

table {
    width: 100% !important;
    border-collapse: collapse !important;
    background-color: #020617 !important;
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid #00ffff !important;
    box-shadow: 0 0 15px #00ffff;
}

thead tr th {
    color: #00ffff !important;
    font-size: 16px !important;
    text-align: center !important;
    background-color: #0f172a !important;
    border-bottom: 2px solid #ff00ff !important;
    padding: 12px !important;
    animation: glowText 2s infinite alternate;
}

tbody tr td {
    color: #e5e7eb !important;
    text-align: center !important;
    padding: 10px !important;
    border-bottom: 1px solid #334155 !important;
    font-size: 15px !important;
}

tbody tr:hover {
    background-color: rgba(124, 58, 237, 0.25) !important;
    transition: 0.3s;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# TÍTULO
# ==============================

st.title("📡 Teoría de la Información y Codificación de Huffman")

# ==============================
# SELECCIÓN DE CÁLCULO
# ==============================

calculo = st.radio(
    "Seleccione el cálculo a realizar",
    ["Teoría de la Información", "Codificación de Huffman"]
)

# ==============================
# FUNCIONES MATEMÁTICAS
# ==============================

def info_hartley(p):
    return -math.log10(p)

def entropia_shannon(p):
    return -p * math.log2(p)

# ======================================================
# TEORÍA DE LA INFORMACIÓN
# ======================================================

if calculo == "Teoría de la Información":

    opcion = st.radio(
        "Seleccione el método de entrada",
        ["Subir archivo", "Escribir texto"]
    )

    texto = ""

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

    elif opcion == "Escribir texto":
        texto = st.text_area("Escriba el texto aquí")

    if texto:
        texto = texto.upper()
        texto = "".join(c for c in texto if c.isalpha())

        st.subheader("Texto procesado")
        st.text(texto)

        frecuencias = Counter(texto)
        N = sum(frecuencias.values())
        M = len(frecuencias)
        
        

        st.subheader("Tabla de frecuencias")

        datos = []
        for letra, f in sorted(frecuencias.items(), key=lambda x: x[1], reverse=True):
            p = f / N
            datos.append((letra, f, p))

        st.table(pd.DataFrame(
            datos,
            columns=["Letra", "Frecuencia", "Probabilidad"]
        ))

        st.write(f"Total de símbolos (N): {N}")
        st.write(f"Símbolos distintos (M): {M}")

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

        r = 0.7
        T = H / r

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

# ======================================================
# CODIFICACIÓN DE HUFFMAN
# ======================================================

if calculo == "Codificación de Huffman":

    st.caption("Entrada tipo: A10, E7, I5, S5, O3, H2, Z2")

    opcion = st.radio(
        "Seleccione el método de entrada",
        ["Subir archivo", "Escribir frecuencias"]
    )

    entrada = ""

    if opcion == "Subir archivo":
        archivo = st.file_uploader("Suba un archivo .txt", type=["txt"])
        if archivo:
            entrada = archivo.read().decode("utf-8")

    elif opcion == "Escribir frecuencias":
        entrada = st.text_area(
            "Ingrese las frecuencias (ej: A10, E7, I5, S5, O3, H2, Z2)"
        )

    if entrada:
        try:
            frecuencias = {}
            partes = entrada.replace(" ", "").split(",")

            for p in partes:
                simbolo = p[0].upper()
                freq = int(p[1:])
                frecuencias[simbolo] = freq

            st.subheader("Lista inicial de frecuencias")
            st.table([{"Símbolo": s, "f": f} for s, f in frecuencias.items()])

            class Nodo:
                def __init__(self, simbolo, freq):
                    self.simbolo = simbolo
                    self.freq = freq
                    self.izq = None
                    self.der = None

                def __lt__(self, otro):
                    return self.freq < otro.freq

            heap = []
            for s, f in frecuencias.items():
                heappush(heap, Nodo(s, f))

            pasos = []

            while len(heap) > 1:
                n1 = heappop(heap)
                n2 = heappop(heap)

                nuevo = Nodo(n1.simbolo + n2.simbolo, n1.freq + n2.freq)
                nuevo.izq = n1
                nuevo.der = n2

                pasos.append((n1.simbolo, n1.freq, n2.simbolo, n2.freq, nuevo.freq))
                heappush(heap, nuevo)

            raiz = heap[0]

            st.subheader("Sumas sucesivas")
            st.table([
                {
                    "Símbolo 1": s1,
                    "f1": f1,
                    "Símbolo 2": s2,
                    "f2": f2,
                    "Suma": suma
                }
                for s1, f1, s2, f2, suma in pasos
            ])

            codigos = {}

            def recorrer(nodo, codigo=""):
                if nodo.izq is None and nodo.der is None:
                    codigos[nodo.simbolo] = codigo
                    return
                recorrer(nodo.izq, codigo + "0")
                recorrer(nodo.der, codigo + "1")

            recorrer(raiz)

            st.subheader("Códigos Huffman")
            st.table([
                {"Símbolo": s, "Código": codigos[s]}
                for s in codigos
            ])

            st.subheader("Bits totales")

            bits_totales = 0
            tabla_bits = []

            for s, f in frecuencias.items():
                L = len(codigos[s])
                bits = f * L
                bits_totales += bits

                tabla_bits.append({
                    "Símbolo": s,
                    "f": f,
                    "Código": codigos[s],
                    "L": L,
                    "f·L": bits
                })

            st.table(tabla_bits)
            st.success(f"TOTAL = {bits_totales} bits")

        except:
            st.error("Formato inválido. Use por ejemplo: A10, E7, I5, S5, O3, H2, Z2")
