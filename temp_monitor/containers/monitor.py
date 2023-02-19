'''
Module for rendering the monitor page details
'''
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import flet as ft
import requests
import pandas as pd
import matplotlib as plt

TEMPERATURE_HISTORY_URL = "http://tempbox.local/history"

callback = """
    var update_y_range = function(event) {
        var y_axis = fig.layout.yaxis;
        var delta = -event.deltaY;
        var factor = 1.1;
        var new_range = y_axis.range.map(function(r) {
            var center = (r[1] + r[0]) / 2;
            var width = r[1] - r[0];
            var new_width = width * (factor ** (delta / 100));
            var new_start = center - new_width / 2;
            var new_end = center + new_width / 2;
            return [new_start, new_end];
        });
        y_axis.range = new_range;
        Plotly.update('graph', fig.data, fig.layout);
    };
    document.getElementById('graph').addEventListener('wheel', update_y_range);
"""
base_scale = 2.

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
        if (response.status_code == 200):
            self.temp_history = response.json()
            if (self.data is None):
                self.data = pd.DataFrame(columns=["Time - Seconds", "Temperature(F)", "Temperature(C)"])
                self.data.loc[:, "Time - Seconds"] = list(range(299, -1, -1))
            
            self.data.loc[:, "Temperature(F)"] = self.temp_history["f"]
            self.data.loc[:, "Temperature(C)"] = self.temp_history["c"]

    def zoom_fun(self, event):
        # get the current x and y limits
        cur_xlim = self.figure.axes[0].get_xlim()
        cur_ylim = self.figure.axes[0].get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print(event.button)
        # set new limits
        self.figure.axes[0].set_xlim([xdata - cur_xrange*scale_factor,
                     xdata + cur_xrange*scale_factor])
        self.figure.axes[0].set_ylim([ydata - cur_yrange*scale_factor,
                     ydata + cur_yrange*scale_factor])
        plt.draw() # force re-draw