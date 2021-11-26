from fastapi import FastAPI, Header
from typing import Optional

from roughnator.enteater import process_update
from roughnator.ngsy import MachineEntity
from roughnator.util.ngsi.entity import EntityUpdateNotification
from roughnator.util.ngsi.headers import FiwareContext


VERSION = '0.1.0'

app = FastAPI()


@app.get('/')
def read_root():
    return {'roughnator': VERSION}


@app.get("/version")
def read_version():
    return read_root()


@app.post("/updates")
def post_updates(notification: EntityUpdateNotification,
                 fiware_service: Optional[str] = Header(None),
                 fiware_servicepath: Optional[str] = Header(None),
                 fiware_correlator: Optional[str] = Header(None)):
    ctx = FiwareContext(
        service=str(fiware_service), service_path=str(fiware_servicepath),
        correlator=str(fiware_correlator)
    )
    updated_machines = notification.filter_entities(MachineEntity)
    process_update(ctx, updated_machines)
