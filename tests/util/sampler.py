from fipy.ngsi.entity import StructuredValueAttr
from fipy.ngsi.orion import OrionClient
from fipy.sim.sampler import DevicePoolSampler
from typing import Optional, Text
from tests.util.fiware import orion_client
from roughnator.ngsy import Productions
    

class ProductionSampler():
    def __init__(self, orion: OrionClient, json_data, id):
        self._orion = orion
    
        self.production = Productions(
                id=id,
                productions=StructuredValueAttr.new(json_data),
            )
    
    def insert_entity(self):
        self._orion.upsert_entity(self.production)
