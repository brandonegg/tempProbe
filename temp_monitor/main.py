'''
Main Flet app.
'''
import flet as ft
from temp_monitor.containers.monitor import MonitorContainer
from temp_monitor.containers.settings import SettingsContainer
from temp_monitor.data import TemperatureState

async def init_app(page):
    state = TemperatureState(page)
    settings_tab = SettingsContainer(page, state, alignment=ft.alignment.center)

    # Tab Change Listener:
    async def on_change(event):
        if int(event.data) == 1: #settings page
            #fix any unchanged settings
            await settings_tab._render()

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Monitor",
                content=MonitorContainer(page, state, alignment=ft.alignment.center),
            ),
            ft.Tab(
                text="Settings",
                icon=ft.icons.SETTINGS,
                content=settings_tab,
            ),
        ],
        expand=1,
        on_change=on_change
    )

    await page.add_async(tabs)
    await page.update_async()

if __name__ == "__main__":
    async def main(page: ft.Page):
        '''
        Flet entry point to application.
        '''
        page.title = "Temperature Monitor"
        page.padding = 0

        await init_app(page)

    ft.app(target=main)
