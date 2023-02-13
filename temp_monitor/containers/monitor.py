'''
Module for rendering the monitor page details
'''
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import flet as ft

class MonitorContainer(ft.Container):
    '''
    Main monitoring tab view container
    '''
    def __init__(
        self,
        app,
        page: ft.Page,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.graph = TemperatureGraph(expand=True)
        self.content = ft.Row([self.graph])

class TemperatureGraph(PlotlyChart):
    '''
    Main temperature graph object
    '''
    def __init__(
        self,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.data = px.data.gapminder().query("continent=='Oceania'")
        self.figure = px.line(self.data, x="year", y="lifeExp", color="country")
