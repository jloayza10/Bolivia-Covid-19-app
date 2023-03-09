import streamlit as st
import pandas as pd
import numpy as np
import json
import locale
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import plotly.graph_objects as go


#locale.setlocale(locale.LC_TIME, 'es_ES')

df = pd.read_pickle(r'./Step_1-Parse/data/df_covid_Bolivia.pickle')
df_monthly_mean = pd.read_pickle(r'./Step_1-Parse/data/df_monthly_mean.pickle')
df_weekly_mean = pd.read_pickle(r'./Step_1-Parse/data/df_weekly_mean.pickle')
Bolivia_deptos = json.load(open('./Step_0-Raw/data/departamentos_Bolivia.geojson', 'r'))
ciudades = ['Beni', 'Chuquisaca', 'Cochabamba', 'La Paz', 'Oruro', 'Pando', 'Potosi', 'Santa Cruz',
            'Tarija', 'Bolivia']
tipo = ['Positivos', 'Muertes', 'Recuperados',
        'Total Positivos', 'Total Muertes', 'Total Recuperados',
        'Positivos por 100k hab.', 'Muertes por 100k hab.', 'Recuperados por 100k hab.']  # 'Total Activos',
tiempo = ['Por mes', 'Por semana', 'Últimos 15 días']
promedios = ['Diario', '7 días', '14 días', 'Por mes']
graph_types = ['Cuadros de Resumen', 'Gráficos por fecha', 'Mapa']
graph_time_types = ['Gráficos individuales', 'Un solo gráfico']
map_types = [ 'Por Fecha', 'Mapa actual']

mapbox_styles = ["open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain",
                 "stamen-toner", "stamen-watercolor"]

tipo_color_dict = {'Positivos': ['#55BCC9', '#659DBD', '#05386B', '#97CAEF', '#240090', '#190061'],
                   'Muertes': ['#111111', '#474853'],
                   'Recuperados': ['#AFD275', '#8EE4AF'],
                   'Total Positivos': ['#05386B', '#659DBD'],
                   'Total Activos': ['#8E8268', '#8E8268'],
                   'Total Muertes': ['#FC4445', '#474853'],
                   'Total Recuperados': ['#379683', '#8EE4AF'],
                   'Positivos por 100k hab.': ['#55BCC9', '#97CAEF'],
                   'Muertes por 100k hab.': ['#515557', '#515557'],
                   'Recuperados por 100k hab.': ['#AFD275', '#AFD275']
                   }


def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = hex_color * 2
    return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)


def scatter_trace(figure,dataframe,var,ciudad,hover_str):
    figure.add_trace(go.Scatter(x=dataframe[dataframe["Ciudad"] == ciudad].Fecha,
                                y=dataframe[dataframe["Ciudad"] == ciudad][var],
                                name=ciudad,
                                hovertemplate=ciudad + '<br>Fecha: %{x:%d}<br>' +
                                           f'{hover_str}: ' +
                                           '%{y:.1f}<extra></extra>',
                                showlegend=True,
                                #marker_color=tipo_color_dict[multi_tipos_1][0],
                                )
                     )


def bar_trace(figure,dataframe,var,ciudad):
    df_not_na = dataframe[dataframe['Total Positivos'].notna()]
    df_bar = df_not_na[df_not_na['Fecha'] == df_not_na['Fecha'].max()].sort_values(var, ascending=True)
    figure.add_trace(go.Bar(x=df_bar[df_bar["Ciudad"] == ciudad][var],
                            y=df_bar[df_bar["Ciudad"] == ciudad].Ciudad,
                            name=ciudad,
                            hovertemplate=ciudad + f'<br>{var}:' +' %{x}<extra></extra>',
                            showlegend=False,
                            text=df_bar[df_bar["Ciudad"] == ciudad][var],
                            orientation='h',
                            marker_color="#05386B",
                            )
                     )
def bar_trace_1(figure,dataframe,var,ciudad):
    df_not_na = dataframe[dataframe['Total Positivos'].notna()]
    df_bar = df_not_na[df_not_na['Fecha'] == df_not_na['Fecha'].max()].sort_values(var, ascending=True)
    figure.add_trace(go.Bar(x=df_bar[df_bar["Ciudad"] == ciudad][var],
                            y=df_bar[df_bar["Ciudad"] == ciudad].Ciudad,
                            name=ciudad,
                            hovertemplate=ciudad + f'<br>{var}:' +' %{x}<extra></extra>',
                            showlegend=False,
                            text=df_bar[df_bar["Ciudad"] == ciudad][var],
                            orientation='h',
                            marker_color="#05386B",
                            width=0.3,
                            )
                     )
def update_plot_bar(var):
    fig.update_layout(title=var + ' por departamento seleccionado',
                      title_x=0.5,
                      height=600,
                      width=850,
                      autosize=True,
                      font={'color': 'black'},
                      yaxis={'categoryorder':'total ascending'}
                      )
    fig.update_xaxes(title=var,
             title_standoff=4,
             nticks=10,
             ticks="outside",
             tickcolor='black',
             )
    fig.update_yaxes(title='',
                     ticks="outside",
                     tickcolor='black',
                     )

def plot_scatter_M_mean(figure,var,ciudad,hover_str):
    figure.add_trace(go.Scatter(x=df_monthly_mean[df_monthly_mean["Ciudad"]==ciudad].Fecha.dt.strftime('%m-%Y'),
                                y=df_monthly_mean[df_monthly_mean["Ciudad"]==ciudad][var],
                                mode='lines+markers',
                                name=ciudad,
                                hovertemplate=ciudad + '<br>Mes-Año: %{x:%d}<br>' +
                                           '{}: '.format(hover_str) +
                                           '%{y:.1f}<extra></extra>',
                                showlegend=True,
                                )
                     )

def update_plot(hover_str,title_str):
    fig.update_layout(title=tipo_selected + title_str,
                      title_x=0.5,
                      height= 600,
                      width=850,
                      autosize=True,
                      font={'color': 'black'}
                      )
    fig.update_xaxes(title="Fecha",
             title_standoff=4,
             tickformat='%m-%Y',
             nticks=10,
             ticks="outside",
             tickcolor='black',
             )
    fig.update_yaxes(title=hover_str,
                     title_standoff=4,
                     ticks="outside",
                     tickcolor='black',
                     #tick0=0,
                     zeroline=True,
                     rangemode="tozero",
                     )
Fecha_max = df['Fecha'].max().strftime('%d-%m-%Y')


st.set_page_config(page_title="Covid-19 Bolivia Dashboard",layout='wide')
#st.title("Visualización Covid-19 en Bolivia")
st.markdown("<h1 style='text-align: center; color: black;'>Visualización Covid-19 en Bolivia</h1>", unsafe_allow_html=True)
st.caption(f"Fecha de la última actualización de datos: {Fecha_max}")
st.sidebar.title("Opciones de visualizaciones")
#st.sidebar.header("Opciones de gráficos")

sidebar_type = st.sidebar.selectbox("", graph_types)

if sidebar_type == graph_types[0]: # Tablas de Resumen
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("Click para escoger los departamentos"):
            container0 = st.container()
            all_ciudades_0 = st.checkbox("Seleccionar todo", key=1)
            if all_ciudades_0:
                multi_ciudades_0 = container0.multiselect("",
                                                          ciudades,
                                                          ciudades)
            else:
                multi_ciudades_0 = container0.multiselect("",
                                                          ciudades,
                                                          default='Bolivia')

    with col2:
        with st.expander("Click para escoger las variables"):

            container_1 = st.container()
            all_tipos_1 = st.checkbox("Seleccionar todo", key=2)
            if all_tipos_1:
                multi_tipos_1 = container_1.multiselect("",
                                                        tipo[:4],
                                                        tipo[:3])
            else:
                multi_tipos_1 = container_1.multiselect("",
                                                        tipo[:3],
                                                        default='Positivos'
                                                        )
    for i, multi_tipo in enumerate(multi_tipos_1):
        if (i % 2) == 0:
            with col1:
                var_table = [multi_tipo, 'Total ' + multi_tipo, multi_tipo + ' por 100k hab.']
                df_table = df[(df['Ciudad'].isin(multi_ciudades_0)) & (df['Fecha'] == df['Fecha'].max())][
                    ['Ciudad', *var_table]]
                df_table.columns = ['Ciudad',
                                    var_table[0] + '<br>de la fecha',
                                    'Total',
                                    'Por 100k hab.<br>media 14 días'
                                    ]
                fig = ff.create_table(df_table.round(2))
                col1.subheader(multi_tipo + f"\n Fecha: {Fecha_max}")
                st.plotly_chart(fig, use_container_width=True)
        if (i % 2) == 1:
            with col2:
                var_table = [multi_tipo, 'Total ' + multi_tipo, multi_tipo + ' por 100k hab.']
                df_table = df[(df['Ciudad'].isin(multi_ciudades_0)) & (df['Fecha'] == df['Fecha'].max())][
                    ['Ciudad', *var_table]]
                df_table.columns = ['Departamento',
                                    var_table[0] + '<br>de la fecha',
                                    'Total',
                                    'Por 100k hab.<br>media 14 días'
                                    ]
                fig = ff.create_table(df_table.round(2))
                col2.subheader(multi_tipo + f"\n Fecha: {Fecha_max}")
                st.plotly_chart(fig, use_container_width=True)

if sidebar_type == graph_types[1]: # Gráficos por fecha
    sidebar_plot = st.sidebar.selectbox("Cómo ver los gráficos",
                                        graph_time_types)
    if sidebar_plot == graph_time_types[0]:# Gráficos individuales

        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Click para escoger los departamentos"):
                container0 = st.container()
                all_ciudades_0 = st.checkbox("Seleccionar todo", key=1)
                if all_ciudades_0:
                    multi_ciudades_0 = container0.multiselect("",
                                                              ciudades,
                                                              ciudades)
                else:
                    multi_ciudades_0 = container0.multiselect("",
                                                              ciudades,
                                                              default='Bolivia')

        with col2:
            with st.expander("Click para escoger la variable"):
                tipo_selected = st.selectbox("",tipo)
        fig = make_subplots(rows=(len(multi_ciudades_0) // 2 + (len(multi_ciudades_0) % 2 > 0)),
                            cols=2,
                            subplot_titles=['temp_subtitle' for ciudad in np.arange(len(multi_ciudades_0))],
                            print_grid=True,
                            )
        i = 1

        for ciudad in multi_ciudades_0:

            fig.add_trace(go.Bar(x=df[df["Ciudad"] == ciudad].Fecha,
                                 y=df[df["Ciudad"] == ciudad][tipo_selected],
                                 name=ciudad,
                                 hovertemplate=ciudad + '<br>Fecha: %{x:%d}<br>' +
                                               f'{tipo_selected}: ' +
                                               '%{y:.1f}<extra></extra>',
                                 showlegend=True,
                                 marker_color=tipo_color_dict[tipo_selected][0],
                                 ),
                          row=(i // 2 + (i % 2 > 0)),
                          col=(i % 2) + 2 * ((i + 1) % 2)
                          )
            fig.layout.annotations[i - 1]['text'] = ciudad
            fig.layout.annotations[i - 1]['font'] = {'size': 20, 'color': 'black'}

            if tipo_selected in tipo[:3]:
                max_tipo_avg7 = df[df["Ciudad"] == ciudad][tipo_selected + '_avg7'].max()
                fig.add_trace(go.Scatter(x=df[df["Ciudad"] == ciudad].Fecha,
                                         y=df[df["Ciudad"] == ciudad][tipo_selected + '_avg7'],
                                         mode='lines',
                                         name=ciudad,
                                         fill='tozeroy',
                                         hovertemplate=ciudad + '<br>Fecha: %{x:%d-%m-%Y}<br>' +
                                                       'Promedio {}: '.format(tipo_selected) +
                                                       '%{y:.1f}<extra></extra>',
                                         showlegend=True,
                                         # marker_color = tipo_color_dict[sidebar_tipo][0],
                                         fillcolor=f"rgba{(*hex_to_rgb(tipo_color_dict[tipo_selected][0]), 0.3)}",
                                         line_color=tipo_color_dict[tipo_selected][1],
                                         # opacity=0.95,
                                         ),
                              row=(i // 2 + (i % 2 > 0)),
                              col=(i % 2) + 2 * ((i + 1) % 2),
                              )
                fig.add_annotation(
                    x=df[df["Ciudad"] == ciudad].loc[df[tipo_selected + '_avg7'] == max_tipo_avg7]['Fecha'].iloc[-1],
                    y=max_tipo_avg7,
                    ax=df[df["Ciudad"] == ciudad].loc[df[tipo_selected + '_avg7'] == max_tipo_avg7]['Fecha'].iloc[
                           -1] - pd.Timedelta((df['Fecha'].max() - df['Fecha'].min()) / 10),
                    ay=max_tipo_avg7,
                    xref='x' + (str(i) if i != 1 else ''),
                    yref='y' + (str(i) if i != 1 else ''),
                    axref='x' + (str(i) if i != 1 else ''),
                    ayref='y' + (str(i) if i != 1 else ''),
                    text=tipo_selected + "<br>Promedio<br>7 días",
                    font=dict(size=10,
                              color=tipo_color_dict[tipo_selected][1]),
                    xshift=-3,
                    yshift=-2,
                    # xanchor='right',
                    # yanchor='top',
                    arrowcolor=tipo_color_dict[tipo_selected][1],
                    arrowwidth=2,
                    showarrow=True,
                    arrowhead=0,
                    row=(i // 2 + (i % 2 > 0)),
                    col=(i % 2) + 2 * ((i + 1) % 2),
                    )

            if len(multi_ciudades_0) == 1:
                fig.update_xaxes(domain=[0, 1])
                fig.layout.annotations[0].update(x=0.5)

            i = i + 1
        if len(multi_ciudades_0) == 1:
            fig_height = 600
            fig_width = 850
            titlex = 0.5
        elif len(multi_ciudades_0) <= 4:
            fig_height = 600
            fig_width = 1150
            titlex = 0.5

        elif len(multi_ciudades_0) <= 8:
            fig_height = 730
            fig_width = 1150
            titlex = 0.5
        else:
            fig_height = 1000
            fig_width = 1150
            titlex = 0.5
        fig.update_layout(
            title=tipo_selected + """ por departamento<br>Colocar el mouse sobre cada gráfico para obtener info. adicional.""",
            title_x=titlex,
            height=fig_height,
            width=fig_width,
            # autosize=True,
            showlegend=False,
            font={'color': 'black'}
            )
        fig.update_xaxes(title="Fecha",
                         title_standoff=4,
                         tickformat='%m-%Y',
                         nticks=10,
                         ticks="outside",
                         tickcolor='black',
                         )
        fig.update_yaxes(title=tipo_selected,
                         title_standoff=4,
                         )
        st.plotly_chart(fig)

    if sidebar_plot == graph_time_types[1]: # Gráfico único
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Click para escoger los departamentos"):
                container0 = st.container()
                all_ciudades_0 = st.checkbox("Seleccionar todo", key=1)
                if all_ciudades_0:
                    multi_ciudades_0 = container0.multiselect("",
                                                              ciudades,
                                                              ciudades)
                else:
                    multi_ciudades_0 = container0.multiselect("",
                                                              ciudades,
                                                              default='Bolivia')

        with col2:
            with st.expander("Click para escoger la variable"):
                tipo_selected = st.selectbox("",tipo,index=3)
        # if tipo_selected in np.array(tipo)[np.r_[0:3, 6:9]]:
        if tipo_selected in tipo[:3]:
            with col2:
                with st.expander("Click para escoger promedio"):
                    promedio_selected = st.selectbox("",promedios)
            fig = go.Figure()
            df_plot = None
            if promedio_selected==promedios[0]:
                tipo_plot = tipo_selected
                df_plot = df
                hover_str = 'Datos diarios de '+tipo_selected
                title_str = ''
            elif promedio_selected==promedios[1]:
                tipo_plot = tipo_selected+'_avg7'
                df_plot = df
                hover_str = 'Promedio 7 días de ' + str(tipo_selected)
                title_str = '<br>Promedio móvil 7 días'
            elif promedio_selected==promedios[2]:
                tipo_plot = tipo_selected+'_avg14'
                df_plot = df
                hover_str = 'Promedio 14 días de ' + str(tipo_selected)
                title_str = '<br>Promedio móvil 14 días'
            elif promedio_selected == promedios[3]:
                hover_str = 'Promedio mensual de ' + str(tipo_selected)
                title_str= '<br>Promedio mensual'
                for ciudad in multi_ciudades_0:
                    plot_scatter_M_mean(fig, tipo_selected, ciudad,hover_str)

            if df_plot is None:
                pass
            else:
                for ciudad in multi_ciudades_0:
                    scatter_trace(fig,df_plot,tipo_plot,ciudad,hover_str)

            update_plot(hover_str,title_str)

            st.plotly_chart(fig)
        if tipo_selected in tipo[6:]:
            fig = go.Figure()
            for ciudad in multi_ciudades_0:
                hover_str = ' ' + str(tipo_selected)
                title_str = '<br>(Promedio 14 días)'
                scatter_trace(fig,df,tipo_selected,ciudad,hover_str)
            update_plot(hover_str,title_str)
            st.plotly_chart(fig)
        if 'Total' in tipo_selected:
            fig = go.Figure()
            if len(multi_ciudades_0) == 1:
                for ciudad in multi_ciudades_0:
                    bar_trace_1(fig,df,tipo_selected,ciudad)
                update_plot_bar(tipo_selected)

            else:
                for ciudad in multi_ciudades_0:
                    bar_trace(fig,df,tipo_selected,ciudad)
                update_plot_bar(tipo_selected)
            st.plotly_chart(fig)


if sidebar_type == graph_types[2]: # Mapa

    with st.expander("Seleccionar tipo de mapa"):
        map_type = st.selectbox("",map_types)
    col1, col2 = st.columns(2)
    if map_type == map_types[0]:
        with col1:
            with st.expander("Seleccionar período temporal"):
                selectbox_tiempo = st.selectbox("", tiempo, key=3)

        if selectbox_tiempo == 'Por mes':
            with col2:
                with st.expander("Seleccionar variable"):
                    selectbox_tipos = st.selectbox("", tipo[:3], key=4)
            title_str="Promedio mensual de " + selectbox_tipos + """ por departamento.<br>Mapa interactivo, el botón \"Play\" inicia la animación."""
            fig = px.choropleth_mapbox(
                df_monthly_mean[df_monthly_mean.Ciudad != 'Bolivia'],
                locations="id",
                geojson=Bolivia_deptos,
                color=selectbox_tipos,
                color_continuous_scale='ice_r',  # https://plotly.com/python/builtin-colorscales/
                animation_frame='Fecha_str',
                range_color=[0, df_monthly_mean[df_monthly_mean.Ciudad != 'Bolivia'][selectbox_tipos].max()],
                hover_name="Ciudad",
                hover_data={'Fecha_str': True, tipo[0]: True, tipo[1]: True, tipo[2]: True, 'id': False},
                mapbox_style=mapbox_styles[0],
                center={"lat": -16, "lon": -64},
                zoom=3.7,
                opacity=0.8,
                title=title_str,
            )

            # print("plotly express hovertemplate:", fig.data[0].hovertemplate)
            fig.update_traces(
                hovertemplate='<b>%{hovertext}</b><br>Mes: %{customdata[0]}<br>Positivos: %{z:.1f}<br>Muertes: %{customdata[2]:.1f}<br>Recuperados: %{customdata[3]:.1f}')
            for f in fig.frames:
                f.data[0].update(
                    hovertemplate='<b>%{hovertext}</b><br>Mes: %{customdata[0]} <br>Positivos: %{z:.1f}<br>Muertes: %{customdata[2]:.1f}<br>Recuperados: %{customdata[3]:.1f}')
            fig.update_layout(sliders=[dict(currentvalue={"prefix": "Mes: "})],
                              height=550,
                              width=800,
                              title_x=0.5)
            # print("plotly express hovertemplate:", fig.data[0].hovertemplate)
            st.plotly_chart(fig)

        if selectbox_tiempo == 'Por semana':
            with col2:
                with st.expander("Seleccionar variable"):
                    selectbox_tipos = st.selectbox("", tipo[:3], key=4)
            title_str="Promedio semanal de " + selectbox_tipos + """ por departamento.<br>Mapa interactivo, el botón \"Play\" inicia la animación."""
            fig = px.choropleth_mapbox(
                df_weekly_mean[df_weekly_mean.Ciudad != 'Bolivia'],
                locations="id",
                geojson=Bolivia_deptos,
                color=selectbox_tipos,
                color_continuous_scale='ice_r',
                animation_frame='wk-AA',
                range_color=[0, df_weekly_mean[df_weekly_mean.Ciudad != 'Bolivia'][selectbox_tipos].max()],
                hover_name="Ciudad",
                hover_data={'wk-AA': True, tipo[0]: True, tipo[1]: True, tipo[2]: True, 'id': False},
                mapbox_style=mapbox_styles[0],
                center={"lat": -16, "lon": -64},
                zoom=3.7,
                opacity=0.7,
                title=title_str,
            )

            # print("plotly express hovertemplate:", fig.data[0].hovertemplate)
            fig.update_traces(
                hovertemplate='<b>%{hovertext}</b><br>Semana: %{customdata[0]}<br>Positivos: %{z:.1f}<br>Muertes: %{customdata[2]:.1f}<br>Recuperados: %{customdata[3]:.1f}')
            for f in fig.frames:
                f.data[0].update(
                    hovertemplate='<b>%{hovertext}</b><br>Semana: %{customdata[0]} <br>Positivos: %{z:.1f}<br>Muertes: %{customdata[2]:.1f}<br>Recuperados: %{customdata[3]:.1f}')
            fig.update_layout(sliders=[dict(currentvalue={"prefix": "Semana: "})],
                              title_x=0.5,
                              height=550,
                              width=800,)
            # print("plotly express hovertemplate:", fig.data[0].hovertemplate)
            st.plotly_chart(fig)
        if selectbox_tiempo == 'Últimos 15 días':
            with col2:
                with st.expander("Seleccionar variable"):
                    selectbox_tipos = st.selectbox("", tipo, key=2)
            title_str="Evolución de " + selectbox_tipos + " en los últimos 15 días."
            fig = px.choropleth(
                df.loc[df['Fecha'].ge(df['Fecha'].max() - pd.Timedelta(days=15)) & (df.Ciudad != 'Bolivia')],
                locations="id",
                geojson=Bolivia_deptos,
                color=selectbox_tipos,
                color_continuous_scale='ice_r',
                animation_frame='Fecha_str2',
                range_color=[0,
                             df.loc[df['Fecha'].ge(df['Fecha'].max() - pd.Timedelta(days=15)) & (df.Ciudad != 'Bolivia')][
                                 selectbox_tipos].max()],
                hover_name="Ciudad",
                hover_data={'Fecha_str2': False, 'id': False},
                center={"lat": -16, "lon": -64},
                title=title_str,
            )

            fig.add_traces(go.Scattergeo(
                locations=df["id"],
                geojson=Bolivia_deptos,
                text=df['Ciudad'],
                textposition="middle center",
                mode='text',
                hoverlabel=None,
                hovertext=None,
                hoverinfo='skip',
                showlegend=False
            ))

            fig.update_geos(fitbounds="locations", visible=True)
            fig.update_layout(sliders=[dict(currentvalue={"prefix": "Fecha: "})],
                              title_x=0.5,
                              height=550,
                              width=800,)

            st.plotly_chart(fig)

    if map_type == map_types[1]:
        with col1:
            with st.expander("Seleccionar variable"):
                selectbox_tipos = st.selectbox("", tipo, key=1)
        fig = px.choropleth_mapbox(
            df[(df['Fecha'] == df['Fecha'].max()) & (df.Ciudad != 'Bolivia')],
            locations="id",
            geojson=Bolivia_deptos,
            color=selectbox_tipos,
            color_continuous_scale='ice_r',
            hover_name="Ciudad",
            # hover_data = tipo[:3],
            hover_data={'Fecha_str': True, tipo[0]: True, tipo[1]: True, tipo[2]: True, tipo[3]: True,
                        tipo[4]: True, tipo[5]: True, tipo[6]: True, tipo[7]: True, tipo[8]: True,
                        'id': False},
            title=selectbox_tipos + """ por departamento.<br>Colocar el mouse sobre cada departamento
    para obtener info. adicional.""",
            mapbox_style=mapbox_styles[0],
            center={"lat": -16, "lon": -64},
            zoom=4,
            opacity=0.7,
        )
        print("plotly express hovertemplate:", fig.data[0].hovertemplate)
        fig.update_traces(
            hovertemplate='<b>%{hovertext}</b><br>Fecha: %{customdata[0]}<br>Positivos: %{customdata[1]}<br>Muertes: %{customdata[2]}<br>Recuperados: %{customdata[3]}<br>Total Positivos: %{customdata[4]}<br>Total Muertes: %{customdata[5]}<br>Total Recuperados: %{customdata[6]}<br>Positivos por 100k hab. : %{customdata[7]:.2f}<br>Muertes por 100k hab. : %{customdata[8]:.2f}<br>Recuperados por 100k hab. : %{customdata[9]:.2f}')
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig)


# Footer

footer1="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
.test {
position: relative;
display:block;
#left: 0;
#bottom: 0;
padding: 5px;
top: 80px;
#width: 100%;
background-color: transparent;
color: #343a40;
text-align: center;
}
p {
  font-size: 0.87em;
}
</style>

<div class="test">
<p>Desarrollado por 
  <a style='display: inline-block; text-align: left;' href="https://www.github.com/jloayza10" 
  target="_blank">Jorge Loayza R
  </a></p>
  <p>Datos: 
 <a style='display: inline-block; text-align: center;'
  href="https://lookerstudio.google.com/u/0/reporting/92796894-acf3-4ab7-9395-20655de351f7/page/p_3ga366rsuc" 
  target="_blank">Gobierno Boliviano
 </a>.
  
</p>
</div>
"""

st.markdown(footer1,unsafe_allow_html=True)
