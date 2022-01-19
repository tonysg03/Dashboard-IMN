# -*- coding: utf-8 -*-
"""
Created on Wed 30 Nov 09:10:45 2021

@author: Anthony Segura García

e-mail: asegura@imn.ac.cr

Instituto Meteorológico Nacional
Departamento de Red Meteorológica y Procesamiento de Datos
"""
import pandas as pd
import numpy as np
import plotly.express as px

def copy_file(file, option_slctd, year_slctd = None, resolution = None):
   
    if resolution == "Diarios":
        file['FECHA'] = pd.to_datetime(file['FECHA'])
    else:
        file['DATE'] = pd.to_datetime(file['DATE'])
    
    c_file = file.copy()

    if year_slctd != None:
        if resolution == "Diarios":
            c_file = c_file[(c_file.FECHA.dt.year >= year_slctd[0]) & (c_file.FECHA.dt.year <= year_slctd[1])]
        else:
            c_file = c_file[(c_file.DATE.dt.year >= year_slctd[0]) & (c_file.DATE.dt.year <= year_slctd[1])]

    c_file["{}".format(option_slctd)] = c_file["{}".format(option_slctd)].replace(-9.0, np.nan)

    return c_file

def box_plot(file, option_slctd, year_slctd = None, resolution = None):

    c_file = copy_file(file, option_slctd, year_slctd, resolution)
    
    fig = px.box(
        c_file,
        y = "{}".format(option_slctd)
    ) 
    
    return fig

def hist_plot(file, option_slctd, year_slctd = None, resolution = None):

    c_file = copy_file(file, option_slctd, year_slctd, resolution)
    
    fig = px.histogram(
        c_file,
        x = "{}".format(option_slctd)
    ) 

    return fig

def line_plot(file, option_slctd, year_slctd, resolution = None):

    c_file = copy_file(file, option_slctd, year_slctd, resolution)

    if resolution == "Diarios":
        x = 'FECHA'
    else:
        x = 'DATE'

    fig = px.line(
        data_frame = c_file,
        x = x,
        y = "{}".format(option_slctd) 
    )

    return fig

def boxby_slctd(file, option_slctd, time, delim, resolution = None):

    if resolution == "Diarios":
        file[time] = file["FECHA"].dt.strftime(delim)
    else:
        file[time] = file["DATE"].dt.strftime(delim)

    fig = px.box(
        file,
        x = "{}".format(time),
        y = "{}".format(option_slctd),
        color = "{}".format(time)
    )

    return fig

def boxby_plot(file, option_slctd, year_slctd, time, resolution = None):
    
    c_file = copy_file(file, option_slctd, year_slctd, resolution)

    if time == 'Hour':
        c_file = boxby_slctd(c_file, option_slctd, time, '%H', resolution)
    elif time == 'Month':
        c_file = boxby_slctd(c_file, option_slctd, time, '%b', resolution)
    elif time == 'Year':
        c_file = boxby_slctd(c_file, option_slctd, time, '%Y', resolution)

    return c_file