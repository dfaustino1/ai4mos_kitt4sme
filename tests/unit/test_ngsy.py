from roughnator.ngsy import *


def test_float_attr_serialisation():
    want = '{"type": "Number", "value": 2.3}'
    got = FloatAttr.new(2.3).json()
    assert want == got


def test_readings_to_machine_entity_json():
    sensors_data = {"AcelR": 1, "fz": 2, "Diam": 4, "ae": 5, "HB": 6,
                    "geom": 10, "Ra": 11}
    rr = RawReading(**sensors_data)

    machine1 = MachineEntity(id='').set_id_with_type_prefix('1')
    got = rr.to_machine_entity(entity_id=machine1.id).to_json()

    want = '{"id": "urn:ngsi-ld:Machine:1", "type": "Machine", ' \
           '"AcelR": {"type": "Number", "value": 1.0}, ' \
           '"fz": {"type": "Number", "value": 2.0}, ' \
           '"Diam": {"type": "Number", "value": 4.0}, ' \
           '"ae": {"type": "Number", "value": 5.0}, ' \
           '"HB": {"type": "Number", "value": 6.0}, ' \
           '"geom": {"type": "Number", "value": 10.0}, ' \
           '"Ra": {"type": "Number", "value": 11.0}}'
    assert want == got
