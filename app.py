import pandas as pd
import streamlit as st
import plotly.express as px



ruta = "https://github.com/Eddudiaz79-Orion/PASAJEROS/raw/refs/heads/main/data_sint_oper_pred_clas.csv.xls"

df = pd.read_csv(ruta)

#**** ANÁLISIS Y PROCESAMIENTO ****
df_tipo_vuelo = df['TIPO_VUELO'].value_counts().reset_index()
estadisticos = df_tipo_vuelo['count'].describe()
maximo = estadisticos["max"]
minimo = estadisticos["min"]
media = estadisticos["mean"]

#CONFIGUARACIÓN DE LA PÁGINA

st.set_page_config(
    page_title="Operaciones Acumuladas",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Ajuste del ancho maximo del contenedor principal a 1200 px 
st.markdown(
    '''
    <style>
        .block-container {
            max-width: 1200px;
        }
    </style>           
    ''',
    unsafe_allow_html=True
)

paleta_barras = px.colors.qualitative.Antique


st.image("encabezado.png")

#**** VISUALIZACIÓN DE LOS DATOS ****
st.title('Datos Operaciones')

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Máximo", f"{maximo:.0f}", "10%",border=True)
with col2:
    st.metric("Mínimo", f"{minimo:.0f}", "5%",border=True)
with col3:
    st.metric("Medio", f"{media:.0f}", "-7%",border=True)

with st.expander("Datos_Operaciones"):
    st.dataframe(df)


##################################################################
#################### ANÁLISIS Y PROCESAMIENTO#####################
##################################################################

#ESTADISTICOS DE LA COLUMNA "TIPO_VUELO""

df_tipo_vuelo = df["TIPO_VUELO"].value_counts().reset_index()
df_tipo_vuelo.columns = ["TIPO_VUELO","count"]
estadisticos = df_tipo_vuelo["count"].describe()
maximo = estadisticos["max"]
minimo = estadisticos["min"]
media = estadisticos["mean"]

# TOP 5 AEROPUERTOS CON MAYOR NÚMERO DE OPERACIONES
df_top5_ops_aeropuerto = df['AEROPUERTO_OPERACION'].value_counts().reset_index().head(5)
df_top5_ops_aeropuerto.columns = ['AEROPUERTO_OPERACION', 'count']

# TOP 10 RUTAS CON MAYOR NÚMERO DE OPERACIONES
df['RUTA'] = df['ORIGEN'] + ' ▶ ' + df['DESTINO']
df_top10_rutas = df['RUTA'].value_counts().reset_index().head(10)
df_top10_rutas.columns = ['RUTA', 'CANTIDAD']

#********* VISUALIZACION DE LOS DATOS *********
st.title('Datos Operaciones')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Mínimo', f'{minimo:.0f}', border=True)
with col2:
    st.metric('Media', f'{media:.0f}', border=True)
with col3:
    st.metric('Máximo', f'{maximo:.0f}', border=True)

with st.expander("Ver Matriz de Datos"):
    st.dataframe(df)

with st.expander("Top 5 Aeropuertos con Mayor Número de Operaciones"):
    st.dataframe(df_top5_ops_aeropuerto)

st.dataframe(df_top5_ops_aeropuerto)
with st.container(border=True):
    col4, col5 = st.columns(2)
    # ANÁLISIS DE LOS AEROPUERTOS CON MAYOR NUMERO DE OPERACIONES 
    with col4:
    
        fig_barras = px.bar(
            df_top5_ops_aeropuerto,
            x="AEROPUERTO_OPERACION",
            y="count",

            title="Top 5 Aeropuertos con mayor número de operaciones",
            labels={
                "AEROPUERTO_OPERACION": "Aeropuerto",
                "count": "Número de Operaciones"
                },
            color= "AEROPUERTO_OPERACION",
            color_discrete_sequence=paleta_barras
        )
        fig_barras.update_layout(showlegend=False)

        # Mostrar la grafica de barras

        st.plotly_chart(fig_barras, use_container_width=True)

    # DISEÑO DE DOS COLUMNAS PARA GRAFICOS

    with col5:
        # # ANÁLISIS DE RUTAS
        # Top 10 rutas con mayor numero de operaciones
        fig_rutas = px.bar (
            df_top10_rutas,
            x="CANTIDAD",
            y="RUTA",
            title="Top 10 rutas con mayor numero de operaciones",
            color= "CANTIDAD",
            color_continuous_scale="sunset"
        )
        fig_rutas.update_coloraxes(showscale=False)
        # Mostrar la grafica
        st.plotly_chart(fig_rutas,use_container_width=True)

tab1, tab2 = st.tabs(["Matriz de Datos","Grafica de barras"])

with tab1:
    st.dataframe(df_top10_rutas)
with tab2:
    df_top10_rutas=df_top10_rutas.sort_values("CANTIDAD", ascending=True)
    fig_rutas_2 = px.bar (
            df_top10_rutas,
            x="CANTIDAD",
            y="RUTA",
            title="Top 10 rutas con mayor número de operaciones",
            color= "CANTIDAD",
            color_continuous_scale="sunset"
        )
# Mostrar Grafico en tab2
    fig_rutas.update_coloraxes(showscale=False)
    st.plotly_chart(fig_rutas_2,use_container_width=True)

# PRUEBA DEL USO DE SLIDER DENTRO DE UN FORMULARIO
    with st.form('Análisis por Años'):
        slider_anio = st.slider('Selecciona el año', min_value=2010, max_value=2023, value=2025)
        enviado = st.form_submit_button('Analizar')

    st.subheader(f'Análisis de Operaciones en el año {slider_anio}')
    