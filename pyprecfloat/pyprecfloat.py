import struct
import math

# separate child class; arb length but max of 32
# Have distance in bits from lsb, value, child object
# addition: add children to parent recursively
# addition: track carry; update distance or add to parent if distance is 0
# Add exponents and multiply mantissa
# decimal_precision = 50; number of decimal places retained during initialization and math operations

class PFloat:

    def __init__(self, num: int = 0):
        # Create 32-bit integer representation of given integer
        divisor_exponent = 0
        sign, num = 0 if num >= 0 else 1, abs(num)
        if isinstance(num, float):
            num, d = num.as_integer_ratio()
            divisor_exponent = d.bit_length() - 1 # power of 2

        msb = num.bit_length() - 1 # Subtract space of implicit leading 1
        exponent = msb + 127 - divisor_exponent
        dist_from_mpos = 23 - msb

        shifted = num << dist_from_mpos if dist_from_mpos >= 0 else num >> (-1 * dist_from_mpos)
        mantissa = shifted & 0x7FFFFF # 11111111111111111111111; len 23
        self.pfloat = (sign << 31) | exponent << 23 | mantissa
    
    def toInt(self) -> int:
        pos_adjustment = 23

        sign = self.pfloat & (1 << 31)
        mantissa = self.pfloat & 0x7FFFFF | 1 << 23
        exponent = (self.pfloat & 0x7F800000) >> 23
        if (pos_adjustment - (exponent - 127) >= 0):
            original = mantissa >> pos_adjustment - (exponent - 127)
        else:
            original = mantissa << (exponent - 127) - pos_adjustment
        return original * (-1 if sign else 1)

    def toFloat(self) -> float:
        p = self.pfloat

        sign = -1 if (p >> 31) & 1 else 1

        exponent = ((self.pfloat & 0x7F800000) >> 23) - 127

        mantissa_bits = p & 0x7FFFFF
        mantissa = 1 + mantissa_bits / (1 << 23)

        return sign * mantissa * (2 ** exponent)


    def reverseBits(num):
        res = 0
        bitlen = len(bin(num)) - 2 #Update with pos of floating point
        for i in range(bitlen):
            a = (num >> i) & 1
            res |= a << (bitlen - 1 - i)
            print(bin(res))
        return res

    def veritfy(self):
        return struct.unpack('f', struct.pack('I', self.pfloat))[0]
    
    def getSign(self, num: int | float):
        if num > 0:
            return num, 0
        return -1 * num, 1