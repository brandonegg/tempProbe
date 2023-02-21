'''
Module for rendering the settings page details
'''
import flet as ft
import requests
import asyncio
import aiohttp
from temp_monitor.data import TemperatureState

ALERT_SETTINGS_URL = "http://tempbox.local/alert"

class SettingsContainer(ft.Container):
    '''
    Settings page view
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
        # Stores phone min/max and phone_number
        self.settings = None
        # Components
        self.unit_switcher_component = None
        self.refresh_data_component = None
        self.alert_settings_component = None
        self.alert_settings_input_component = None
        self.main_column_component = None
        self.min_temp_input = None

        self._settings_update_event = asyncio.Event()
        asyncio.create_task(self._render_update_listener())
        asyncio.create_task(self._retrieve_server_settings())

    async def _retrieve_server_settings(self):
        '''
        Fetches alert settings from temp box server.
        '''
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ALERT_SETTINGS_URL) as resp:
                    self.settings = await resp.json()
                    print("updated settings")
        except:
            self.settings = None

        self._settings_update_event.set()

    async def _render_update_listener(self):
        await self._render()
        while True:
            await self._settings_update_event.wait()
            await self._render()
            self._settings_update_event.clear()

    def _update_unit(self):
        pass

    async def _render(self):
        if self.unit_switcher_component is None:
            self.radio_temp_selector = ft.RadioGroup(content=ft.Row([
                        ft.Radio(value= "c", label="Celsius"),
                        ft.Radio(value= "f", label="Fahrenheit")
                    ]))

            self.unit_switcher_component = ft.Container(
                ft.Column([
                    ft.Text("Display Temperature In:", size=15),
                    self.radio_temp_selector,
                    ft.Container(
                        ft.OutlinedButton(text="update", on_click=self._update_unit),
                        alignment=ft.alignment.center
                    ),
                ]),
                width=300
            )

        self.radio_temp_selector.value = self.state.data_unit

        if self.alert_settings_component is None:
            self.alert_settings_component = ft.Container()


        if self.settings is None:
            # render refresh button
            if self.refresh_data_component is None:
                self.refresh_data_component = ft.Container(
                    ft.Column([
                        ft.Text("Unable to contact server", color='red'),
                        ft.Container(
                            ft.OutlinedButton(text="try again", on_click=self._refresh_alert_settings),
                            alignment=ft.alignment.center,
                        )
                    ]),
                    alignment=ft.alignment.center,
                )

            self.alert_settings_component.content = self.refresh_data_component
        else:
            if self.alert_settings_input_component is None:
                self.phone_input = ft.TextField(label="Phone Number", hint_text='include area code', value=self.settings["phone_number"], text_align=ft.TextAlign.RIGHT, width=300)
                self.min_temp_input = ft.TextField(label=f"Min ({self.settings['unit'].upper()})", value=self.settings["min_temp"], expand=True)
                self.max_temp_input = ft.TextField(label=f"Max ({self.settings['unit'].upper()})", value=self.settings["max_temp"], expand=True)
                self.update_alert_button = ft.OutlinedButton(text="update", on_click=self._update_settings)
                self.alert_bottom_container = ft.Container(alignment=ft.alignment.center)

                self.alert_settings_input_component = ft.Container(
                    ft.Column(
                        [
                            ft.Text("Phone Alert Settings:", size=15),
                            self.phone_input,
                            ft.Text("Temperature Alert Triggers:"),
                            ft.Row(
                                [
                                    self.min_temp_input,
                                    self.max_temp_input
                                ],
                                spacing=20,
                            ),
                            ft.Container(
                                self.update_alert_button,
                                alignment=ft.alignment.center,
                            ),
                            self.alert_bottom_container,
                        ],
                    ),
                )
            else:
                self.phone_input.value = self.settings["phone_number"]
                self.min_temp_input.label = f"Min({self.state.data_unit.upper()})"
                self.min_temp_input.value = self.settings["min_temp"]
                
                self.max_temp_input.label = f"Max({self.state.data_unit.upper()})"
                self.max_temp_input.value = self.settings["max_temp"]
            
            self.alert_settings_component.content = self.alert_settings_input_component

        if self.main_column_component is None:
            self.main_column_component = ft.Container(
                ft.Column([self.unit_switcher_component, self.alert_settings_component], width=300, spacing=60),
                alignment=ft.alignment.center,
                padding=30
            )

        self.content = self.main_column_component
        await self.update_async()

    async def _refresh_alert_settings(self, _event):
        await self._retrieve_server_settings()

    async def _update_unit(self, _event):
        self.state.set_unit(self.radio_temp_selector.value)

        if self.min_temp_input is None:
            return
        
        self.min_temp_input.label = f"Max({self.state.data_unit.upper()})"
        self.max_temp_input.label = f"Max({self.state.data_unit.upper()})"
        await self.max_temp_input.update_async()
        await self.min_temp_input.update_async()

    async def _set_alert_loading(self):
        self.alert_bottom_container.content = ft.Row([
                ft.ProgressRing(width=16, height=16, stroke_width = 2),
                ft.Text("sending data..."),
            ])
        self.update_alert_button.disabled = True
        await self.alert_settings_input_component.update_async()

    async def _show_alert_message(self, time, msg, color):
        self.alert_bottom_container.content = ft.Container(
            ft.Text(msg, color=color),
            alignment=ft.alignment.center,
        )
        await self.alert_bottom_container.update_async()
        await asyncio.sleep(time)
        self.alert_bottom_container.content = ft.Container()
        await self.alert_bottom_container.update_async()

    async def _loading_finished_handler(self):
        self.update_alert_button.disabled = False
        self.alert_bottom_container.content = ft.Container()
        
        await self.update_alert_button.update_async()

    async def _update_settings(self, event):
        new_settings = {
            "phone_number": self.phone_input.value,
            "min_temp": int(self.min_temp_input.value),
            "max_temp": int(self.max_temp_input.value),
            "unit": self.state.data_unit
        }

        await self._set_alert_loading()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(ALERT_SETTINGS_URL, json=new_settings) as resp:
                    await self._loading_finished_handler()
                    await self._show_alert_message(5, "Alert settings updated successfully!", "green")
        except:
            await self._loading_finished_handler()
            await self._show_alert_message(5, "No response from server", "red")
