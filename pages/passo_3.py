import base64
import math
from typing import TypedDict
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from loguru import logger
import pandas as pd
import cv2 as cv
import io
from PIL import Image

from models.Circulo import Circulo, Colonia

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

petri_centro = st.session_state['petri_centro']
petri_raio = st.session_state['petri_raio']
precisao = 10000


def desenhar_colonias(imagem, colonias: list[Colonia]) -> plt.Figure:
    fig, ax = plt.subplots()
    ax.imshow(imagem, cmap=plt.cm.gray)
    for colonia in colonias:
        circy, circx = circle_perimeter(colonia.y, colonia.x, colonia.raio)
        ax.scatter(circx, circy, color='red', s=0.5)  # 'r' indica a cor vermelha
    return fig


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


def colonias_dataframe(colonias: list[Colonia]) -> pd.DataFrame:
    with io.BytesIO() as buffer:
        #fig.savefig(buffer, format='png')
        data = base64.encodebytes(buffer.getvalue()).decode("utf-8")
    for colonia in colonias:
        yield {
            "x": colonia.x,
            "y": colonia.y,
            "raio": colonia.raio,
        }


pil_img_array = np.array(Image.open(st.session_state['img_path']))
img = cv.imread(st.session_state['img_path'])
cv_img = cv.medianBlur(cv.imread(st.session_state['img_path'], cv.IMREAD_GRAYSCALE), 5)
th1 = cv.adaptiveThreshold(cv_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
th2 = cv.adaptiveThreshold(cv_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 0)

st.session_state['img'] = img
st.session_state['th1'] = th1
st.session_state['th2'] = th2


class ColoniaListData(TypedDict):
    colonias: list[Colonia]
    coeficientes: list[float]
    raw_imgs_data: list[str]
    th2_imgs_data: list[str]
    is_a_colony: list[bool]


class ColoniaList:
    def __init__(self, colonias: list[Colonia]):
        self.data: ColoniaListData = {
            'colonias': colonias,
            'coeficientes': [0.0 for _ in colonias],
            'raw_imgs_data': ['' for _ in colonias],
            'th2_imgs_data': ['' for _ in colonias],
            'is_a_colony': [False for _ in colonias]
        }
        self.pos_defined = False

    def get_data(self) -> ColoniaListData:
        sorted_indices = sorted(range(len(self.data['coeficientes'])), key=lambda i: self.data['coeficientes'][i], reverse=True)

        # Reordenar todas as listas do dicionário usando os índices ordenados
        self.data['colonias'] = [self.data['colonias'][i] for i in sorted_indices]
        self.data['coeficientes'] = [self.data['coeficientes'][i] for i in sorted_indices]
        self.data['raw_imgs_data'] = [self.data['raw_imgs_data'][i] for i in sorted_indices]
        self.data['th2_imgs_data'] = [self.data['th2_imgs_data'][i] for i in sorted_indices]
        self.data['is_a_colony'] = [self.data['is_a_colony'][i] for i in sorted_indices]
        return self.data

    def get_confirmed_colonies(self) -> list[Colonia]:
        return [colonia for colonia, is_colony in zip(self.data['colonias'], self.data['is_a_colony']) if is_colony]

    def draw_colonies(self, img):
        return desenhar_colonias(img, self.get_confirmed_colonies())

    def set_min_coef(self, coef_min: float):
        for i, coef in enumerate(self.data['coeficientes']):
            self.data['is_a_colony'][i] = coef > coef_min

    def get_table(self) -> pd.DataFrame:
        df_data: dict[str, list] = {}
        if not self.pos_defined:
            df_data = {
                'colonias': self.data['colonias'],
                'coeficientes': self.data['coeficientes']
            }
        else:
            df_data = self.data
        return pd.DataFrame(df_data)

    def pos_definitions(self):
        self.data['coeficientes'] = self.get_coeficientes()
        self.data['raw_imgs_data'] = self.get_imgs_data(st.session_state['img'])
        self.data['th2_imgs_data'] = self.get_imgs_data(st.session_state['th2'])
        self.pos_defined = True

    @staticmethod
    def get_uniformity(img):
        uni = img.astype(np.float32) / 255
        blur_uni = cv.GaussianBlur(uni, (11, 11), 2)
        for i in range(10):
            blur_uni = cv.GaussianBlur(blur_uni, (11, 11), 2)
        last_blur_uni = cv.GaussianBlur(blur_uni, (11, 11), 2)
        ssd_blur_uni = np.sum((last_blur_uni - blur_uni) ** 2)
        return ssd_blur_uni * 1000

    def get_coeficientes(self) -> list[float]:
        img = st.session_state['img']

        coeficientes = []

        #for colonia in self.data['colonias']:
        #    i = colonia.get_croped_img(img)

        for colonia in self.data['colonias']:
            i = colonia.get_croped_img_in(img)
            coef = colonia.get_darker_median_color(i)
            coeficientes.append(coef)

        return coeficientes

    def get_imgs_data(self, img) -> list[str]:
        imgs_data = []
        for colonia in self.data['colonias']:
            try:
                imgs_data.append(colonia.get_data_img(img))
            except SystemError as e:
                logger.warning(f'Erro ao tentar obter a imagem de {colonia}', e)
                imgs_data.append('')
        return imgs_data

    def __iter__(self):
        for colonia in self.data['colonias']:
            yield colonia

    def __getitem__(self, index):
        return self.data['colonias'][index]

    def __len__(self):
        return len(self.data['colonias'])

    def __repr__(self):
        return f"ColoniaList({self.data['colonias']})"


filtered_colonias = []

raio_min = st.session_state['raio_min']
raio_max = st.session_state['raio_max']

all_colonies = st.session_state['colonias']
st.text(f'Colonias detectadas: {len(list(st.session_state["colonias"]))}')

for colonia in all_colonies:
    if colonia.get_distance(petri_centro) < petri_raio:
        is_russian_doll = False
        for smaller_colony in filter(lambda c: c.raio < colonia.raio, all_colonies):
            if smaller_colony.get_distance((colonia.x, colonia.y)) < colonia.raio:
                is_russian_doll = True
                break
        if not is_russian_doll:
            filtered_colonias.append(colonia)

colonias = ColoniaList(filtered_colonias)
colonias.pos_definitions()
del filtered_colonias

coef_min = st.number_input('Coeficiente Mínimo', min_value=0.0, max_value=255.0, value=0.0, step=0.1, key='coef_min')
colonias.set_min_coef(coef_min)

col1, col2 = st.columns(2)
colonias.data['is_a_colony'] = col1.data_editor(
    colonias.get_data(),
    column_config={
        "raw_imgs_data": st.column_config.ImageColumn(
            "Raw Image", help="Streamlit app preview screenshots"
        ),
        "th2_imgs_data": st.column_config.ImageColumn(
            "Th2 Image", help="Streamlit app preview screenshots"
        )
    },
    hide_index=True,
)['is_a_colony']
col1.text(f'Colonias contabilizadas: {len(colonias.get_confirmed_colonies())}')
col2.pyplot(colonias.draw_colonies(img))


import zipfile
from io import BytesIO


def decodificar_base64(base64_string):
    return base64.b64decode(base64_string.split(',')[1])


def criar_zip(lista_imgs_base64):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for idx, base64_string in enumerate(lista_imgs_base64):
            img_data = decodificar_base64(base64_string)
            img_name = f'imagem_{idx}.png'
            zip_file.writestr(img_name, img_data)
    buffer.seek(0)
    return buffer


def filter_imgs(imgs: list[str], is_a_colony: list[bool], polarity: bool = True) -> list[str]:
    return [img for img, is_colony in zip(imgs, is_a_colony) if is_colony == polarity]


img_colonias = criar_zip(filter_imgs(colonias.data['raw_imgs_data'], colonias.data['is_a_colony'], True))
img_nao_colonias = criar_zip(filter_imgs(colonias.data['raw_imgs_data'], colonias.data['is_a_colony'], False))


col1.download_button(
    label="Baixar Imagens Colonias",
    data=img_colonias,
    file_name="colonias.zip",
    mime="application/zip"
)

col1.download_button(
    label="Baixar Imagens Não-Colonias",
    data=img_nao_colonias,
    file_name="nao_colonias.zip",
    mime="application/zip"
)