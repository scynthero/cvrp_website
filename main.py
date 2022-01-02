import time
from io import StringIO

import streamlit as st
from stqdm import stqdm
from cvrp import *

st.header('CVRP')
st.subheader('Parametry modelu')

vehicle_count = st.number_input('Liczba dostępnych pojazdów')
# st.write('Liczba pojazdów ', vehicle_count)
capacity = st.number_input('Pojemność pojazdu')
# st.write('Pojemność ', capacity)
uploaded_file = st.file_uploader("Wgraj plik z danymi")
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    # st.write(stringio)
    # To read file as string:
    string_data = stringio.read()
    # st.write(string_data)

if not vehicle_count or not capacity or not uploaded_file:
    st.info('Podaj parametry i wgraj plik')
else:
    if st.button('Uruchom obliczenia'):
        results = main(string_data, int(vehicle_count), int(capacity))
        st.subheader('Wyniki')
        col1, col2 = st.columns(2)
        col1.metric(label="Liczba wykorzystanych pojazdów", value=f"{len(results[0])}")
        col2.metric(label="Wartość funkcji celu", value=f"{results[1]:.2f}")

        text_contents = f'''Zbiór tras:\n'''
        for route in results[0]:
            print(route)
            text_contents += str(route) + "\n"

        st.download_button('Pobierz zbiór tras', text_contents)
