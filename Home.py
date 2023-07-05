import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon=":")


#image_path = 'C:/Users/raquel.santos/Dropbox/Curso_DS_Foundation/2-ftc_analisando_dados_com_python/dataset/'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fartest Delivery in Town' )
st.sidebar.markdown( """___""" )

st.write( "# Curry Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadoes semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
        Indicadores semanais de crescimento dos restaurantes.
    ### Ask for Help
    - Time de Data Science do Discord
        - @raquelcoelho
    """
)