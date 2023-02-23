'''
Module for rendering the monitor page details
'''
import asyncio
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import flet as ft
from temp_monitor.data import TemperatureState
from temp_monitor.globals import BASE_URL
import aiohttp

TEMPERATURE_HISTORY_URL = f"{BASE_URL}/history"
DISPLAY_URL = f"{BASE_URL}/display"

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
        self.graph_container = None
        self.no_data_screen = None
        self.no_sensor_screen = None

        self.current_view = None # error | graph
        self.graph_gesture_wrapper = None

        asyncio.create_task(self._data_update_listener())

    async def render_views(self):
        '''
        Main view render logic for monitoring page
        '''
        prev_view = self.current_view
    
        if not self.state.server_connected:
            if self.no_data_screen is None:
                self.no_data_screen = ft.Container(
                    ft.Column([
                        ft.Text("Attempting to connect to temperature sensor...", size=14),
                        ft.Container(ft.ProgressBar(width=200), alignment=ft.alignment.center, width=400)
                    ]),
                    alignment=ft.alignment.center,
                    width=400
                )

            self.content = self.no_data_screen
            self.current_view = "error"
        elif not self.state.sensor_connected:
            if self.no_sensor_screen is None:
                self.no_sensor_screen = ft.Text("Temperature Sensor not Connected!", color="red", size=30)

            self.content = self.no_sensor_screen
            self.current_view = "error"
        else:
            if self.graph is None or self.graph_gesture_wrapper is None or self.graph_container is None:
                self.graph = TemperatureGraph(self.state, expand=True)

                self.graph_gesture_wrapper = ft.Container(
                        ft.GestureDetector(
                        mouse_cursor=ft.MouseCursor.GRAB,
                        on_pan_update=self._pan_update,
                        on_scroll=self._scroll_update,
                        drag_interval=25,
                        content=self.graph,
                    ),
                    alignment=ft.alignment.center
                )

                self.enable_display_alert_message = ft.Text("", color="")
                self.enable_display_toggle = ft.Switch(label="Enable Display", value=False, on_change=self._enable_display_changed)
                self.graph_container = ft.Container(
                    ft.Column([
                        ft.Row([self.enable_display_toggle, self.enable_display_alert_message]),
                        self.graph_gesture_wrapper
                    ]),
                    alignment=ft.alignment.center,
                    padding=20
                )

            self.current_view = "graph"
            self.content = self.graph_container

        await self.update_async()

    async def _enable_display_changed(self, event):
        val = event.data
        request = {
            "set_display": val == "true"
        }

        self.enable_display_toggle.disabled = True
        await self.enable_display_alert_message.update_async()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(DISPLAY_URL, json=request) as resp:
                    data = await resp.json()
                    if not 'success' in data:
                        raise Exception("request unsuccessful")
                    
                    self.enable_display_alert_message.value = ""
        except:
            self.enable_display_alert_message.color = "red"
            self.enable_display_alert_message.value = "Server unreachable. Try again"
            self.enable_display_toggle.value = not val

        self.enable_display_toggle.disabled = False
        await self.enable_display_toggle.update_async()
        await self.enable_display_alert_message.update_async()

    async def _data_update_listener(self):
        await self.render_views()
        while True:
            await self.state.data_update_event.wait()
            if not self.graph is None:
                self.graph.flag_data_for_update()
            await self.render_views()
            self.state.data_update_event.clear()
            #await self.update_async()

    async def _scroll_update(self, event):
        if self.graph is None:
            return

        scale_factor = 0.001
        factor = 1 + (scale_factor * event.scroll_delta_y)

        self.graph.zoom_uniform(factor)
        await self.graph.update_async()

    async def _pan_update(self, event):
        if self.graph is None:
            return

        scale_factor = 0.005

        self.graph.shift_axis(scale_factor*event.delta_x, scale_factor*event.delta_y)
        await self.graph.update_async()

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
        self.max_x_range = [300, 0]
        self.y_range = None
        self.axis_ratio = 0.25 # (y_axis max-min) / (x_axis max - min) ex: 0.5 means y_axis spans half the # of degrees and x_axis time units.
        self.data_needs_update = True

        self.state = state
        self.height = 600

        self.figure = px.line(self.state.data, x="Time - Seconds", y=f"Temperature({self.state.data_unit.upper()})")
        self.figure['layout']['xaxis']['autorange'] = "reversed"

        self._sync_x_range()

    def _before_build_command(self):
        # TODO: Maybe a more efficient way of doing this?
        if self.data_needs_update:
            self.figure = px.line(self.state.data, x="Time - Seconds", y=f"Temperature({self.state.data_unit.upper()})")
            self.figure['layout']['xaxis']['autorange'] = "reversed"
            self.data_needs_update = False

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
        #self.y_range = [self.state.data[data_col].min(), self.state.data[data_col].max()]
        self.y_range = [0, int(abs(self.x_range[0]-self.x_range[1])*self.axis_ratio)]
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

        if self.x_range[0] + x_adjustment >= self.max_x_range[0]:
            x_adjustment = self.max_x_range[0] - self.x_range[0]
        if self.x_range[1] + x_adjustment <= self.max_x_range[1]:
            x_adjustment = self.max_x_range[1] - self.x_range[1]

        self.x_range = [self.x_range[0] + x_adjustment, self.x_range[1] + x_adjustment]
        self.y_range = [self.y_range[0] + y_adjustment, self.y_range[1] + y_adjustment]
        self._update_axis()

    def flag_data_for_update(self):
        '''
        Makes it so new line graph is only generated when needed. Flag this when dataframe updates.
        '''
        self.data_needs_update = True

    def zoom_uniform(self, factor):
        '''
        Zoom x-axis
        '''
        x_range = abs(self.x_range[0] - self.x_range[1])
        scaled_x_range = x_range * factor
        x_adjustment = (scaled_x_range - x_range) / 2


        new_x_0 = self.x_range[0] - x_adjustment
        new_x_1 = self.x_range[1] + x_adjustment

        if (new_x_0 >= self.max_x_range[0]):
            new_x_1 = new_x_1 - (new_x_0 - self.x_range[0])
            new_x_0 = self.max_x_range[0]

        if (new_x_1 <= self.max_x_range[1]):
            new_x_1 = self.max_x_range[1]

        actual_scaled_x_range = abs(new_x_0 - new_x_1)

        y_range = abs(self.y_range[1] - self.y_range[0])
        scaled_y_range = actual_scaled_x_range*self.axis_ratio
        y_adjustment = ((scaled_y_range - y_range) * self.axis_ratio) / 2

        self.x_range = [new_x_0, new_x_1]
        self.y_range = [self.y_range[0] - y_adjustment, self.y_range[1] + y_adjustment]

        self._update_axis()
