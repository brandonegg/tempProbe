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
            mouse_cursor=ft.MouseCursor.GRAB,
            on_pan_update=self._pan_update,
            on_scroll=self._scroll_update,
            drag_interval=25,
            content=self.graph,
        )

        self.content = ft.Row([graph_gesture_wrapper])

    def _scroll_update(self, event):
        scale_factor = 0.001
        factor = 1 + (scale_factor * event.scroll_delta_y)

        self.graph.zoom_uniform(factor)
        self.page.update()

    def _pan_update(self, event):
        scale_factor = 0.005

        self.graph.shift_axis(scale_factor*event.delta_x, scale_factor*event.delta_y)
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
        self.x_range = [300, 0]
        self.y_range = [300, 0]
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

    def _update_axis(self):
        '''
        Sync x and y-axis values to figure.
        '''
        self.figure.update_xaxes(autorange=False, range=self.x_range)
        self.figure.update_yaxes(autorange=False, range=self.y_range)

    def shift_axis(self, amount_x, amount_y):
        '''
        Adjust x/y axis
        '''
        x_adjustment = abs(self.x_range[0] - self.x_range[1])*(amount_x/2)
        y_adjustment = abs(self.y_range[0] - self.y_range[1])*(amount_y/2)

        self.x_range = [self.x_range[0] + x_adjustment, self.x_range[1] + x_adjustment]
        self.y_range = [self.y_range[0] + y_adjustment, self.y_range[1] + y_adjustment]
        self._update_axis()

    def zoom_uniform(self, factor):
        '''
        Zoom x-axis
        '''
        x_adjustment = abs(self.x_range[0] - self.x_range[1]) * (1-factor)
        y_adjustment = abs(self.y_range[0] - self.y_range[1]) * (1-factor)

        self.x_range = [self.x_range[0] - x_adjustment, self.x_range[1] + x_adjustment]
        self.y_range = [self.y_range[0] + y_adjustment, self.y_range[1] - y_adjustment]
        self._update_axis()
