from typing import runtime_checkable, Protocol, ClassVar
from dataclasses import dataclass
import requests
import random


@runtime_checkable
class TemperatureSensor(Protocol):
    def read_temperature(self) -> float:...
    @property
    def get_sensor_id(self) -> str:...


@dataclass
class WeatherApiSensor:
    temperature:str
    _id:str="WAS26-Odessa"
    def __init__(self) -> None:
        try:
            response = requests.get("https://wttr.in/odessa?format=j1", timeout=10)
            response.raise_for_status()
            data = response.json()
            self.temperature = data["current_condition"][0]["temp_C"]

        except requests.exceptions.HTTPError as e:
            print(f"Ошибка HTTP: {e}")
        except requests.exceptions.Timeout:
            print("Превышено время ожидания")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")

    def read_temperature(self) -> float:
        return float(self.temperature)
    @property
    def get_sensor_id(self) -> str:
        return self._id

@dataclass
class SimulatedSensor:
    base:float
    devitation:float
    temperature:float
    def __init__(self,base,devitation) -> None:
        self.base = base
        self.devitation = devitation
    def read_temperature(self) -> float:
        return self.base + float(random.randint(int(self.devitation*-1),int(self.devitation)))
    @property
    def get_sensor_id(self) -> str:
        return "SimulatedSensor"
@dataclass
class FakeAlways25:
    temperature:ClassVar[float]=25.0
    _id:str="Fake-25"
    def read_temperature(self) -> float:
        return self.temperature
    @property
    def get_sensor_id(self) -> str:
        return self._id

w=WeatherApiSensor()
print(w.read_temperature())
print(w.get_sensor_id)
s=SimulatedSensor(23,10)
print(s.read_temperature())
print(s.get_sensor_id)
fa=FakeAlways25()
print(fa.read_temperature())
print(fa.get_sensor_id)


