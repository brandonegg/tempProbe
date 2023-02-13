'''
Main Flet app.
'''
import flet as ft
from temp_monitor.containers.monitor import MonitorContainer
from temp_monitor.containers.settings import SettingsContainer

class TemperatureMonitorApp:
    '''
    Main application. Holds all flet objects for easy state maintenance
    '''
    def __init__(self, page: ft.Page):
        self.page = page

        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Monitor",
                    content=MonitorContainer(self, page),
                ),
                ft.Tab(
                    text="Settings",
                    icon=ft.icons.SETTINGS,
                    content=SettingsContainer(self, page, alignment=ft.alignment.center),
                ),
            ],
            expand=1
        )

        self.page.controls.append(self.tabs)
        self.page.update()

if __name__ == "__main__":
    def main(page: ft.Page):
        '''
        Flet entry point to application.
        '''
        page.title = "Temperature Monitor"
        page.padding = 0
        TemperatureMonitorApp(page)

    ft.app(target=main)
