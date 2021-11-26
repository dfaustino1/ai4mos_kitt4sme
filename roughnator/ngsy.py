"""
Basic NGSI v2 data types.

Examples
--------

>>> from roughnator.ngsy import *


1. NGSI attributes from values.

>>> FloatAttr.from_value(2.3).json()
{"type": "Number", "value": 2.3}
>>> TextAttr.from_value('hi')
type='Text' value='hi'


2. NGSI entity from JSON---ignores unknown attributes.

>>> BaseEntity.parse_raw('{"id": "1", "type": "foo", "x": 3}')
id='1' type='foo'


3. Build entity with preformatted ID

>>> machine1 = MachineEntity(id='').set_id_with_type_prefix('1')
>>> machine1
id='urn:ngsi-ld:Machine:1' type='Machine' AcelR=None fz=None Diam=None ae=None HB=None geom=None Ra=None


4. Don't serialise unset NGSI attributes.

>>> machine1.json(exclude_none=True)
{"id": "urn:ngsi-ld:Machine:1", "type": "Machine"}


5. Build sensors data from dictionary.

>>> sensors_data = {"AcelR": 1, "fz": 2, "Diam": 4, "ae": 5, "HB": 6, "geom": 10, "Ra": 11}
>>> rr = RawReading(**sensors_data)
AcelR=1.0 fz=2.0 Diam=4.0 ae=5.0 HB=6.0 geom=10.0 Ra=11.0


6. Transform sensors data to machine entity and serialise it.

>>> rr.to_machine_entity(entity_id=machine1.id).json(exclude_none=True)
{"id": "urn:ngsi-ld:Machine:1", "type": "Machine", "AcelR": {"type": "Number", "value": 1.0}, "fz": {"type": "Number", "value": 2.0}, "Diam": {"type": "Number", "value": 4.0}, "ae": {"type": "Number", "value": 5.0}, "HB": {"type": "Number", "value": 6.0}, "geom": {"type": "Number", "value": 10.0}, "Ra": {"type": "Number", "value": 11.0}}


7. Same as (6) but now some readings are missing.

>>> rr = RawReading(AcelR=1, Ra=11)
>>> rr.to_machine_entity(entity_id=machine1.id).json(exclude_none=True))
{"id": "urn:ngsi-ld:Machine:1", "type": "Machine", "AcelR": {"type": "Number", "value": 1.0}, "Ra": {"type": "Number", "value": 11.0}}


8. Build roughness estimate entity and serialise it.

>>> ai = RoughnessEstimateEntity(id=machine1.id, acceleration=FloatAttr.from_value(2.3), roughness=FloatAttr.from_value(4.5))
>>> ai.json()
{"id": "urn:ngsi-ld:Machine:1", "type": "RoughnessEstimate", "acceleration": {"type": "Number", "value": 2.3}, "roughness": {"type": "Number", "value": 4.5}}


9. Filter machine entities out of an NGSI update notification.

>>> notification = EntityUpdateNotification(
   ...    data=[
   ...        {"id": "1", "type": "Machine", "Ra": {"value": 1.1}},
   ...        {"id": "2", "type": "NotMe", "Ra": {"value": 2.2}},
   ...        {"id": "3", "type": "Machine", "Ra": {"value": 3.3}}
   ...    ]
   ... )
>>> notification.filter_entities(MachineEntity)
[MachineEntity(id='1', type='Machine', AcelR=None, fz=None, Diam=None, ae=None, HB=None, geom=None, Ra=FloatAttr(type='Number', value=1.1)), MachineEntity(id='3', type='Machine', AcelR=None, fz=None, Diam=None, ae=None, HB=None, geom=None, Ra=FloatAttr(type='Number', value=3.3))]

"""


from pydantic import BaseModel
from typing import Any, List, Optional, Type


def ld_urn(unique_suffix: str) -> str:
    return f"urn:ngsi-ld:{unique_suffix}"


class Attr(BaseModel):
    type: Optional[str]
    value: Any

    @classmethod
    def from_value(cls, v: Any) -> Optional['Attr']:
        if v is None:
            return None
        return cls(value=v)


class FloatAttr(Attr):
    type = 'Number'
    value: float


class TextAttr(Attr):
    type = 'Text'
    value: str


class BaseEntity(BaseModel):
    id: str
    type: str

    def set_id_with_type_prefix(self, unique_suffix: str):
        own_id = f"{self.type}:{unique_suffix}"
        self.id = ld_urn(own_id)
        return self

    @classmethod
    def from_raw(cls, raw_entity: dict) -> Optional['BaseEntity']:
        own_type = cls(id='').type
        etype = raw_entity.get('type', '')
        if own_type != etype:
            return None
        return cls(**raw_entity)


class EntityUpdateNotification(BaseModel):
    data: List[dict]

    def filter_entities(self, entity_class: Type[BaseEntity]) -> [BaseEntity]:
        candidates = [entity_class.from_raw(d) for d in self.data]
        return [c for c in candidates if c is not None]


class MachineEntity(BaseEntity):
    type = 'Machine'
    AcelR: Optional[FloatAttr]
    fz: Optional[FloatAttr]
    Diam: Optional[FloatAttr]
    ae: Optional[FloatAttr]
    HB: Optional[FloatAttr]
    geom: Optional[FloatAttr]
    Ra: Optional[FloatAttr]


class RoughnessEstimateEntity(BaseEntity):
    type = 'RoughnessEstimate'
    acceleration: FloatAttr
    roughness: FloatAttr


class RawReading(BaseModel):
    AcelR: Optional[float]
    fz: Optional[float]
    Diam: Optional[float]
    ae: Optional[float]
    HB: Optional[float]
    geom: Optional[float]
    Ra: Optional[float]

    def to_machine_entity(self, entity_id) -> MachineEntity:
        e = MachineEntity(id=entity_id)

        e.AcelR = FloatAttr.from_value(self.AcelR)
        e.fz = FloatAttr.from_value(self.fz)
        e.Diam = FloatAttr.from_value(self.Diam)
        e.ae = FloatAttr.from_value(self.ae)
        e.HB = FloatAttr.from_value(self.HB)
        e.geom = FloatAttr.from_value(self.geom)
        e.Ra = FloatAttr.from_value(self.Ra)

        return e


# print(FloatAttr.from_value(2.3).json())
# print(TextAttr.from_value('hi'))
#
# foo = BaseEntity.parse_raw('{"id": "1", "type": "foo", "x": 3}')
# print(foo)
#
# machine1 = MachineEntity(id='').set_id_with_type_prefix('1')
# print(machine1)
# print(machine1.json(exclude_none=True))
#
# sensors_data = {"AcelR": 1, "fz": 2, "Diam": 4, "ae": 5, "HB": 6, "geom": 10,
#                 "Ra": 11}
# rr = RawReading(**sensors_data)
# print(rr)
# print(rr.to_machine_entity(entity_id=machine1.id).json(exclude_none=True))
#
# rr = RawReading(AcelR=1, Ra=11)
# print(rr)
# print(rr.to_machine_entity(entity_id=machine1.id).json(exclude_none=True))
#
# ai = RoughnessEstimateEntity(
#     id=machine1.id,
#     acceleration=FloatAttr.from_value(2.3),
#     roughness=FloatAttr.from_value(4.5))
# print(ai.json())
#
# notification = EntityUpdateNotification(
#     data=[
#         {"id": "1", "type": "Machine", "Ra": {"value": 1.1}},
#         {"id": "2", "type": "NotMe", "Ra": {"value": 2.2}},
#         {"id": "3", "type": "Machine", "Ra": {"value": 3.3}}
#     ]
# )
# print(notification.filter_entities(MachineEntity))

notification = EntityUpdateNotification(
    data=[
        {"id": "1", "type": "Machine", "Ra": {"value": 1.1}},
        {"id": "2", "type": "NotMe", "Ra": {"value": 2.2}},
        {"id": "3", "type": "Machine", "Ra": {"value": 3.3}}
    ]
)
print(notification.json())
