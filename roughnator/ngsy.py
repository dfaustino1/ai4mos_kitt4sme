"""
Roughnator NGSI v2 data types.

Examples
--------

>>> from fipy.ngsi.entity import *
>>> from roughnator.ngsy import *


1. NGSI attributes from values.

>>> FloatAttr.new(2.3).json()
'{"type": "Number", "value": 2.3}'
>>> print(TextAttr.new('hi'))
type='Text' value='hi'


2. NGSI entity from JSON---ignores unknown attributes.

>>> BaseEntity.parse_raw('{"id": "1", "type": "foo", "x": 3}')
BaseEntity(id='1', type='foo')


3. Build entity with preformatted ID

>>> machine1 = MachineEntity(id='').set_id_with_type_prefix('1')
>>> machine1.id, machine1.type
('urn:ngsi-ld:Machine:1', 'Machine')


4. Don't serialise unset NGSI attributes.

>>> machine1.to_json()
'{"id": "urn:ngsi-ld:Machine:1", "type": "Machine"}'


5. Build sensors data from dictionary.

>>> sensors_data = {"AcelR": 1, "fz": 2, "Diam": 4, "ae": 5, "HB": 6,
...                 "geom": 10, "Ra": 11}
>>> rr = RawReading(**sensors_data)
>>> print(rr)
AcelR=1.0 fz=2.0 Diam=4.0 ae=5.0 HB=6.0 geom=10.0 Ra=11.0


6. Transform sensors data to machine entity and serialise it.

>>> rr.to_machine_entity(entity_id=machine1.id).to_json()
'{"id": "urn:ngsi-ld:Machine:1", "type": "Machine", \
"AcelR": {"type": "Number", "value": 1.0}, \
"fz": {"type": "Number", "value": 2.0}, \
"Diam": {"type": "Number", "value": 4.0}, \
"ae": {"type": "Number", "value": 5.0}, \
"HB": {"type": "Number", "value": 6.0}, \
"geom": {"type": "Number", "value": 10.0}, \
"Ra": {"type": "Number", "value": 11.0}}'


7. Same as (6) but now some readings are missing.

>>> rr = RawReading(AcelR=1, Ra=11)
>>> rr.to_machine_entity(entity_id=machine1.id).to_json()
'{"id": "urn:ngsi-ld:Machine:1", "type": "Machine", \
"AcelR": {"type": "Number", "value": 1.0}, \
"Ra": {"type": "Number", "value": 11.0}}'


8. Build roughness estimate entity and serialise it.

>>> ai = RoughnessEstimateEntity(id=machine1.id,
...                              acceleration=FloatAttr.new(2.3),
...                              roughness=FloatAttr.new(4.5))
>>> ai.json()
'{"id": "urn:ngsi-ld:Machine:1", "type": "RoughnessEstimate", \
"acceleration": {"type": "Number", "value": 2.3}, \
"roughness": {"type": "Number", "value": 4.5}}'


9. Filter machine entities out of an NGSI update notification.

>>> notification = EntityUpdateNotification(
...    data=[
...        {"id": "1", "type": "Machine", "Ra": {"value": 1.1}},
...        {"id": "2", "type": "NotMe", "Ra": {"value": 2.2}},
...        {"id": "3", "type": "Machine", "Ra": {"value": 3.3}}
...    ]
... )
>>> notification.filter_entities(MachineEntity)
[MachineEntity(id='1', type='Machine', AcelR=None, fz=None, Diam=None, \
ae=None, HB=None, geom=None, Ra=FloatAttr(type='Number', value=1.1)), \
MachineEntity(id='3', type='Machine', AcelR=None, fz=None, Diam=None, \
ae=None, HB=None, geom=None, Ra=FloatAttr(type='Number', value=3.3))]

"""

from fipy.ngsi.entity import BaseEntity, FloatAttr
from pydantic import BaseModel
from typing import Optional


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

        e.AcelR = FloatAttr.new(self.AcelR)
        e.fz = FloatAttr.new(self.fz)
        e.Diam = FloatAttr.new(self.Diam)
        e.ae = FloatAttr.new(self.ae)
        e.HB = FloatAttr.new(self.HB)
        e.geom = FloatAttr.new(self.geom)
        e.Ra = FloatAttr.new(self.Ra)

        return e


# print(FloatAttr.from_value(2.3).json())
# print(TextAttr.from_value('hi'))
#
# foo = BaseEntity.parse_raw('{"id": "1", "type": "foo", "x": 3}')
# print(foo)
#
# machine1 = MachineEntity(id='').set_id_with_type_prefix('1')
# print(machine1)
# print(machine1.to_json())
#
# sensors_data = {"AcelR": 1, "fz": 2, "Diam": 4, "ae": 5, "HB": 6, "geom": 10,
#                 "Ra": 11}
# rr = RawReading(**sensors_data)
# print(rr)
# print(rr.to_machine_entity(entity_id=machine1.id).to_json())
#
# rr = RawReading(AcelR=1, Ra=11)
# print(rr)
# print(rr.to_machine_entity(entity_id=machine1.id).to_json())
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
