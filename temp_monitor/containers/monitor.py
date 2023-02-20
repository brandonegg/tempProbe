'''
Module for rendering the monitor page details
'''
import asyncio
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import flet as ft
from temp_monitor.data import TemperatureState

TEMPERATURE_HISTORY_URL = "http://tempbox.local/history"

class MonitorContainer(ft.Container):
    '''
    Main monitoring tab view container
    '''
    def __init__(
        self,
        page: ft.Page,
        state: TemperatureState,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.page = page
        self.state = state
        self.graph = None
        self.graph_row = None

        self.no_data_screen = None
        self.current_view = None # error | graph
        self.graph_gesture_wrapper = None

        asyncio.create_task(self._data_update_listener())

    async def render_views(self):
        '''
        Main view render logic for monitoring page
        '''
        prev_view = self.current_view
    
        if (self.state.data.empty):
            if self.no_data_screen is None:
                self.no_data_screen = ft.Text("error, no data")
            self.content = self.no_data_screen
            self.current_view = "error"
        else:
            if self.graph is None or self.graph_gesture_wrapper is None or self.graph_row is None:
                self.graph = TemperatureGraph(self.state, expand=True)

                self.graph_gesture_wrapper = ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.GRAB,
                    on_pan_update=self._pan_update,
                    on_scroll=self._scroll_update,
                    drag_interval=25,
                    content=self.graph,
                )

                self.graph_row = ft.Row([self.graph_gesture_wrapper])

            self.current_view = "graph"
            self.content = self.graph_row

        await self.update_async()

    async def _data_update_listener(self):
        await self.render_views()
        while True:
            await self.state.data_update_event.wait()
            await self.render_views()
            self.state.data_update_event.clear()
            #await self.update_async()

    async def _scroll_update(self, event):
        if self.graph is None:
            return

        scale_factor = 0.001
        factor = 1 + (scale_factor * event.scroll_delta_y)

        self.graph.zoom_uniform(factor)
        await self.update_async()

    async def _pan_update(self, event):
        if self.graph is None:
            return

        scale_factor = 0.005

        self.graph.shift_axis(scale_factor*event.delta_x, scale_factor*event.delta_y)
        await self.update_async()

class TemperatureGraph(PlotlyChart):
    '''
    Main temperature graph object
    '''
    def __init__(
        self,
        state: TemperatureState,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.x_range = None
        self.y_range = None

        self.state = state

        self.figure = px.line(self.state.data, x="Time - Seconds", y=f"Temperature({self.state.data_unit.upper()})")
        self.figure['layout']['xaxis']['autorange'] = "reversed"

        self._sync_x_range()

    def _before_build_command(self):
        # TODO: Maybe a more efficient way of doing this?
        self.figure = px.line(self.state.data, x="Time - Seconds", y=f"Temperature({self.state.data_unit.upper()})")
        self.figure['layout']['xaxis']['autorange'] = "reversed"

        if self.x_range is None or self.y_range is None:
            self._sync_x_range()
        
        self._update_axis()
        super()._before_build_command()

    def _sync_x_range(self):
        '''
        Update x range and y range variables to be in sync with state
        '''
        self.x_range = [len(self.state.data.index), 0]
        data_col = f"Temperature({self.state.data_unit.upper()})"
        self.y_range = [self.state.data[data_col].min(), self.state.data[data_col].max()]
        self._update_axis()

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
