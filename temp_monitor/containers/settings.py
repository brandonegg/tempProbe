'''
Module for rendering the settings page details
'''
import flet as ft
import requests

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
        
        settings_res = self._retrieve_server_settings()
        if (settings_res.status_code == 200):
            self._add_settings(settings_res.json())

    def _wait_for_response(self):
        pass

    def _retrieve_server_settings(self):
        '''
        Fetches alert settings from temp box server.
        '''
        return requests.get(ALERT_SETTINGS_URL)

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
