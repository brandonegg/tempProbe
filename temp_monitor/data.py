import asyncio
import flet as ft
import pandas as pd
import aiohttp
from temp_monitor.globals import BASE_URL

TEMPERATURE_HISTORY_URL = f"{BASE_URL}/history"
FAILURE_THRESHOLD = 5

class TemperatureState:
    '''
    Manages requests and temperature data state for the monitor view.
    '''
    def __init__(self, page: ft.Page):
        self.data = pd.DataFrame(columns=["Time - Seconds", "Temperature(F)", "Temperature(C)"])
        self.data_unit = "c"
        self.page = page
        self.request_fail_count = 0
        self.server_connected = False
        self.sensor_connected = False
        self.data_update_event = asyncio.Event()
        asyncio.create_task(self._update_data())

    def set_unit(self, unit):
        self.data_unit = unit
        asyncio.create_task(self._update_data())

    async def _update_data(self):
        while True:
            try:
                session_timeout = aiohttp.ClientTimeout(total=None,sock_connect=2,sock_read=2)
                async with aiohttp.ClientSession(timeout=session_timeout) as session:
                    async with session.get(TEMPERATURE_HISTORY_URL) as resp:
                        data = await resp.json()
                        self.server_connected = True
                        self.sensor_connected = bool(data["sensor_connected"])
                        self.data.loc[:, "Temperature(F)"] = data["f"]
                        self.data.loc[:, "Temperature(C)"] = data["c"]
                        self.data.loc[:, "Time - Seconds"] = list(range(len(data["f"])-1, -1, -1))
                        self.data_update_event.set()
                        self.request_fail_count = 0
            except:
                if (self.request_fail_count >= FAILURE_THRESHOLD):
                    print("unable to find server")
                    self.server_connected = False
                    self.sensor_connected = False
                    self.data_update_event.set()
                else:
                    self.request_fail_count += 1

            await asyncio.sleep(0.2)
