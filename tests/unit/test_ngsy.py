from roughnator.ngsy import *


def test_float_attr_serialisation():
    want = '{"type": "Number", "value": 2.3}'
    got = FloatAttr.from_value(2.3).json()
    assert want == got
