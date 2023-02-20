import flet as ft
import asyncio
import requests
import pandas as pd

TEMPERATURE_HISTORY_URL = "http://tempbox.local/history"

class TemperatureState:
    def __init__(self, page: ft.Page):
        self.data = pd.DataFrame(columns=["Time - Seconds", "Temperature(F)", "Temperature(C)"])
        self.data_unit = "c"
        self.page = page
        self.data_update_event = asyncio.Event()
        asyncio.create_task(self._update_data())

    async def _update_data(self):
        #while True:
            response = requests.get(TEMPERATURE_HISTORY_URL)
            if response.status_code == 200:
                data = response.json()

                self.data_unit = "c"
                self.data.loc[:, "Temperature(F)"] = data["f"]
                self.data.loc[:, "Temperature(C)"] = data["c"]
                self.data.loc[:, "Time - Seconds"] = list(range(len(data["f"])-1, -1, -1))
                self.data_update_event.set()
                print("updated")
            else:
                self.data.drop(self.data.index, inplace=True)

            await self.page.update_async()
            #await asyncio.sleep(1)