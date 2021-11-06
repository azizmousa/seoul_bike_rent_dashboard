#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 04:35:05 2021

@author: amr
"""



import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import dash_daq as daq
import plotly.express as px
from dash.dependencies import Input,Output,State
import datetime as dt

# Load data
df = pd.read_csv('data/bikes.csv', parse_dates=True)


def add_day_month_year(df):
    df['Date'] = pd.to_datetime(df['Date'], 
     format = '%d/%m/%Y', 
     errors = 'coerce')
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['weekday'] = df['Date'].dt.dayofweek
    df['weekday_name'] = df['Date'].apply(lambda x: dt.datetime.strftime(x, '%A'))

    return df

def draw_scatter(input_default):
    temperature_rental = df1.groupby(input_default,as_index=False)['Hour'].mean()
    sc = px.scatter(temperature_rental, x="Hour", y=input_default, color="Hour",title='Each feature changes per hour',template='plotly_dark' ,size_max=60)
    return sc


def draw_hist(input_default):
    seasons_df=df2.groupby(input_default,as_index=False)['Rented Bike Count'].sum()
    # print(seasons_df.head())
    hist = px.histogram(seasons_df,x=input_default,y='Rented Bike Count', 
                        color=input_default, barmode='group',
                        title='Number of bikes rented ',template='plotly_dark' )
    hist.update_layout(yaxis_title_text='Sum Of Rent Count')
    return hist


def seasons_pie_fig(data):
    seasons_df=data.groupby('Seasons',as_index=False)['Rented Bike Count'].sum()
    # print(seasons_df.head())
    fig = px.pie(seasons_df, values='Rented Bike Count', names='Seasons', 
                  template='plotly_dark',
                  title='')
    return fig

def day_trend_fig(data):
    trend_df=data.groupby(['weekday_name', 'Hour'],as_index=False)['Rented Bike Count'].mean()
    # print(seasons_df.head())
    fig = px.line(trend_df, x="Hour", y='Rented Bike Count', 
                  color="weekday_name",
                  title='',
                  template='plotly_dark' ,markers=True)
    fig.update_layout(yaxis_title_text='Sum Of Rent Count')
    return fig

def rent_per_day_fig(data):
    dd = data.groupby('Date',as_index=False)['Rented Bike Count'].sum()
    fig = px.line(dd, x="Date", y='Rented Bike Count', 
                  title='',
                  template='plotly_dark')
    fig.update_layout(yaxis_title_text='Sum Of Rent Count')
    return fig



df1=add_day_month_year(df)
df2=add_day_month_year(df)

sc=draw_scatter('Rented Bike Count')
hist=draw_hist('Day')

# Initialize the app
app = dash.Dash(__name__)


def build_top_banner():
    return html.Div(
    id="banner",
    className="banner",
    children=[
        html.Div(
            id="banner-text",
            children=[
                html.H5("Seoul Bike Rent Dashboard", style={ 
                                               'fontSize':50,
                                               'textAlign':'center'}),
                html.H6("Report For Seoul Bike Rental Process", style={ 
                                               'fontSize':50,
                                               'textAlign':'center'}),
            ],
        ),
    ],
)

def generate_section_banner(title):
    return html.Div(className="section-banner", children=title, style={ 
                                               'fontSize':25,
                                               'color': '#eb5e34',
                                               'textAlign':'center'})


def build_top_panel():
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            # Metrics summary
            html.Div(
                id="change_per_hour",
                className="six columns",
                children=[
                    generate_section_banner("Change per hour"),
                    html.Div(
                        id="metric-div",
                        children=[
                            # generate_metric_list_header(),
                            build_scatter_plot(),
                        ],
                    ),
                ],
            ),
            # BAR_CHAR
            html.Div(
                id="rented_summary",
                className="six columns",
                children=[
                    generate_section_banner("Rented Bikes Summary"),
                    html.Div(
                        id="metric-div2",
                        children=[
                            # generate_metric_list_header(),
                            build_bar_plot()
                        ],
                    ),
                ],
            ),
        ],
    )



def build_middle_panel():
    return html.Div(
        id="middle-section-container",
        # className="row",
        children=[
            # seasons_pie
            html.Div(
                id="seasons_pie_dev",
                className="six columns",
                children=[
                    generate_section_banner("Seasonality"),
                    build_pie_plot(seasons_pie_fig(df2)),
                ],
            ),
            # BAR_CHAR
            html.Div(
                id="aaa",
                className="six columns",
                children=[
                    generate_section_banner("Rented Bikes Summary"),
                    html.Div(
                        id="mbbb",
                        children=[
                            # generate_metric_list_header(),
                            build_line_trend_plot(df2)
                        ],
                    ),
                ],
            ),
        ],
    )


def build_buttom_panel():
  return html.Div(
        id="buttom-section-container",
        # className="row",
        children=[
            # seasons_pie
            html.Div(
                id="buttom_panel_dev",
                className="twilve columns",
                children=[
                    generate_section_banner("Bike Rental Trend"),
                    build_rent_per_day_trend(df2)
                ],
            )
        ],
    )

def build_scatter_plot():
    return html.Div(
            children=[
                 html.Label('Choose feature to draw'),
                 dcc.Dropdown(id='features',
                     options=[
                         {'label': 'solar radiation', 'value': 'Solar Radiation (MJ/m2)'},
                         {'label':'Humidity', 'value': 'Humidity(%)'},
                         {'label': 'windSpeed', 'value': 'Wind speed (m/s)'},
                         {'label': 'Temperature', 'value': 'Temperature(C)'},
                         {'label': 'Rainfall', 'value': 'Rainfall(mm)'},
                         {'label': 'Visibility (10m)', 'value': 'Visibility (10m)'},
                         {'label': 'Number of bikes', 'value': 'Rented Bike Count'}
        
                         ],
                     value='Rented Bike Count'),
                 dcc.Graph(
                     id='Scatter',
                     figure=sc
                     )
                 ]
            )



def build_pie_plot(data):
   return html.Div(
            children=[
                    dcc.Graph(
                          id="piechart",
                          figure=seasons_pie_fig(df2)
                      )
                 ]
            )    

def build_line_trend_plot(data):
   return html.Div(
            children=[
                    dcc.Graph(
                          id="trendhart",
                          figure=day_trend_fig(df2)
                      )
                 ]
            )   


def build_rent_per_day_trend(data):
    return html.Div(
            children=[
                    dcc.Graph(
                          id="rentLine",
                          figure=rent_per_day_fig(df2)
                      )
                 ]
            )   

def build_bar_plot():
    return html.Div(
            children=[
                 html.Label('Choose Time Slot to draw'),
                 dcc.Dropdown(id='feature_selections',
                                options=[
                                    {'label': 'Seasons', 'value': 'Seasons'},
                                    {'label': 'Hour', 'value': 'Hour'},
                                    {'label': 'Day', 'value': 'Day'},
                                    {'label': 'Week', 'value': 'weekday'},
                                    {'label': 'Month', 'value': 'Month'}
            
                                ],
                                value='Seasons'
                            ),
                              dcc.Graph(
                                  id='histogram',
                                  figure=hist,
                                  
                                  )
                 ]
            )    


       
app.layout = html.Div(
    children=[
        build_top_banner(),
        html.Div(
            id="status-container",
            children=[
                html.Div(
                    id="graphs-container",
                    children=[html.Div(children=[build_top_panel()]), 
                              html.Div(children=[build_middle_panel()]), build_buttom_panel()],
                ),
            ],
        ),
        ]

)

@app.callback(
Output('Scatter','figure'),
[Input('features','value')],
)

def update_scatter(input_1):
    print(input_1)
    sc=draw_scatter(input_1)
    return sc

@app.callback(
Output('histogram','figure'),
[Input('feature_selections','value')],
)

def update_hist(input_2):
    hist=draw_hist(input_2)
    return hist


if __name__ == '__main__':
    app.run_server(debug=True)
