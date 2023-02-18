'''
Module for rendering the settings page details
'''
import flet as ft

class SettingsContainer(ft.Container):
    '''
    Settings page view
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
        self._add_settings()

    def _add_settings(self):
        self.phone_input = ft.TextField(label="Phone Number", hint_text='include area code', value="", text_align=ft.TextAlign.RIGHT, width=300)
        self.min_temp_input = ft.TextField(label="Min", expand=True)
        self.max_temp_input = ft.TextField(label="Max", expand=True)
        self.update_button = ft.OutlinedButton(text="update")

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
