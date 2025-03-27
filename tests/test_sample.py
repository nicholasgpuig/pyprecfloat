import sys
import os
from pyprecfloat.pyprecfloat import PFloat

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

def test_pfloat_init():
    assert PFloat(1).pfloat == 1065353216
    assert PFloat(-1).pfloat == 3212836864
    assert PFloat(8224953).pfloat == 1257963890 # 8224953 = 0b11111011000000010111001
    assert PFloat(170141163178059628080016879768632819712).pfloat == 2130706430 # 1 * 23 << 254

