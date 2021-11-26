from fastapi import FastAPI

from roughnator.enteater import process_update
from roughnator.ngsy import EntityUpdateNotification, MachineEntity


VERSION = '0.1.0'

app = FastAPI()


@app.get('/')
def read_root():
    return {'roughnator': VERSION}


@app.get("/version")
def read_version():
    return read_root()


@app.post("/updates")
def post_updates(notification: EntityUpdateNotification):
    updated_machines = notification.filter_entities(MachineEntity)
    process_update(updated_machines)
