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
    def test(e):
        print("hello")

    page.title('Temperature Monitor')

    d_f = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(d_f, x="year", y="lifeExp", color="country")

    page.add(PlotlyChart(fig, expand=True))

    new_task = ft.TextField(hint_text="test", width=300)
    page.add(ft.Row([new_task, ft.ElevatedButton("test", on_click=test)]))

ft.app(target=main)
