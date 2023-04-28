from fipy.ngsi.entity import EntityUpdateNotification
from fipy.ngsi.headers import FiwareContext
from fastapi import FastAPI, Header
from typing import Optional

from roughnator import __version__
from roughnator.enteater import process_update
import roughnator.log as log
from roughnator.ngsy import Productions


app = FastAPI()


@app.get('/')
def read_root():
    return {'roughnator': __version__}


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

    log.received_ngsi_entity_update(ctx, notification)

    updated_productions = notification.filter_entities(Productions)
    
    if updated_productions:
        process_update(ctx, updated_productions)
