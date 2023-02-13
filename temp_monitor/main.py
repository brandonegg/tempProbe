'''
Main Flet app entry point.
'''
import flet as ft
import temp_monitor.pages.monitor as monitor
import temp_monitor.pages.settings as settings

def settings_page():
    '''
    Settings page view
    '''
    return ft.Text("TODO")

def main(page: ft.Page):
    '''
    Main page display
    '''
    page.title = 'Temperature Monitor'

    tabs = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Monitor",
                content=ft.Container(
                    content=monitor.page(), alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                text="Settings",
                icon=ft.icons.SETTINGS,
                content=settings.page(),
            ),
        ],
        expand=1,
    )

    page.add(tabs)

ft.app(target=main)
