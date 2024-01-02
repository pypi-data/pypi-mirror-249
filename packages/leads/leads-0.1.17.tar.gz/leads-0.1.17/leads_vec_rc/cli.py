from json import loads
from os import mkdir
from os.path import abspath, exists

from fastapi import FastAPI

from leads.comm import *
from leads.utils import *
from leads_dashboard import *

config = load_config(abspath(__file__)[:-6] + "config.json")
if not exists(config.data_dir):
    mkdir(config.data_dir)
    print(f"Data dir \"{config.data_dir}\" created")

time_stamp_record = DataPersistence[int](config.data_dir + "/time_stamp.csv", max_size=2000)
speed_record = DataPersistence[float](config.data_dir + "/speed.csv", max_size=2000)


class CustomCallback(Callback):
    def on_connect(self, service: Service, connection: Connection) -> None:
        print("Connected")

    def on_fail(self, service: Service, error: Exception) -> None:
        print(error)

    def on_receive(self, service: Service, msg: bytes) -> None:
        data = loads(msg.decode())
        time_stamp_record.append(data["t"])
        speed_record.append(data["front_wheel_speed"])

    def on_disconnect(self, service: Service, connection: Connection) -> None:
        time_stamp_record.close()
        speed_record.close()


client = start_client(config.comm_addr, create_client(config.comm_port, CustomCallback()), True)

app = FastAPI(title="LEADS VeC Remote Controller")


@app.get("/")
async def index() -> str:
    return "LEADS VeC Remote Controller"


@app.get("/time_stamp")
async def time_stamp() -> list[int]:
    return time_stamp_record.to_list()


@app.get("/speed")
async def speed() -> list[float]:
    return speed_record.to_list()
