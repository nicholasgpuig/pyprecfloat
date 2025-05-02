import sys
import os
from pyprecfloat.pyprecfloat import PFloat

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


def test_pfloat_init():
    assert PFloat(1).pfloat == 1065353216
    assert PFloat(-1).pfloat == 3212836864
    assert PFloat(8224953).pfloat == 1257963890  # 8224953 = 0b11111011000000010111001
    assert (
        PFloat(170141163178059628080016879768632819712).pfloat == 2130706430
    )  # 1 * 23 << 254


def test_pfloat_fraction_init():
    assert PFloat(0.5).pfloat == 1056964608
    assert PFloat(-0.5).pfloat == 3204448256
    assert PFloat(100.348975).pfloat == 1120449196


def test_tofloat():
    assert PFloat(0.125).toFloat() == 0.125
    assert PFloat(-0.125).toFloat() == -0.125
    assert PFloat(83.16).toFloat() == 83.16
    assert (
        PFloat(170141163178059628080016879768632819712).toFloat()
        == 170141163178059628080016879768632819712
    )


def test_child_creation():
    z = PFloat(33554435).child
    assert z.value == 3 and z.distance == 0
    y = PFloat(100.348975).child
    assert y.value == 217 and z.distance == 0
