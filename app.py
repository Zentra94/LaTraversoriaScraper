import streamlit as st
from PIL import Image
from config import PATH_STATICS_IMAGES
from packages.core.rappi_scraper import RappiParser
from packages.core.utils import to_excel

st.write('# La Traversoria Scrapper (V 1.0)')
st.text("by: Franco Zentilli")

PLACES = ["Rappi", "Uber Eats", "Pedidos Ya"]
PARSERS = {"Rappi": RappiParser}


image = Image.open(PATH_STATICS_IMAGES / "LT_logo.jpg")
st.image(image)

place = st.selectbox("Seleciona la empresa", PLACES)
parser = PARSERS[place]()
categories = parser.categories
category = st.selectbox("Seleciona la categoría", categories.keys())
limit = st.number_input("Máximo número de búsquedas", 5)
if st.button("Submit"):
    st.write("Comenzando scrapping en {} para {} ...".format(place, category))
    restaurants_urls = parser.get_restaurants_urls(category=category)
    restaurants_results = parser.get_restaurants_results(restaurants_urls=restaurants_urls,
                                                         limit=limit)

    df_xlsx = to_excel(restaurants_results)
    st.download_button(label='📥 Descargar resultados',
                       data=df_xlsx,
                       file_name='restaurants_results.xlsx')

    st.balloons()







