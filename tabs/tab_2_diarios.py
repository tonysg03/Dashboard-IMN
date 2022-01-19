# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 15:38:10 2021

@author: Anthony Segura García

e-mail: asegura@imn.ac.cr

Instituto Meteorológico Nacional
Departamento de Red Meteorológica y Procesamiento de Datos
"""

#Se cargan las librerías
from dash import dcc
from dash import html

import dash_bootstrap_components as dbc

#Hacer un diccionario con los nombres y las variables para que se vea mejor y se reduzca
#el código

# fig_names = ['Temperatura', 'Lluvia', 'Humedad Relativa', 'Radiación Total', 
#              'Dirección del Viento', 'Velocidad escalar del Viento', 
#              'Velocidad vectorial del Viento', 'Presión']

mark_values = {1994: '1994', 1997: '1997', 2000: '2000', 2003: '2003',
               2006: '2006', 2009: '2009', 2012: '2012', 2015: '2015',
               2018: '2018', 2021: '2021'}

tab_2_layout = html.Div([

    html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Variable Meteorológica"),
                    dbc.CardBody([
                        dcc.RadioItems(id = "slct_D_var",
                                        options = [{"label": "Temperatura Máxima", "value": 'TEMP_MX'},
                                                    {"label": "Temperatura Mínima", "value": 'TEMP_MN'}],
                                        value = 'TEMP_MX'
                        )
                    ]),
                    dbc.CardFooter(
                        dbc.Row([
                            dbc.Col(
                                html.Div("Variable seleccionada:"),
                                width={"size": "auto"},
                            ),
                            dbc.Col(
                                html.Div(id = 'output_D_container',
                                    style = {"color": "green"}),
                                width={"size": "auto"},
                            ),
                        ]),
                    )], 
                    color = "light"),
                width={"size": "3"}
                ),
                dbc.Col(
                        dcc.RangeSlider(
                            id = "range_slider",
                            marks = mark_values,
                            step = 1,
                            min = 1994,
                            max = 2021,
                            value = [1994,2021]
                        ),
                        align = "center"
                )
            ])
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H4("Boxplot histórico", className = "card-title"),
                dcc.Graph(id = "variable_DG_box")
            ], 
            color = "dark", inverse=True),
            className = "mb-3"
        ),
        dbc.Col(
            dbc.Card([
                html.H4("Histograma histórico", className = "card-title"),
                dcc.Graph(id = "variable_D_Hist")
            ], 
            color = "dark", inverse=True)
        )
       
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H4("Temperatura diaria", className = "card-title"),
                dcc.Graph(id = "variable_D_graph")
            ], 
            color = "info", outline = True),
            className = "mb-3"
        )       
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H4("Boxplot con resolución mensual", className = "card-title"),
                dcc.Graph(id = "variable_D_box_year")
            ], 
            color = "success", inverse=True),
            className = "mb-3"
        ),
        dbc.Col(
            dbc.Card([
                html.H4("Boxplot con resolución mensual", className = "card-title"),
                dcc.Graph(id = "variable_D_box_month")
            ], 
            color = "danger", inverse=True),
            className = "mb-3"
        )
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H4("Reporte de estadísticos", className = "card-title"),
                dcc.Graph(id = "report_D_graph")
            ],
            color = "info", inverse=True),
        )
    ])    
])