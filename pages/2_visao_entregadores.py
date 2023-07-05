#Libraries
from haversine import haversine
from datetime  import datetime
import plotly.express as px
import folium
import plotly.express as px

# bibliotecas necessárias
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Entregadores', page_icon='' )


# =======================================================================================================================
# Funções
# =======================================================================================================================
def clean_code( df1 ):
    """ Esta função tem a responsabilidade de limpar o dataframe 

        Tipos de limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços das variáveis de texto
        4. Formatação das colunas de datas
        5. Limpeza da coluna de tempo ( Remoção do texto da variável numérica )

        Input: Dataframe
        Output: Dataframe    
    """
    
    # 1.convertendo a coluna Age de texto para número
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    
    
    linhas_selecionadas = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = df1['Festival'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # 2.convertendo a coluna Ratings de texto para número decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    
    # 3.convertendo a coluna Order_Date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    
    # 4.convertendo a coluna multiple_deliveries de texto para int
    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    # 6.removendo os espaços dentro de strings/texto/objects
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    
    # 7.limpando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1


def top_delivers( df1, top_asc ):
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
             .groupby(['City', 'Delivery_person_ID'])
             .mean()
             .sort_values(['City', 'Time_taken(min)']).reset_index())

    df2_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].tail(10)
    df2_aux02 = df2.loc[df2['City'] == 'Urban', :].tail(10)
    df2_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].tail(10)
    
    df3 = pd.concat([df2_aux01, df2_aux02, df2_aux03]).reset_index(drop=top_asc)

    return df3
    

    
# ================================ Início da Estrutura Lógica do Código =================================================

# ================================
# Import dataset
# ================================
df = pd.read_csv( 'train.csv' )

# ================================
# Limpando os dados
# ================================
df1 = clean_code( df )



# =======================================================================================================================
# Barra Lateral no Streamlit
# =======================================================================================================================
st.header('Marketplace - Visão Entregadores')

#image_path = 'logo.png'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fartest Delivery in Town' )
st.sidebar.markdown( """___""" )

st.sidebar.markdown( '## Selecione uma data limite' )
date_slider = st.sidebar.slider( 'Até qual valor?', 
                    value     = datetime.strptime(pd.to_datetime('2022-03-05').strftime('%Y-%m-%d'), '%Y-%m-%d'),
                    min_value = datetime.strptime(pd.to_datetime('2022-02-11').strftime('%Y-%m-%d'), '%Y-%m-%d'),
                    max_value = datetime.strptime(pd.to_datetime('2022-04-06').strftime('%Y-%m-%d'), '%Y-%m-%d'))

st.sidebar.markdown( """___""" )

traffic_options = st.sidebar.multiselect('Quais as condições de trânsito',
                      ['Low', 'Medium', 'High', 'Jam'],
                      default='Low')

conditions_options = st.sidebar.multiselect('Quais as condições climáticas',
                      ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
                      default='conditions Cloudy')

st.sidebar.markdown( """___""" )
st.sidebar.markdown( '### Powered by Comunidade DS' )

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, : ]


# Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, : ]


# Filtro de Condições Climáticas
condicoes_selecionadas = df1['Weatherconditions'].isin( conditions_options )
df1 = df1.loc[condicoes_selecionadas, : ]


# =======================================================================================================================
# Layout no Streamlit
# =======================================================================================================================
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '_', '_'] )

with tab1:
    with st.container():
        st.title( 'Overall Metrics' )
        col1, col2, col3, col4 = st.columns( 4, gap='large' )
        
        with col1:
            # A maior idade dos entregadores
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric( 'Maior de idade', maior_idade )

        with col2:
            # A menor idade dos entregadores
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric( 'Menor de idade', menor_idade )

        with col3:
            # A melhor condição de veículos
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric( 'Melhor condição', melhor_condicao )

        with col4:
            # A pior condição de veículos
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric( 'Pior condição', pior_condicao )

    with st.container():
        st.markdown("""___""")
        st.title( 'Avaliações' )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown( '##### Avaliação Média por Entregador' )
            df_aval_med_entregador = df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index().round(2)
            st.dataframe( df_aval_med_entregador )


        with col2:
            st.markdown( '##### Avaliação Média por Trânsito' )
            df_aval_med_trafico = (df1.loc[:, ['Road_traffic_density', 'Delivery_person_Ratings']]
                                      .groupby('Road_traffic_density')
                                      .agg({'Delivery_person_Ratings': ['mean', 'std']}))

            # mudança de nome das colunas
            df_aval_med_trafico.columns = ['delivery_mean', 'delivery_std']
            
            # reset do index
            df_aval_med_trafico = df_aval_med_trafico.reset_index()
            st.dataframe( df_aval_med_trafico )  

            
            st.markdown( '##### Avaliação Média por Clima' )
            df_aval_med_condclimatica = (df1.loc[condicoes_selecionadas, ['Weatherconditions', 'Delivery_person_Ratings']]
                                            .groupby('Weatherconditions')
                                            .agg({'Delivery_person_Ratings': ['mean', 'std']}))

            # mudança de nome das colunas
            df_aval_med_condclimatica.columns = ['delivery_mean', 'delivery_std']
            
            # reset do index
            df_aval_med_condclimatica = df_aval_med_condclimatica.reset_index()
            st.dataframe( df_aval_med_condclimatica ) 
            

        with st.container():
            st.markdown("""___""")
            st.title( 'Velocidade de Entrega' )

            col1, col2 = st.columns(2)

            with col1:
                st.markdown( '##### Top Entregadores mais rápidos' )
                df3 = top_delivers( df1, top_asc=True )
                st.dataframe(df3)

            with col2:
                st.markdown( '##### Top Entregadores mais lentos' )
                df3 = top_delivers( df1, top_asc=False )
                st.dataframe(df3)

                
                    
                    
                











        




