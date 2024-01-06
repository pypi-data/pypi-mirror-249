from aiohttp import ClientSession
import asyncio
from ..device import Device
class BzuTech:
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
        self._token = None
        self._operatorid = None
        self._contratoid = None
        self.dispositivos = None
        self.httpheaders = {}
    
    async def start(self) -> bool:
        if await self._async_auth():

            self.httpheaders["Authorization"] = "Bearer " + self._token
            contract = await self._async_set_contrato()
            got_devices = await self._async_set_dispositivos()

            return contract and got_devices
        else: return False

    async def _async_auth(self) -> bool:
        url = "https://back-prd.bzutech.com.br/auth/login/"
        data = {"operador_email": self.email, "password": self.password}
        client = ClientSession()
        try:
            async with client.post(url=url, data=data) as resp:
                resposta = await resp.json()
                await client.close()
                self._token = resposta["tokens"]["access"]
                self._operatorid = resposta["id"]
                return True
        except(KeyError):
            return False

    async def _async_set_contrato(self) -> bool:
        """"""
        url = "https://back-prd.bzutech.com.br/operador/navbar/" + str(self._operatorid)
        client = ClientSession()
        async with client.get(url=url, headers = self.httpheaders) as resp:
            resposta = await resp.json()
            await client.close()
            self._contratoid = resposta["empresas"][1]["contratos_id"]
            return True

    async def _async_set_dispositivos(self) -> bool:
        url = "https://back-prd.bzutech.com.br/dispositivos/listar/" + str(
            self._contratoid
        )
        dispositivos = {}
        client = ClientSession()
        
        async with client.get(url=url, headers = self.httpheaders) as resp:
            resposta = await resp.json()
            for disp in resposta:
                if disp["status_dispositivo"] == 1:
                    chipid = int(disp["boot_chip_id"])
                    dispname = (
                        disp["dispnum"]
                        if disp["dispname"] == None
                        else disp["dispname"]
                    )
                    dispositivo = Device(chipid, self.httpheaders, dispname)
                    await dispositivo.initialize()
                    dispositivos[str(chipid)] = dispositivo
            self.dispositivos = dispositivos
            await client.close()
            return True
    
    def get_token(self) -> str:
        return self._token

    def get_device_names(self) -> list:
        return list(self.dispositivos.keys())

    def get_sensors(self, chipid: str) -> list:
        if chipid in self.get_device_names():
            return list(self.dispositivos[chipid].get_sensor_names())
        return ["-1"]
    
    def get_reading(self, chipid: str, sensorname:str):
        return self.dispositivos[chipid].get_readings(sensorname.upper())