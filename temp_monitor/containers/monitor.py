'''
Module for rendering the monitor page details
'''
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import flet as ft

def page():
    '''
    Page for monitoring data.
    '''
    def test(_event):
        print("hello")

    d_f = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(d_f, x="year", y="lifeExp", color="country")
    graph = PlotlyChart(fig, expand=True)

    new_task = ft.TextField(hint_text="test", width=300)
    input_row = ft.Row([new_task, ft.ElevatedButton("test", on_click=test)])
    return ft.Container(content=ft.Column([graph, input_row]), alignment=ft.alignment.center)
