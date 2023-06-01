# prueba_streamlit

import numpy as np
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from matplotlib.pyplot import figure
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

st.set_page_config(layout="wide")# Utilizar la página completa en lugar de una columna central estrecha

suicidios = pd.read_csv('Suicidios (1).csv', encoding='utf-8', sep = ";") # leer datos
    
suicidios=suicidios.drop("ID", axis=1)
suicidios.columns = ["Año", "Sexo", "Edad", "Mes", "DiaSemana", "Departamento", "Municipio", "Causa", "Estado", "Latitude (y)", "Longitude (x)"]
suicidios['Año'].value_counts() #2016 a 2018
suicidios['Sexo'].value_counts() #Mayoria Hombres
suicidios['Edad'].value_counts() #Mayoria de 20 a 29 años
suicidios['Mes'].value_counts() #
suicidios['DiaSemana'].value_counts() #Mayoria Domingo
suicidios['Departamento'].value_counts() #Mayoria Antioquia
suicidios['Municipio'].value_counts() #Mayoria Bogota
suicidios['Causa'].value_counts() #Todos son suicidios... Eliminar variable
suicidios['Estado'].value_counts() #Todos son casos definitivos-confirmados... Eliminar variable
suicidios=suicidios.drop(["Causa", "Estado"], axis=1)
suicidios['Municipio']=suicidios['Municipio'].apply(lambda x: x.lower())
suicidios['Departamento']=suicidios['Departamento'].apply(lambda x: x.lower())
suicidios["Departamento"].value_counts() #Borrar el que es sin Inf
suicidios=suicidios[suicidios['Departamento'] != "sin información"].reset_index() # sin inf borrado
    
def sintilde(cadena):
    replacements = (
    ("á", "a"),
    ("é", "e"),
    ("í", "i"),
    ("ó", "o"),
    ("ú", "u")
    )
    for a, b in replacements:
        cadena = cadena.replace(a, b)
    return cadena

#San Andrés
suicidios.loc[suicidios["Departamento"]=='archipiélago de san andrés',"Departamento"] = "san andres"
    
#bogotá d.c.
suicidios.loc[suicidios["Departamento"]=='bogotá',"Departamento"] = "bogota d.c."
    
suicidios["Departamento"]=suicidios["Departamento"].apply(lambda x: sintilde(x))

if not st.sidebar.checkbox("Ocultar página principal", False, key='1'):
    # Título principal, h1 denota el estilo del título 1
    
    st.markdown("<h1 style='text-align: center; color: #3C9AD0;' > ANÁLISIS DESCRIPTIVO DE LOS SUICIDIOS Y SU RELACIÓN CON FACTORES EXTERNOS </h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: left; color: #73C6B6;' > Objetivo: Caracterizar los suicidios en Colombia y su relación con factores externos y tecnológicos</h1>", unsafe_allow_html=True)
    st.sidebar.title ("ANÁLISIS DESCRIPTIVO DE LOS SUICIDIOS Y SU RELACIÓN CON FACTORES EXTERNOS")
    st.sidebar.markdown ("Navegador")
    
    
    # VISUALIZACIÓN SUICIDIOS
    
    
    st.markdown("<h2 style='text-align: left; color: #F7DC6F ;' > Rangos de edades </h1>", unsafe_allow_html=True)
    

    #st.write(suicidios)
    
    # GRAFICO DE BARRAS PARA COMPARAR LAS EDADES
    # crear dataset
    base = suicidios.groupby(['Edad'])[['Municipio']].count().sort_values('Municipio', ascending = False).reset_index()
    
    # crear gráfica
    fig = px.bar(base, x = 'Edad', y='Municipio', color="Edad",
                 title= '<b> CANTIDAD DE SUICIDIOS POR EDAD<b>',
                 color_discrete_sequence=px.colors.sequential.thermal)
    
    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'EDADES',
        yaxis_title = 'Número de Suicidios',
        template = 'simple_white',
        title_x = 0.5)
    
    st.plotly_chart(fig)
    
    st.markdown("<h2 style='text-align: left; color: #F7DC6F ;' > Sexo </h1>", unsafe_allow_html=True)
    
    # GRAFICO DE BARRAS PARA COMPARAR LAS EDADES y SEXO
    # crear dataset
    base = suicidios.groupby(['Edad', "Sexo"])[['Municipio']].count().sort_values('Municipio', ascending = False).reset_index()
    
    # crear gráfica
    fig = px.bar(base, x = 'Edad', y='Municipio', color="Sexo",
                 title= '<b> CANTIDAD DE SUICIDIOS POR EDAD y SEXO <b>',
                 color_discrete_sequence=px.colors.qualitative.Dark24)
    
    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'EDADES',
        yaxis_title = 'NÚMERO DE SUICIDIOS',
        template = 'simple_white',
        title_x = 0.5)
    
    st.plotly_chart(fig)
    
    
    st.markdown("<h2 style='text-align: left; color: #F7DC6F ;' > Día de la semana </h1>", unsafe_allow_html=True)
    
    # GRAFICO DE BARRAS PARA COMPARAR DIAS
    # crear dataset
    base = suicidios.groupby(['DiaSemana'])[['Municipio']].count().sort_values('Municipio', ascending = False).reset_index()
    
    # crear gráfica
    fig = px.bar(base, x = 'DiaSemana', y='Municipio', color="DiaSemana",
                 title= '<b> CANTIDAD DE SUICIDIOS POR DÍA <b>',
                 color_discrete_sequence=px.colors.qualitative.Bold)
    
    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'DÍA',
        yaxis_title = 'NÚMERO DE SUICIDIOS',
        template = 'simple_white',
        title_x = 0.5)
    
    st.plotly_chart(fig)
    
    
    st.markdown("<h2 style='text-align: left; color: #F7DC6F ;' > Departamento </h1>", unsafe_allow_html=True)

    suicidios['Latitude (y)']=suicidios['Latitude (y)'].apply(lambda x: float(x.replace(',', '.')))
    suicidios['Longitude (x)']=suicidios['Longitude (x)'].apply(lambda x: float(x.replace(',', '.')))
    
    df=suicidios[["Longitude (x)", "Latitude (y)"]]
    df.columns=["lon", "lat"]

    st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=5,
         longitude=-75,
         zoom=5,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=20000,
            elevation_scale=5,
            elevation_range=[0, 55000],
            pickable=True,
            extruded=True,
         ),
     ],
 ))
    


###############################################################################################################

#ANÁLISIS DE SUICIDIOS E INTERNET

internet = pd.read_csv('Internet.csv', sep = ",") # leer datos


internet['Municipio']=internet['Municipio'].apply(lambda x: x.lower())
internet['Departamento']=internet['Departamento'].apply(lambda x: x.lower())

internet=internet[internet["Ano"] != 2017]
internet['Ano'].unique() #Del 2018 al 2020
internet.columns = ["Año", "Trimestre", "Departamento", "Municipio", "Accesos_Fijos", "Poblacion", "Indice"]


# Hacer un checkbox


if st.sidebar.checkbox('Relación entre suicidios e internet', False):
    
    base=internet.groupby(["Departamento", "Año"])["Indice"].sum().reset_index()
    base["Año"]=base["Año"].astype(str)

    # crear gráfica
    fig = px.bar(base, x = 'Departamento', y='Indice', color="Año",
            title= '<b> INDICE DE INTERNET POR DEPARTAMENTO<b>',
            color_discrete_sequence=px.colors.qualitative.Vivid)

    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'Departamento',
        yaxis_title = 'Índice de Internet',
        template = 'simple_white',
        title_x = 0.5)

    # Enviar tabla a streamlitblack
    st.plotly_chart(fig)
    
    TablaAgregada=suicidios.groupby(["Año","Departamento"])[["Municipio"]].count().reset_index()
    TablaAgregada.columns=['Año','Departamento', 'Suicidios']

    ##Suicidios-Internet
    BD1=pd.merge(TablaAgregada,internet, on=['Año', "Departamento"], how = 'inner') # dejando solos los años y departamentos en común
    fig, ax = plt.subplots();
    sns.heatmap(BD1.corr(), ax=ax);

    st.pyplot(fig)

#ANÁLISIS DE SUICIDIOS E INNOVACIÓN

innovacion = pd.read_csv('Innovacion.csv', encoding='utf-8', sep=";") # leer datos
# Hacer un checkbox

if st.sidebar.checkbox('Relación entre suicidios e innovación', False):

        
    innovacion['Puntaje']=innovacion['Puntaje'].apply(lambda x: float(x.replace(',', '.')))
    innovacion.columns=["Departamento", "Año", "Indice", "Posicion", "Puntaje", "Grupo"]
    
    innovacion['Departamento']=innovacion['Departamento'].apply(lambda x: x.lower())
    
    #San Andrés
    
    innovacion.loc[innovacion["Departamento"]=='san andres y providencia',"Departamento"] = "san andrés"
    
    #bogotá d.c.
    
    innovacion.loc[innovacion["Departamento"]=='bogotá & cundinamarca',"Departamento"] = "cundinamarca" #esta base no tiene una clase especifica para solo bogotá
    
    innovacion["Departamento"]=innovacion["Departamento"].apply(lambda x: sintilde(x))
    
    
    TablaAgregada=suicidios.groupby(["Año","Departamento"])[["Municipio"]].count().reset_index()
    TablaAgregada.columns=['Año','Departamento', 'Suicidios']
    
    #Suicidios-Innovacion
    BD2=pd.merge(TablaAgregada,innovacion,on=['Año', "Departamento"], how = 'inner') # dejando solos los años y departamentos en común
    
    #### HEAT MAP
    fig, ax = plt.subplots();
    sns.heatmap(BD2.corr(), ax=ax);
    st.pyplot(fig)
    
    
    
    #### PAIRPLOT
    
    variables=["Suicidios", "Posicion", "Puntaje", "Grupo"]
    fig = sns.pairplot(BD2.loc[:,variables], diag_kind="kde", height=2)
    st.pyplot(fig)





#ANÁLISIS DE SUICIDIOS E INVERSION

inversion = pd.read_csv('Inversion.csv', sep = ";", decimal=",") # leer datos
inversion=inversion.convert_dtypes()
columnas=inversion.columns[1:]
for i in columnas:
  inversion[i]=inversion[i].apply(lambda x: float(x.replace(',', '.').strip('%')) / 100.0)

inversion=inversion.rename(columns = {'Ano':'Año'})
inversion=inversion.drop(20, axis=0)
inversion["Año"] = pd.to_datetime(inversion['Año'], format="%Y")
inversion["Año"] = pd.DatetimeIndex(inversion['Año']).year

# Hacer un checkbox


if st.sidebar.checkbox('Relación entre suicidios e inversión', False):
    
    TablaAgregada=suicidios.groupby(["Año","Departamento"])[["Municipio"]].count().reset_index()
    TablaAgregada.columns=['Año','Departamento', 'Suicidios']
    
    ACTI=pd.melt(inversion, id_vars =['Año'], value_vars =inversion.loc[:,inversion.columns.str.contains("ACTI")].columns)
    ACTI.columns=["Año", "DepartamentoACTI", "ACTI"]
    ID=pd.melt(inversion, id_vars =['Año'], value_vars =inversion.loc[:,inversion.columns.str.contains("_I+")].columns)
    ID.columns=["Año","DepartamentoID", "ID"]
    ACTI['DepartamentoACTI']=ACTI['DepartamentoACTI'].apply(lambda x: x.replace("_ACTI", ""))

    ID['DepartamentoID']=ID['DepartamentoID'].apply(lambda x: x.replace("_I+D", ""))
    
    ID.columns=["Año","Departamento", "ID"]
    ACTI.columns=["Año", "Departamento", "ACTI"]
    

    ID=ID[ID["Departamento"] != "COLOMBIA"]
    ACTI=ACTI[ACTI["Departamento"] != "COLOMBIA"]

    ACTI['Departamento']=ACTI['Departamento'].apply(lambda x: x.lower())
    ID['Departamento']=ID['Departamento'].apply(lambda x: x.lower())

    ##Corregir escritura:
    ACTI.loc[ACTI["Departamento"]=='bogota, d.c.',"Departamento"] = "bogota d.c."
    ID.loc[ID["Departamento"]=='bogota, d.c.',"Departamento"] = "bogota d.c."

    ACTI.loc[ACTI["Departamento"]=='cindinamarca',"Departamento"] = "cundinamarca"
    ID.loc[ID["Departamento"]=='cindinamarca',"Departamento"] = "cundinamarca"

    ACTI.loc[ACTI["Departamento"]=='narino',"Departamento"] = "nariño"
    ID.loc[ID["Departamento"]=='narino',"Departamento"] = "nariño"
   
    
    #Suicidios-Inversión
    BD3=pd.merge(TablaAgregada,ACTI, on=['Año', "Departamento"], how = 'inner') # dejando solos los años y departamentos en común
    BD3=pd.merge(BD3,ID, on=['Año', "Departamento"], how = 'inner')
    
    #HEATMAP
    fig, ax = plt.subplots();
    sns.heatmap(BD3.corr(), ax=ax);
    st.pyplot(fig)


    #PAIRPLOT
    variables=["Suicidios", "ACTI", "ID"]
    fig = sns.pairplot(BD3.loc[:,variables], diag_kind="kde", height=2)
    st.pyplot(fig)
    
    
