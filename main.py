# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 12:02:09 2021

@author: Anthony Segura García

e-mail: asegura@imn.ac.cr

Instituto Meteorológico Nacional
Departamento de Red Meteorológica y Procesamiento de Datos
"""

#Se cargan las librerías
import pandas as pd
import numpy as np
import plotly.express as px

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc

from tabs import tab_1_horarios
from tabs import tab_2_diarios

from Graph_functions import *

import glob
import fnmatch

external_scripts = ["https://cdn.plot.ly/plotly-locale-es-latest.js"]

#Se crea el Dashboard
app = dash.Dash(__name__,
                update_title = 'Cargando...',
                meta_tags = [{"name": "viewport", "content": "width=device-width, initial-scale=2"}],
                external_scripts = external_scripts,
                external_stylesheets = [dbc.themes.DARKLY],
                suppress_callback_exceptions=True)

# #Esta función evita los mensajes de errores al llamar layouts que no están en main.py
# app.config['suppress_callback_exceptions'] = True

app.title = "RBD"

config_plots = dict(locale = "es")

#Lee todos los archivos de Rangos máximos y mínimos
filenames = glob.glob('../Datos_T/*.csv')

report_files_H_cuenca_35 = glob.glob('../../../Proyecto_Revision_BD/EJ_TEMP_H_C69/Report_lim_cuenca/datos_LSD_*.txt')

report_files_H_cuenca_P = glob.glob('../../../Proyecto_Revision_BD/EJ_TEMP_H_C69/Report_lim_cuenca/datos_LCP_*.txt')

report_files_H_est_35 = glob.glob('../../../Proyecto_Revision_BD/EJ_TEMP_H_C69/Report_lim_est/datos_LSD_*.txt')

report_files_H_est_P = glob.glob('../../../Proyecto_Revision_BD/EJ_TEMP_H_C69/Report_lim_est/datos_LP_*.txt')

report_files_H_dif = glob.glob('../../../Proyecto_Revision_BD/EJ_TEMP_H_C69/Report_diff/datos_LDIFF_P_*.txt')

report_files_D_cuenca = glob.glob('../../../Proyecto_Revision_BD/EJ_TEMP_DM_C69/Report_lim_cuenca/datos_LC_M*.txt')

report_files_D_est_MN = glob.glob('../../../Proyecto_Revision_BD/EJ_TEMP_DM_C69/Report_lim_est/datos_LE_MN*.txt')

report_files_D_est_MX = glob.glob('../../../Proyecto_Revision_BD/EJ_TEMP_DM_C69/Report_lim_est/datos_LE_MX*.txt')

def files(files, num_est, delim):
    df = pd.read_csv(fnmatch.filter(files,"*"+num_est+"*")[0], delimiter = delim)
    
    return df

estaciones = ["633", "647", "677", "679", "681", "695", "697", "699", "701",
              "709", "711", "713", "717", "719", "721", "723", "725", "727",
              "729", "731", "735", "737", "739", "743", "747", "749", "751"]


#Se agregan las características de la app/dashboard
app.layout = dbc.Container([
    
    html.Div(id = "blank_output"),
    #Se coloca el título del dash

    html.Div(dbc.Row([
                dbc.Col(
                    dbc.Card(
                        html.H1("Proyecto Revisión de la Base de Datos",
                             className = 'text-center text-white'),
                        color="primary",
                        body=False),
                className = "mb-4" ,
                width = 12)
            ])
    ),

    html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Cuenca"),
                    dbc.CardBody([
                        dcc.Dropdown(id = "slct_bsn",
                            options = [{"label": "69", "value": "69"}],
                            multi = False,
                            value = '69',
                            style = {'width': '100%'}
                        )
                    ])
                ],
                color = "danger", outline=True),
            width={"size": "auto"},),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Estación"),
                    dbc.CardBody([
                        dcc.Dropdown(id = "slct_est",
                            options = [{'label': x, 'value': x} for x in estaciones],
                            multi = False,
                            value = '633',
                            style = {'width': '105%'}
                        )
                    ])
                ], 
                color = "danger", outline=True),
            width={"size": "auto"},),
        ],  justify = "start",
            className="g-0",)
    ]),

    #Se crean las pestañas
        dbc.Card([
            dbc.CardHeader(
                dbc.Tabs([
                    dbc.Tab(label = 'Horarios',
                            tab_id = 'tab-1',
                            activeLabelClassName="text-warning"),
                    dbc.Tab(label = 'Diarios',
                            tab_id = 'tab-2',
                            activeLabelClassName="text-success")],
                    id = "tabs",
                    active_tab="tab-1",
                )
            ),
            dbc.CardBody(
                html.Div(id = 'tabs-content')
            )
            
        ],
        color = "light")
        
])

@app.callback(
    Output(component_id = 'tabs-content', component_property = 'children'),
    Input(component_id = 'tabs', component_property = 'active_tab')
)

def content(tab):
    if tab == 'tab-1':
        return tab_1_horarios.tab_1_layout
    elif tab == 'tab-2':
        return tab_2_diarios.tab_2_layout

############# HORARIOS #############    

@app.callback(
    [Output(component_id = 'output_H_container', component_property = 'children'),
    Output(component_id = 'variable_HG_box', component_property = 'figure')],
    [Input(component_id = 'slct_H_var', component_property = 'value'),
     Input(component_id = 'slct_bsn', component_property = 'value'),
     Input(component_id = 'slct_est', component_property = 'value')]
)

def HG_box(option_slctd, bsn_slctd, est_slctd):
    
    container = "{}".format(option_slctd)

    file = files(filenames, '\\T_'+str(bsn_slctd)+str(est_slctd), ",")

    fig = box_plot(file, option_slctd)

    return container, fig

@app.callback(
    Output(component_id = 'variable_H_Hist', component_property = 'figure'),
    [Input(component_id = 'slct_H_var', component_property = 'value'),
     Input(component_id = 'slct_bsn', component_property = 'value'),
     Input(component_id = 'slct_est', component_property = 'value')]
)

def H_hist(option_slctd, bsn_slctd, est_slctd):
    
    file = files(filenames, '\\T_'+str(bsn_slctd)+str(est_slctd), ",") 
 
    fig = hist_plot(file, option_slctd)
    
    return fig

@app.callback(
    Output(component_id = 'variable_H_graph', component_property = 'figure'),
    [Input(component_id = 'slct_H_var', component_property = 'value'),
     Input(component_id = 'range_slider', component_property = 'value'),
     Input(component_id = 'slct_bsn', component_property = 'value'),
     Input(component_id = 'slct_est', component_property = 'value')]
)

def update_H_graph(option_slctd, year_slctd, bsn_slctd, est_slctd):
  
    file = files(filenames, '\\T_'+str(bsn_slctd)+str(est_slctd), ",") 
    
    fig = line_plot(file, option_slctd, year_slctd)

    return fig

@app.callback(
    Output(component_id = 'variable_H_box_year', component_property = 'figure'),
    [Input(component_id = 'slct_H_var', component_property = 'value'),
      Input(component_id = 'range_slider', component_property = 'value'),
      Input(component_id = 'slct_bsn', component_property = 'value'),
      Input(component_id = 'slct_est', component_property = 'value')]
)

def H_box(option_slctd, year_slctd, bsn_slctd, est_slctd):
    
    file = files(filenames, '\\T_'+str(bsn_slctd)+str(est_slctd), ",") 
    
    time = "Year"

    fig = boxby_plot(file, option_slctd, year_slctd, time)
 
    return fig

@app.callback(
    Output(component_id = 'variable_H_box_month', component_property = 'figure'),
    [Input(component_id = 'slct_H_var', component_property = 'value'),
      Input(component_id = 'range_slider', component_property = 'value'),
      Input(component_id = 'slct_bsn', component_property = 'value'),
      Input(component_id = 'slct_est', component_property = 'value')]
)

def H_box(option_slctd, year_slctd, bsn_slctd, est_slctd):
    
    file = files(filenames, '\\T_'+str(bsn_slctd)+str(est_slctd), ",") 
    
    time = "Month"

    fig = boxby_plot(file, option_slctd, year_slctd, time)
 
    return fig

@app.callback(
    Output(component_id = 'variable_H_box_hour', component_property = 'figure'),
    [Input(component_id = 'slct_H_var', component_property = 'value'),
      Input(component_id = 'range_slider', component_property = 'value'),
      Input(component_id = 'slct_bsn', component_property = 'value'),
      Input(component_id = 'slct_est', component_property = 'value')]
)

def H_box(option_slctd, year_slctd, bsn_slctd, est_slctd):
    
    file = files(filenames, '\\T_'+str(bsn_slctd)+str(est_slctd), ",") 
    
    time = "Hour"

    fig = boxby_plot(file, option_slctd, year_slctd, time)
 
    return fig

@app.callback(
    Output(component_id = 'report_Hc_graph', component_property = 'figure'),
    [Input(component_id = 'range_slider', component_property = 'value'),
      Input(component_id = 'slct_bsn', component_property = 'value'),
      Input(component_id = 'slct_est', component_property = 'value')]
)

def update_report_H_graph(year_slctd, bsn_slctd, est_slctd):
    
    file = files(report_files_H_cuenca_35, str(bsn_slctd)+str(est_slctd), " ") 

    file_rep_P = files(report_files_H_cuenca_P, str(bsn_slctd)+str(est_slctd), " ") 
    
    file['DATE'] = file['row.names'] + " " + file['redond']
    
    fig = line_plot(file, "DATOS", year_slctd)
    
    fig.add_scatter(x=file["DATE"], y=file["LSUP_C3.5"], name='+3.5smes')
    fig.add_scatter(x=file["DATE"], y=file["LINF_C3.5"], name='-3.5smes')

    fig.add_scatter(x=file["DATE"], y=file_rep_P["P9999_mes_C69"], name='P9999')
    fig.add_scatter(x=file["DATE"], y=file_rep_P["P0001_mes_C69"], name='P0001')
    
    return fig

@app.callback(
    Output(component_id = 'report_He_graph', component_property = 'figure'),
    [Input(component_id = 'range_slider', component_property = 'value'),
      Input(component_id = 'slct_bsn', component_property = 'value'),
      Input(component_id = 'slct_est', component_property = 'value')]
)

def update_report_H_graph(year_slctd, bsn_slctd, est_slctd):
    
    file = files(report_files_H_est_35, str(bsn_slctd)+str(est_slctd), " ") 

    file_rep_P = files(report_files_H_est_P, str(bsn_slctd)+str(est_slctd), " ") 
    
    file['DATE'] = file['row.names'] + " " + file['redond']
    
    fig = line_plot(file, "DATOS", year_slctd)
    
    fig.add_scatter(x=file["DATE"], y=file["LSUP_E3.5"], name='+3.5smes')
    fig.add_scatter(x=file["DATE"], y=file["LINF_E3.5"], name='-3.5smes')

    fig.add_scatter(x=file["DATE"], y=file_rep_P["P9999_mes_E69"], name='P9999')
    fig.add_scatter(x=file["DATE"], y=file_rep_P["P0001_mes_E69"], name='P0001')
    
    return fig

@app.callback(
    Output(component_id = 'report_diff_graph', component_property = 'figure'),
    [Input(component_id = 'range_slider', component_property = 'value'),
      Input(component_id = 'slct_bsn', component_property = 'value'),
      Input(component_id = 'slct_est', component_property = 'value')]
)

def update_report_diff_graph(year_slctd, bsn_slctd, est_slctd):
    
    file = files(report_files_H_dif, str(bsn_slctd)+str(est_slctd), " ") 

    file['DATE'] = file['row.names'] + " " + file['redond']
    
    fig = line_plot(file, "diff_DATOS", year_slctd)
    
    fig.add_scatter(x=file["DATE"], y=file["P01_mes_DIF69"], name='+6smes')
    fig.add_scatter(x=file["DATE"], y=file["P99_mes_DIF69"], name='-6smes')
   
    return fig

############# DIARIOS #############    

@app.callback(
    Output(component_id = 'variable_DG_box', component_property = 'figure'),
    [Input(component_id = 'slct_D_var', component_property = 'value'),
     Input(component_id = 'slct_bsn', component_property = 'value'),
     Input(component_id = 'slct_est', component_property = 'value')]
)

def HG_box(option_slctd, bsn_slctd, est_slctd):
    
    file = files(filenames, '\\D_T_'+str(bsn_slctd)+str(est_slctd), ",")

    year_slctd = None

    resolution = "Diarios"

    fig = box_plot(file, option_slctd, year_slctd, resolution)

    return fig

@app.callback(
    Output(component_id = 'variable_D_Hist', component_property = 'figure'),
    [Input(component_id = 'slct_D_var', component_property = 'value'),
     Input(component_id = 'slct_bsn', component_property = 'value'),
     Input(component_id = 'slct_est', component_property = 'value')]
)

def H_hist(option_slctd, bsn_slctd, est_slctd):
    
    file = files(filenames, '\\D_T_'+str(bsn_slctd)+str(est_slctd), ",") 
 
    year_slctd = None

    resolution = "Diarios"

    fig = hist_plot(file, option_slctd, year_slctd, resolution)
    
    return fig

@app.callback(
    [Output(component_id = 'output_D_container', component_property = 'children'),
      Output(component_id = 'variable_D_graph', component_property = 'figure')],
    [Input(component_id = 'slct_D_var', component_property = 'value'),
     Input(component_id = 'range_slider', component_property = 'value'),
     Input(component_id = 'slct_bsn', component_property = 'value'),
     Input(component_id = 'slct_est', component_property = 'value')]
)

def update_D_graph(option_slctd, year_slctd, bsn_slctd, est_slctd):
 
    container = "{}".format(option_slctd)
    
    file = files(filenames, '\\D_T_'+str(bsn_slctd)+str(est_slctd), ",") 
    
    resolution = "Diarios"

    fig = line_plot(file, option_slctd, year_slctd, resolution)
    
    return container, fig

@app.callback(
    Output(component_id = 'variable_D_box_year', component_property = 'figure'),
    [Input(component_id = 'slct_D_var', component_property = 'value'),
     Input(component_id = 'range_slider', component_property = 'value'),
     Input(component_id = 'slct_bsn', component_property = 'value'),
     Input(component_id = 'slct_est', component_property = 'value')]
)

def D_box(option_slctd, year_slctd, bsn_slctd, est_slctd):
    
    file = files(filenames, '\\D_T_'+str(bsn_slctd)+str(est_slctd), ",") 
    
    resolution = "Diarios"

    time = "Year"

    fig = boxby_plot(file, option_slctd, year_slctd, time, resolution)

    return fig

@app.callback(
    Output(component_id = 'variable_D_box_month', component_property = 'figure'),
    [Input(component_id = 'slct_D_var', component_property = 'value'),
     Input(component_id = 'range_slider', component_property = 'value'),
     Input(component_id = 'slct_bsn', component_property = 'value'),
     Input(component_id = 'slct_est', component_property = 'value')]
)

def D_box(option_slctd, year_slctd, bsn_slctd, est_slctd):
    
    file = files(filenames, '\\D_T_'+str(bsn_slctd)+str(est_slctd), ",") 
    
    resolution = "Diarios"

    time = "Month"

    fig = boxby_plot(file, option_slctd, year_slctd, time, resolution)
    
    return fig

@app.callback(
    Output(component_id = 'report_D_graph', component_property = 'figure'),
    [Input(component_id = 'slct_D_var', component_property = 'value'),
     Input(component_id = 'range_slider', component_property = 'value'),
     Input(component_id = 'slct_bsn', component_property = 'value'),
     Input(component_id = 'slct_est', component_property = 'value')]
)

def update_report_D_graph(option_slctd, year_slctd, bsn_slctd, est_slctd):
    
    file = files(report_files_D_cuenca, str(bsn_slctd)+str(est_slctd), " ") 

    file_rep_D_est_mn = files(report_files_D_est_MN, str(bsn_slctd)+str(est_slctd), " ") 

    file_rep_D_est_mx = files(report_files_D_est_MX, str(bsn_slctd)+str(est_slctd), " ") 

    file['FECHA'] = pd.to_datetime(file['FECHA'])
    
    resolution = "Diarios"
    
    fig = line_plot(file, option_slctd, year_slctd, resolution)

    if option_slctd == "TEMP_MX":
        fig.add_scatter(x=file["FECHA"], y=file["LSUP_C3.5_MX"], name='LSUP_C3.5_MX')
        fig.add_scatter(x=file["FECHA"], y=file["LINF_C3.5_MX"], name='LINF_C3.5_MX')

        fig.add_scatter(x=file["FECHA"], y=file_rep_D_est_mx["LSUP_E3.5_MX"], name='LSUP_E3.5_MX')
        fig.add_scatter(x=file["FECHA"], y=file_rep_D_est_mx["LINF_E3.5_MX"], name='LINF_E3.5_MX')
    
    else:
        fig.add_scatter(x=file["FECHA"], y=file["LSUP_C3.5_MN"], name='LSUP_C3.5_MN')
        fig.add_scatter(x=file["FECHA"], y=file["LINF_C3.5_MN"], name='LINF_C3.5_MN')
    
        fig.add_scatter(x=file["FECHA"], y=file_rep_D_est_mn["LSUP_E3.5_MN"], name='LSUP_E3.5_MN')
        fig.add_scatter(x=file["FECHA"], y=file_rep_D_est_mn["LINF_E3.5_MN"], name='LINF_E3.5_MN')
    

    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)    