'''
Main Flet app entry point.
'''
import plotly.express as px

import flet as ft
from flet.plotly_chart import PlotlyChart

def main(page: ft.Page):
    '''
    Main page display
    '''
    d_f = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(d_f, x="year", y="lifeExp", color="country")

    page.add(PlotlyChart(fig, expand=True))

ft.app(target=main)
