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

        graph_gesture_wrapper = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            on_scale_update=lambda event: self._scale_update(event),
            content=self.graph,
        )

        self.content = ft.Row([graph_gesture_wrapper])

    def _scale_update(self, event):
        scale_factor = 2
        self.graph.shift_axis(scale_factor*event.focal_point_delta_x, scale_factor*event.focal_point_delta_y)
        self.page.update()

class TemperatureGraph(PlotlyChart):
    '''
    Main temperature graph object
    '''
    def __init__(
        self,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.display_in = 'F'
        self._update_history()

        self.figure = px.line(self.data, x="Time - Seconds", y=f"Temperature({self.display_in})")
        self.figure['layout']['xaxis']['autorange'] = "reversed"

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
            self.x_range = [300, 0]
            self.y_range = [self.data[f"Temperature({self.display_in})"].min(), self.data[f"Temperature({self.display_in})"].max()]

    def shift_axis(self, amount_x, amount_y):
        self.x_range = [self.x_range[0] + amount_x/2, self.x_range[1] + amount_x/2]
        self.y_range = [self.y_range[0] + amount_y/2, self.y_range[1] + amount_y/2]
        self.figure.update_xaxes(autorange=False, range=self.x_range)
        self.figure.update_yaxes(autorange=False, range=self.y_range)

    def zoom_x(self, amount):
        self.x_range = [self.x_range[0] - amount/2, self.x_range[1] + amount/2]
        self.figure.update_xaxes(autorange=False, range=self.x_range)
