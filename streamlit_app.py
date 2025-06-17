import os
import pickle

import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

uploadedfile = st.file_uploader("Selecione a imagem", type=['png', 'jpeg', 'jpg'])
print(uploadedfile)
if uploadedfile is not None:
    st.session_state['img_path'] = r"images/" + uploadedfile.name
    with open(os.path.join("images", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())

if st.button("Começar..."):
    st.switch_page("pages/passo_1.py")