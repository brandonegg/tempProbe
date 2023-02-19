'''
Module for rendering the monitor page details
'''
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import flet as ft
import requests
import pandas as pd

TEMPERATURE_HISTORY_URL = "http://tempbox.local/history"

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

        self._update_history()

        self.display_in = 'F'
        self.figure = px.line(self.data, x="Time - Seconds", y=f"Temperature({self.display_in})")
        self.figure['layout']['xaxis']['autorange'] = "reversed"
        # attach the call back
        #self.figure.canvas.mpl_connect('scroll_event', lambda event: self.zoom_fun(event))

    def _update_history(self):
        '''
        Make a request to temperature box's history endpoint.
        '''
        response = requests.get(TEMPERATURE_HISTORY_URL)
        if response.status_code == 200:
            self.temp_history = response.json()
            if self.data is None:
                self.data = pd.DataFrame(columns=["Time - Seconds", "Temperature(F)", "Temperature(C)"])
                self.data.loc[:, "Time - Seconds"] = list(range(299, -1, -1))
  
            self.data.loc[:, "Temperature(F)"] = self.temp_history["f"]
            self.data.loc[:, "Temperature(C)"] = self.temp_history["c"]
