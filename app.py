import streamlit as st
from PyPDF2 import PdfReader
from collections import Counter
import math
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
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
        ["Escribir frecuencias", "Subir archivo (.txt o .pdf)"]
    )

    entrada = ""

    # ==============================
    # ENTRADA POR ARCHIVO
    # ==============================

    if opcion == "Subir archivo (.txt o .pdf)":
        archivo = st.file_uploader(
            "Suba un archivo (.txt o .pdf)",
            type=["txt", "pdf"]
        )

        if archivo:
            if archivo.type == "application/pdf":
                reader = PdfReader(archivo)
                for page in reader.pages:
                    texto_pdf = page.extract_text()
                    if texto_pdf:
                        entrada += texto_pdf
            else:
                entrada = archivo.read().decode("utf-8")

    # ==============================
    # ENTRADA MANUAL
    # ==============================

    elif opcion == "Escribir frecuencias":
        entrada = st.text_area(
            "Ingrese las frecuencias (ej: A10, E7, I5, S5, O3, H2, Z2)"
        )

    # ==============================
    # PROCESAMIENTO
    # ==============================

    if entrada:
        try:
            # ======= Procesar frecuencias =======
            frecuencias = {}
            partes = entrada.replace(" ", "").replace("\n", ",").split(",")
            for p in partes:
                if p == "":
                    continue
                simbolo = p[0].upper()
                freq = int(p[1:])
                frecuencias[simbolo] = freq

            st.subheader(" Lista inicial de frecuencias")
            st.table([{"Símbolo": s, "f": f} for s, f in frecuencias.items()])

            # ======= Crear nodos para Huffman =======
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
            estado_listas = []
            estado_listas.append(
                sorted([(n.simbolo, n.freq) for n in heap], key=lambda x: x[1])
            )

            contador_paso = 1
            while len(heap) > 1:
                n1 = heappop(heap)
                n2 = heappop(heap)

                nuevo = Nodo(n1.simbolo + n2.simbolo, n1.freq + n2.freq)
                nuevo.izq = n1
                nuevo.der = n2

                pasos.append({
                    "Paso": contador_paso,
                    "Símbolo 1": n1.simbolo,
                    "f1": n1.freq,
                    "Símbolo 2": n2.simbolo,
                    "f2": n2.freq,
                    "Nueva combinación": nuevo.simbolo,
                    "Suma": nuevo.freq
                })

                heappush(heap, nuevo)

                estado_listas.append(
                    sorted([(n.simbolo, n.freq) for n in heap], key=lambda x: x[1])
                )

                contador_paso += 1

            raiz = heap[0]

            # ======= Mostrar proceso =======
            st.subheader(" Sumas sucesivas paso a paso")
            st.table(pasos)

            st.subheader(" Evolución de la lista")
            for i, estado in enumerate(estado_listas):
                texto_estado = " , ".join([f"{s}{f}" for s, f in estado])
                if i == 0:
                    st.write(f"Estado inicial → {texto_estado}")
                else:
                    st.write(f"Después del paso {i} → {texto_estado}")

            # ======= Generar códigos Huffman =======
            codigos = {}
            def recorrer(nodo, codigo=""):
                if nodo.izq is None and nodo.der is None:
                    codigos[nodo.simbolo] = codigo
                    return
                recorrer(nodo.izq, codigo + "0")
                recorrer(nodo.der, codigo + "1")

            recorrer(raiz)

            st.subheader(" Códigos Huffman")
            st.table([{"Símbolo": s, "Código": codigos[s]} for s in codigos])

            # ======= Calcular bits totales =======
            bits_totales = 0
            tabla_bits = []
            for s, f in frecuencias.items():
                L = len(codigos[s])
                bits = f * L
                bits_totales += bits
                tabla_bits.append({"Símbolo": s, "f": f, "Código": codigos[s], "L": L, "f·L": bits})

            st.subheader(" Bits totales")
            st.table(tabla_bits)
            st.success(f"TOTAL = {bits_totales} bits")

            # ======= VISUALIZACIÓN DEL ÁRBOL HUFFMAN =======
                        # ======= VISUALIZACIÓN DEL ÁRBOL HUFFMAN =======
            def dibujar_arbol(nodo):
                G = nx.DiGraph()
                labels = {}

                def agregar_nodos(n, padre=None):
                    if n is None:
                        return
                    G.add_node(id(n))
                    labels[id(n)] = f"{n.simbolo}\n{n.freq}"
                    if padre:
                        G.add_edge(id(padre), id(n))
                    agregar_nodos(n.izq, n)
                    agregar_nodos(n.der, n)

                agregar_nodos(nodo)

                # -------- POSICIÓN JERÁRQUICA REAL --------
                def jerarquia_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
                    pos = {}

                    def _jerarquia_pos(G, node, width=1., vert_gap=0.2,
                                       vert_loc=0, xcenter=0.5, pos=None):
                        if pos is None:
                            pos = {node: (xcenter, vert_loc)}
                        else:
                            pos[node] = (xcenter, vert_loc)

                        children = list(G.successors(node))
                        if len(children) != 0:
                            dx = width / len(children)
                            nextx = xcenter - width/2 - dx/2
                            for child in children:
                                nextx += dx
                                pos = _jerarquia_pos(G, child, width=dx,
                                                     vert_gap=vert_gap,
                                                     vert_loc=vert_loc-vert_gap,
                                                     xcenter=nextx,
                                                     pos=pos)
                        return pos

                    return _jerarquia_pos(G, root, width, vert_gap, vert_loc, xcenter)

                root_id = id(nodo)
                pos = jerarquia_pos(G, root_id)

                # -------- FIGURA --------
                plt.figure(figsize=(14,8))
                ax = plt.gca()
                ax.set_facecolor("#1e1e1e")
                plt.axis("off")

                nx.draw(
                    G,
                    pos,
                    with_labels=False,
                    node_size=3000,
                    node_color="#f1c40f",
                    edge_color="#f1c40f",
                    linewidths=2,
                    node_shape="o"
                )

                nx.draw_networkx_labels(
                    G,
                    pos,
                    labels,
                    font_color="black",
                    font_size=11,
                    font_weight="bold"
                )

                st.subheader(" Visualización del Árbol Huffman")
                st.pyplot(plt)
                plt.clf()

            dibujar_arbol(raiz)

        except:
            st.error("Formato inválido. Use por ejemplo: A10, E7, I5, S5, O3, H2, Z2")

            
# ======================================================
# PORTADA DEL PROYECTO
# ======================================================


st.markdown("""
###  Integrantes

- **Jesús Alberto Simaj Say** - 202108020  
- **Castillo Osorio Mario Alfredo** - 202108018  
- **Jordy Herbert Enrique Cotton Diaz** - 202308027  

---
""")
