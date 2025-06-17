import math
from typing import Literal

import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
from io import BytesIO
import base64
from loguru import logger

from models.Circulo import Circulo

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

ZOOM_FACTORS = 5
INIT_ZOOM = 1
ZOOM_DESLOCATIONS = 2
COLONY_RADIOUS_COLOR = 1/2
GRID_CIRCLE = 60


def zoom_image(img_array, zoom_factor=2):
    original_radius_x, original_radius_y = img_array.shape[1] // 2, img_array.shape[0] // 2
    x_chuck_desloc = st.session_state['x_factor_zoom']
    y_chuck_desloc = st.session_state['y_factor_zoom']
    x_chunk = img_array.shape[1] // many_zoom_chunks()
    y_chunk = img_array.shape[0] // many_zoom_chunks()

    center_x = original_radius_x + x_chuck_desloc * x_chunk
    center_y = original_radius_y + y_chuck_desloc * y_chunk
    radius_x, radius_y = original_radius_x // zoom_factor, original_radius_y // zoom_factor

    st.session_state['center'] = (center_x, center_y)
    logger.info(f"Original radius: ({original_radius_x}, {original_radius_y}).")
    logger.info(f"Chunk: ({x_chunk}, {y_chunk}). X: {x_chunk}. Y: {y_chunk}.")
    logger.info(f"Many zoom chunks:  {many_zoom_chunks()}")
    logger.info(f"Zoom: {zoom_factor}. Center: ({center_x}, {center_y}). Radius: ({radius_x}, {radius_y})")

    cropped_img = img_array[center_y - radius_y:center_y + radius_y, center_x - radius_x:center_x + radius_x]

    st.session_state['cropped_img_array'] = cropped_img

    cropped_pil_img = Image.fromarray(cropped_img)
    zoomed_pil_img = cropped_pil_img.resize((img_array.shape[1], img_array.shape[0]))
    zoomed_img = np.array(zoomed_pil_img)
    return zoomed_img


def many_zoom_chunks(log_zoom_factor: int = None) -> int:
    if 'log_zoom_factor' in st.session_state:
        log_zoom_factor = st.session_state['log_zoom_factor']
    return ZOOM_DESLOCATIONS * (2 ** (log_zoom_factor + 1)) \
        if log_zoom_factor != 0 else 1


def max_deslocation(sinal: Literal['+', '-']) -> int:
    if sinal == '+':
        return many_zoom_chunks() // 2 - ZOOM_DESLOCATIONS
    elif sinal == '-':
        return -many_zoom_chunks() // 2 + ZOOM_DESLOCATIONS


def change_zoom():
    img_array = st.session_state['img_array']
    original_radius_x, original_radius_y = img_array.shape[1] // 2, img_array.shape[0] // 2
    x_chunk = img_array.shape[1] // many_zoom_chunks()
    y_chunk = img_array.shape[0] // many_zoom_chunks()

    if st.session_state['log_zoom_factor'] == 0:
        st.session_state['x_factor_zoom'] = 0
        st.session_state['y_factor_zoom'] = 0
    else:
        st.session_state['x_factor_zoom'] = (st.session_state['center'][0] - original_radius_x) // x_chunk
        st.session_state['y_factor_zoom'] = (st.session_state['center'][1] - original_radius_y) // y_chunk

        if st.session_state['x_factor_zoom'] > max_deslocation('+'):
            st.session_state['x_factor_zoom'] = max_deslocation('+')
        elif st.session_state['x_factor_zoom'] < max_deslocation('-'):
            st.session_state['x_factor_zoom'] = max_deslocation('-')
        if st.session_state['y_factor_zoom'] > max_deslocation('+'):
            st.session_state['y_factor_zoom'] = max_deslocation('+')
        elif st.session_state['y_factor_zoom'] < max_deslocation('-'):
            st.session_state['y_factor_zoom'] = max_deslocation('-')

        logger.info(f"x_factor_zoom: {st.session_state['x_factor_zoom']}; max_deslocation: {max_deslocation('+')}")
        logger.info(f"y_factor_zoom: {st.session_state['y_factor_zoom']}; max_deslocation: {max_deslocation('+')}")


def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/jpg;base64,{img_str}" download="{filename}">{text}</a>'
    return href


def zoom():
    col1, col2, col3 = st.columns([0.4, 0.4, 0.2])
    tab_zoom, tab_circle = col2.tabs(["Zoom", "Círculo"])

    if 'zoom_circle_center_position' not in st.session_state:
        st.session_state['zoom_circle_center_position'] = (0, 0)
    if 'zoom_circle_radius' not in st.session_state:
        st.session_state['zoom_circle_radius'] = 0
    f_circle_radius = 0

    img = Image.open(st.session_state['img_path'])

    st.session_state['img_array'] = np.array(img)

    if 'cropped_img_array' not in st.session_state:
        st.session_state['cropped_img_array'] = st.session_state['img_array']

    if 'x_factor_zoom' not in st.session_state:
        st.session_state['x_factor_zoom'] = 0

    if 'y_factor_zoom' not in st.session_state:
        st.session_state['y_factor_zoom'] = 0

    if 'center' not in st.session_state:
        st.session_state['center'] = (0, 0)

    with tab_zoom:
        st.subheader("Zoom")
        st.session_state['zoom_factor'] = 2 ** st.slider("Fator", 0, ZOOM_FACTORS, INIT_ZOOM, label_visibility='collapsed',
                                                         key='log_zoom_factor', on_change=change_zoom)
        #st.divider()

        desloc_x_cols = st.columns(2)

        arrow_left, arrow_right = st.columns(2)
        with arrow_left:
            def move_left():
                st.session_state['x_factor_zoom'] -= 1
            st.button("←", on_click=move_left, use_container_width=True,
                      disabled=not st.session_state['x_factor_zoom'] > max_deslocation('-') or
                               st.session_state['log_zoom_factor'] == 0)
        with arrow_right:
            def move_right():
                st.session_state['x_factor_zoom'] += 1
            st.button("→", on_click=move_right, use_container_width=True,
                      disabled=not st.session_state['x_factor_zoom'] < max_deslocation('+') or
                               st.session_state['log_zoom_factor'] == 0)

        st.session_state['x_factor_zoom'] = st.slider(
            "SliderY",
            max_deslocation('-'), max_deslocation('+'),
            st.session_state['x_factor_zoom'], label_visibility="collapsed",
            disabled=st.session_state['log_zoom_factor'] == 0
        )

        #st.divider()
        arrows, sliders = st.columns(2)

        def move_up():
            st.session_state['y_factor_zoom'] -= 1
        st.button("↑", on_click=move_up, use_container_width=True,
                  disabled=not st.session_state['y_factor_zoom'] > max_deslocation('-') or
                           st.session_state['log_zoom_factor'] == 0)
        def move_down():
            st.session_state['y_factor_zoom'] += 1
        st.button("↓", on_click=move_down, use_container_width=True,
                  disabled=not st.session_state['y_factor_zoom'] < max_deslocation('+') or
                           st.session_state['log_zoom_factor'] == 0)


        st.session_state['y_factor_zoom'] = st.slider(
            "SliderX",
            max_deslocation('-'), max_deslocation('+'),
            st.session_state['y_factor_zoom'], label_visibility="collapsed",
            disabled=st.session_state['log_zoom_factor'] == 0
        )

    zoomed_img = zoom_image(st.session_state['img_array'], st.session_state['zoom_factor'])

    zoomed_img_pil = Image.fromarray(zoomed_img.astype('uint8'), 'RGB')

    with tab_circle:
        st.subheader("Círculo")

        size = min(zoomed_img_pil.size)

        draw = ImageDraw.Draw(zoomed_img_pil)
        logger.critical(f"Size: {zoomed_img_pil.size}")

        grid_unit = min(zoomed_img_pil.size[0], zoomed_img_pil.size[0]) // GRID_CIRCLE
        #grid_y_unit = zoomed_img_pil.size[1] // GRID_CIRCLE

        circle_radius = st.slider("Raio", GRID_CIRCLE//16, GRID_CIRCLE//2, GRID_CIRCLE//4, 1)

        circle_center = (
            st.slider("Centro X", GRID_CIRCLE//8, GRID_CIRCLE*7//8, GRID_CIRCLE//2, 1),
            st.slider("Centro Y", GRID_CIRCLE//8, GRID_CIRCLE*7//8, GRID_CIRCLE//2, 1)
        )

        p_circle = (
            grid_unit * circle_center[0] - circle_radius * grid_unit,
            grid_unit * circle_center[1] - circle_radius * grid_unit,
            grid_unit * circle_center[0] + circle_radius * grid_unit,
            grid_unit * circle_center[1] + circle_radius * grid_unit
        )

        logger.info(f"{p_circle=}")
        logger.info(f"{st.session_state['cropped_img_array'].shape=}")

        circle_proportion = (p_circle[2] - p_circle[0]) / zoomed_img_pil.size[0] / st.session_state['zoom_factor']

        radious = int(st.session_state['img_array'].shape[1] * circle_proportion // 2)

        draw.ellipse(xy=p_circle, fill=None, outline=(255, 0, 0), width=5)


        if radious < 8:
            st.error("Pequeno demais! Confira:\n-> Circular corretamente\n-> Ter imagem de maior resolução\n")

        def avarage_color(zoomed_img_pil, virtual_p_circle, radius):
            cropped_img_array = st.session_state['cropped_img_array']

            proportion = (
                zoomed_img_pil.size[0] // cropped_img_array.shape[1],
                zoomed_img_pil.size[1] // cropped_img_array.shape[0]
            )

            real_p_circle = (
                virtual_p_circle[0] // proportion[0],
                virtual_p_circle[1] // proportion[1],
                virtual_p_circle[2] // proportion[0],
                virtual_p_circle[3] // proportion[1]
            )

            colony_array = cropped_img_array[real_p_circle[1]:real_p_circle[3], real_p_circle[0]:real_p_circle[2]]
            colony = Image.fromarray(colony_array)
            #st.image(colony)

            l_squad = int(radius * math.sqrt(2) * COLONY_RADIOUS_COLOR)

            logger.info(f"{l_squad=} {radius=} {colony_array.shape=}")

            logger.info(f"{(radius*2 - l_squad) // 2=} {radius*2 - (radius - l_squad) // 2=}")

            inside_colony = colony_array[
                (radius*2 - l_squad) // 2:radius*2 - (radius - l_squad) // 2,
                (radius*2 - l_squad) // 2:radius*2 - (radius - l_squad) // 2
            ]

            #st.image(Image.fromarray(inside_colony))
            #color_cols = col3.columns(3)
            col3.image(colony, use_column_width=True)
            col3.markdown(f"**Raio:**\n :red[{radius} pixels]")
            avg_color = '#%02x%02x%02x' % tuple([int(n) for n in np.mean(inside_colony, axis=(0, 1))])
            c1, c2 = col3.columns(2)
            c1.markdown(f"**Cor:**\n :red[{avg_color}]")
            c2.color_picker("Cor média", avg_color, label_visibility='collapsed')
            p = [real_p_circle[0] + radius, real_p_circle[1] + radius]
            col3.markdown(f"**Posição do centro:**\n :red[{p[0]}, {p[1]}]")
            st.session_state['zoom_circle_center_position'] = p
            st.session_state['zoom_circle_radius'] = radius

        logger.info(f"{radious=}")
        avarage_color(zoomed_img_pil, p_circle, radious)

    col1.image(zoomed_img_pil)

    col1.markdown(get_image_download_link(zoomed_img_pil, "imagem_zoomada.jpg", "Baixar imagem com zoom"),
                  unsafe_allow_html=True)


zoom()
col1, col2, col3 = st.columns(3)
if col1.button('Definir círculo como "Placa de Petri"', use_container_width=True):
    st.session_state['petri_centro'] = st.session_state['zoom_circle_center_position']
    st.session_state['petri_raio'] = st.session_state['zoom_circle_radius']

if 'median_color_min' not in st.session_state:
    st.session_state['median_color_min'] = float('inf')

if col2.button('Definir círculo como "Colonia Pequena"', use_container_width=True):
    st.session_state['raio_min'] = st.session_state['zoom_circle_radius']
    circulo = Circulo(
        st.session_state['zoom_circle_center_position'][0],
        st.session_state['zoom_circle_center_position'][1],
        st.session_state['zoom_circle_radius']
    )
    median_color = circulo.get_median_color(st.session_state['cropped_img_array'])
    if median_color < st.session_state['median_color_min']:
        st.session_state['median_color_min'] = median_color * 0.85


if col3.button('Definir círculo como "Colonia Grande"', use_container_width=True):
    st.session_state['raio_max'] = st.session_state['zoom_circle_radius']

if 'petri_centro' in st.session_state and 'raio_min' in st.session_state and 'raio_max' in st.session_state:
    if st.button("Próximo passo", use_container_width=True):

        st.switch_page("pages/passo_2.py")


if 'petri_centro' in st.session_state:
    st.success(f'Placa de Petri definida como centro: {st.session_state["petri_centro"]} e raio: {st.session_state["petri_raio"]}')

if 'raio_min' in st.session_state:
    st.success(f'Colonia Pequena definida com raio: {st.session_state["raio_min"]}')

if 'raio_max' in st.session_state:
    st.success(f'Colonia Grande definida com raio: {st.session_state["raio_max"]}')
