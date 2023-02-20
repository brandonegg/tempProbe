import flet as ft
import asyncio
import requests
import pandas as pd
import aiohttp

TEMPERATURE_HISTORY_URL = "http://tempbox.local/history"

class TemperatureState:
    def __init__(self, page: ft.Page):
        self.data = pd.DataFrame(columns=["Time - Seconds", "Temperature(F)", "Temperature(C)"])
        self.data_unit = "c"
        self.page = page
        self.data_update_event = asyncio.Event()
        asyncio.create_task(self._update_data())

    async def _update_data(self):
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.get(TEMPERATURE_HISTORY_URL) as resp:
                    data = await resp.json()
                    self.data_unit = "c"
                    self.data.loc[:, "Temperature(F)"] = data["f"]
                    self.data.loc[:, "Temperature(C)"] = data["c"]
                    self.data.loc[:, "Time - Seconds"] = list(range(len(data["f"])-1, -1, -1))
                    self.data_update_event.set()
                    print("updated")

            await asyncio.sleep(1)