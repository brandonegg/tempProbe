'''
Module for rendering the settings page details
'''
import flet as ft
import requests
import asyncio
import aiohttp

ALERT_SETTINGS_URL = "http://tempbox.local/alert"

class SettingsContainer(ft.Container):
    '''
    Settings page view
    '''
    def __init__(
        self,
        page: ft.Page,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.page = page
        # Stores phone min/max and phone_number
        self.settings = None
        # Components
        self.unit_switcher_component = None
        self.refresh_data_component = None
        self.alert_settings_component = None
        self.alert_settings_input_component = None
        self.main_column_component = None

        self._settings_update_event = asyncio.Event()
        asyncio.create_task(self._render_update_listener())

    async def _retrieve_server_settings(self):
        '''
        Fetches alert settings from temp box server.
        '''
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ALERT_SETTINGS_URL) as resp:
                    self.settings = await resp.json()
                    self._settings_update_event.set()
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
            self.unit_switcher_component = ft.Container(
                ft.Column([
                    ft.RadioGroup(content=ft.Row([
                        ft.Radio(value= "c", label="Celsius"),
                        ft.Radio(value= "f", label="Fahrenheit")
                    ])),
                    ft.OutlinedButton(text="update", on_click=self._update_settings)
                ]),
                padding=30,
                width=200
            )

        if self.alert_settings_component is None:
            self.alert_settings_component = ft.Container()


        if self.settings is None:
            # render refresh button
            if self.refresh_data_component is None:
                self.refresh_data_component = ft.Container(
                    ft.OutlinedButton(text="refresh", on_click=self._retrieve_server_settings)
                )

            self.alert_settings_component.content = self.refresh_data_component
        else:
            if self.alert_settings_input_component is None:
                self.phone_input = ft.TextField(label="Phone Number", hint_text='include area code', value=self.settings["phone_number"], text_align=ft.TextAlign.RIGHT, width=300)
                self.min_temp_input = ft.TextField(label=f"Min ({self.settings['unit'].upper()})", value=self.settings["min_temp"], expand=True)
                self.max_temp_input = ft.TextField(label=f"Max ({self.settings['unit'].upper()})", value=self.settings["max_temp"], expand=True)
                self.update_button = ft.OutlinedButton(text="update", on_click=self._update_settings)

                self.alert_settings_input_component = ft.Container(
                    ft.Column(
                        [
                            self.phone_input,
                            ft.Text("Temperature Alert Triggers:"),
                            ft.Row(
                                [
                                    self.min_temp_input,
                                    self.max_temp_input
                                ],
                                width=200,
                                spacing=20,
                            ),
                            ft.Container(
                                self.update_button,
                                alignment=ft.alignment.center,
                            )
                        ],
                        width=200, 
                    ),
                    padding=30,
                )

            self.alert_settings_component.content = self.alert_settings_input_component

        if self.main_column_component is None:
            self.main_column_component = ft.Column([self.unit_switcher_component, self.alert_settings_component])

        self.content = self.main_column_component
        await self.update_async()


    def _add_settings(self, settings):
        self.phone_input = ft.TextField(label="Phone Number", hint_text='include area code', value=settings["phone_number"], text_align=ft.TextAlign.RIGHT, width=300)
        self.min_temp_input = ft.TextField(label=f"Min ({settings['unit'].upper()})", value=settings["min_temp"], expand=True)
        self.max_temp_input = ft.TextField(label=f"Max ({settings['unit'].upper()})", value=settings["max_temp"], expand=True)
        self.update_button = ft.OutlinedButton(text="update", on_click=self._update_settings)

        self.content = ft.Container(
            ft.Column(
                [
                    self.phone_input,
                    ft.Text("Temperature Alert Triggers:"),
                    ft.Row(
                        [
                            self.min_temp_input,
                            self.max_temp_input
                        ],
                        width=200,
                        spacing=20,
                    ),
                    ft.Container(
                        self.update_button,
                        alignment=ft.alignment.center,
                    )
                ],
                width=200, 
            ),
            padding=30,
        ) 
    
    def _refresh_data(self):
        response = requests.get(ALERT_SETTINGS_URL)
        print(response.json())

    def _update_settings(self, event):
        new_settings = {
            "phone_number": self.phone_input.value,
            "min_temp": int(self.min_temp_input.value),
            "max_temp": int(self.max_temp_input.value),
            "unit": "c"
        }

        requests.post(ALERT_SETTINGS_URL, json = new_settings)
        self._refresh_data()
