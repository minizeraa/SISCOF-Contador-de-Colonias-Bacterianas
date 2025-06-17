import math

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt, ticker
import streamlit as st
from math import sqrt, dist
from geneticalgorithm import geneticalgorithm as ga
from math import cos, sin

from skopt import gp_minimize

from detectar_colonias import detectar_colonias
from models.Circulo import Colonia

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

img = cv.imread(st.session_state['img_path'], cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

img = cv.medianBlur(img, 5)

th1 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
 cv.THRESH_BINARY,11,2)

th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
 cv.THRESH_BINARY,11,0)

petri_centro = st.session_state['petri_centro']
petri_raio = st.session_state['petri_raio']
precisao = 100
max_detect = 200

#progress_text = "Calculando coeficientes..."
#my_bar = st.progress(0, text=progress_text)


def get_coef(raio_min: int, raio_max: int):
    grafico = st.empty()
    pontos_acumulados = []
    coeficientes_acumulados = []

    def objetivo(coeficientes):
        coef = coeficientes[0]/precisao
        resultado = detectar_colonias(th1, raio_min=raio_min, raio_max=raio_max, sigma=coef, max=max_detect)
        pontos = 0

        for center_y, center_x, radius in resultado:

            i = th2[
                int(center_y - radius * sqrt(2) / 2):int(center_y + radius * sqrt(2) / 2),
                int(center_x - radius * sqrt(2) / 2):int(center_x + radius * sqrt(2) / 2)
            ]

            white = np.sum(i == 255)
            black = np.sum(i == 0)

            if black and white and (white * 100 / (white + black)) > 60:
                if dist(petri_centro, [center_x, center_y]) < petri_raio:
                    pontos += 1

        pontuacao = 1/pontos if pontos > 0 else 1
        st.text(f"{coef=:.2f} {pontos=:.2f} {pontuacao=:.2f}")
        print(f"{coef=:.2f} {pontos=:.2f} {pontuacao=:.2f}")

        pontos_acumulados.append(pontos)
        coeficientes_acumulados.append(coef)

        fig, ax = plt.subplots(figsize=(16, 4))
        sorted_indices = np.argsort(coeficientes_acumulados)
        ax.plot(np.array(coeficientes_acumulados)[sorted_indices], np.array(pontos_acumulados)[sorted_indices], 'o-',
                label='Pontos Acumulados')
        ax.set_xlabel('Coeficiente')
        ax.set_ylabel('Pontuação')
        ax.legend()
        ax.xaxis.set_major_locator(ticker.MaxNLocator(20))
        ax.grid(True)
        grafico.pyplot(fig)

        return pontuacao

    # Limites dos coeficientes
    limites = [(0 * precisao, 10 * precisao)]

    # Minimização usando otimização bayesiana
    resultado = gp_minimize(objetivo, limites, n_calls=50, random_state=42, initial_point_generator="sobol")

    # Melhores coeficientes encontrados
    return resultado.x[0]/precisao


raio_min = round(st.session_state['raio_min'] * 0.9)
raio_max = round(st.session_state['raio_max'] * 1.15)

raio_min, raio_max = st.slider(
    "Selecione o intervalo de raios para a detecção de colônias:",
    value=(raio_min, raio_max),
    max_value=raio_max*2)
st.text(f"Intervalos muito grandes ou pequenos causarão problemas de detecção.")

if st.checkbox("Subdivir pesquisa", value=True):
    point_division = st.number_input(
        "A partir do raio:",
        min_value=raio_min,
        max_value=raio_max,
        value=round(raio_min+(raio_max-raio_min)/3),
        step=1
    )
    colonias = []
    if st.button('Começar', use_container_width=True):
        coef1 = get_coef(raio_min, point_division)
        coef2 = get_coef(point_division, raio_max)
        st.text(f"Melhores coeficientes: {coef1} e {coef2}")
        colonias += list(detectar_colonias(th1, raio_min=raio_min, raio_max=point_division, sigma=coef1, max=1000))
        colonias += list(detectar_colonias(th1, raio_min=point_division, raio_max=raio_max, sigma=coef2, max=1000))
        st.session_state['colonias'] = [Colonia(y, x, r) for y, x, r in colonias]
else:
    if st.button('Começar', use_container_width=True):
        coef = get_coef(raio_min, raio_max)
        st.text(f"Melhor coeficiente: {coef}")
        colonias = list(detectar_colonias(
            th1,
            raio_min=raio_min,
            raio_max=raio_max,
            sigma=coef,
            max=10000
        ))
        st.session_state['colonias'] = [Colonia(y, x, r) for y, x, r in colonias]

if 'colonias' in st.session_state and st.button('Próximo passo', use_container_width=True):
    st.switch_page("pages/passo_3.py")

