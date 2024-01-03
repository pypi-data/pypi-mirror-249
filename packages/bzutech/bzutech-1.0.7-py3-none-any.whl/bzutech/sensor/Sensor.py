from aiohttp import ClientSession
class Sensor:
    def __init__(self, chipid: int, canal: str, apelido: str, token:dict) -> None:
        self.chipid = "11000"[0 : 8 - len(str(chipid))] + str(chipid)
        self.apelido = canal
        self.httpheaders = token
        self.porta = canal[-1]

        tipos_sensores = {
            "TMP": "Temperatura",
            "HUM": "Humidade",
            "VOT": "Voltagem",
            "CO2": "CO2",
            "CUR": "Corrente",
            "LUM": "Luminosidade",
            "PIR": "",
            "DOOR": "Porta",
            "DOR": "DOR",
            "M10": "M10",
            "M25": "M25",
            "M40": "M40",
            "SND": "SOM",
            "M01": "M01",
            "C01": "C01",
            "VOC": "Gases Volateis",
            "DOS": "DOS",
            "VOA": "Voltagem",
            "VOB": "Voltagem",
            "VOC": "Voltagem",
            "CRA": "Corrente",
            "CRB": "Corrente",
            "CRC": "Corrente",
            "VRA": "Voltagem",
            "VRB": "Voltagem",
            "VRC": "Voltagem",
            "C05": "C05",
            "C01": "C01",
            "C25": "C25",
            "C40": "C40",
            "C10": "C10",


        }

        cod_sensores = {
            "SPS30-C01": "87",
            "SPS30-M10": "70",
            "SPS30-M40": "68",
            "SPS30-M25": "66",
            "SPS30-M01": "64",
            "DOOR-DOS": "86",
            "SHT26-HUM": "85",
            "SHT24-HUM": "84",
            "SHT25-TMP": "83",
            "RTZSBZ-SND": "82",
            "SGP30-CO2": "62",
            "SGP30-VOC": "60",
            "SCT013-CUR": "02",
            "SCHNE-CUR": "14",
            "ZMPT-CUR": "06",
            "SHT20-HUM": "21",
            "SHT30-HUM": "08",
            "AHT10-HUM": "07",
            "BH1750-LUM": "11",
            "TSL2561-LUM": "05",
            "DOOR-DOR": "23",
            "SR602-DOOR": "04",
            "S16L201D-PIR": "13",
            "SR602-PIR": "10",
            "AHT10-TMP": "01",
            "SHT30-TMP": "03",
            "AHT20-TMP": "22",
            "SHT20-TMP": "20",
            "ZMPT-VOT": "09",
            "SCHNE-VOT": "12",
            "ADS7878-VOA": "88",
            "ADS7878-VOB": "89",
            "ADS7878-VOC": "90",
            "ADS7878-CRA": "91",
            "ADS7878-CRB": "92",
            "ADS7878-CRC": "93",
            "ADS7878-VRA": "94",
            "ADS7878-VRB": "95",
            "ADS7878-VRC": "96",
            "SPS30-C25": "97",
            "SPS30-C40": "98",
            "SPS30-C10": "99",
            "SPS30-C05": "100",


        }

        self.tipo = tipos_sensores[canal.split("-")[1]]
        self.sensorref = canal[-1] + "00" + cod_sensores[canal[0:-2]]

    async def get_leitura(self):
        url = (
            "https://back-prd.bzutech.com.br/logs/ultima_medicao/"
            + self.chipid
            + "/"
            + self.sensorref
        )
        client = ClientSession()
        async with client.get(url, headers = self.httpheaders) as resp:
            resposta = await resp.json()
            await client.close()
            return(int(resposta["medicao"]) / 1000000)