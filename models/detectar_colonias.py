import numpy as np
import streamlit as st
from skimage.feature import canny
from skimage.transform import hough_circle, hough_circle_peaks

from models.Circulo import Colonia


@st.cache_data
def detectar_colonias(img, raio_min, raio_max, sigma, max) -> list[Colonia]:
  imagem = img
  imagem_gray = imagem
  im = imagem

  edges = canny(im, sigma=sigma)

    # Definir os raios possíveis para as colônias
  hough_radii = np.arange(raio_min, raio_max, 2)

  # Realizar a transformação de Hough
  hough_res = hough_circle(edges, hough_radii)

  # Selecionar os picos mais proeminentes
  accums, cx, cy, radii = hough_circle_peaks(
      hough_res, hough_radii, min_xdistance=raio_min, min_ydistance=raio_min, total_num_peaks=max)

  return [Colonia(x, y, raio) for x, y, raio in zip(cx, cy, radii)]