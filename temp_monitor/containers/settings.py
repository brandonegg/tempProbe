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
        self.content = ft.Text('TODO')
