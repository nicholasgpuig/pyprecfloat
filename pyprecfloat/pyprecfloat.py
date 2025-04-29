import struct
import math

# separate child class; arb length but max of 32
# Have distance in bits from lsb, value, child object
# addition: add children to parent recursively
# addition: track carry; update distance or add to parent if distance is 0
# Add exponents and multiply mantissa
# decimal_precision = 50; number of decimal places retained during initialization and math operations

# Retrieve child values: recurse and get all vals, add them and divide by denominator to get decimal

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
        self.exponent = exponent # DEBUG
        self.child = None

    # Initial n is n % d
    # distance -1 or 1 based on direction
    # Currently examining in space of 32 bits - if first bits are zero, shift into space and add to distance
    def createChild(self, n, distance=0): # How to get distance ; change -1 to class constant
        if not n: # No more bits left
            return None
        
        distance -= 1 # Child values start 1 bit behind parent by default
        
        # Remove leading zeros and add them to distance
        lsb = (n & -n).bit_length() - 1
        if lsb > 0:
            distance -= lsb
            n >>= lsb

        size = 2 # DEBUG - change to 32
        val = n & 3 # 11
        trailing_zeros = val.bit_length() - size
        
        newChild = ChildNode(val, distance)
        newChild.child = self.createChild(n >> size, trailing_zeros)
        return newChild
    
    def showNodes(self):
        print("\nPARENT")
        print(self.toFloat())
        print()
        if self.child:
            c = self.child
            while c:
                print("CHILD")
                print(bin(c.value)[2:])
                print("distance:" + str(c.distance) + "\n")
                c = c.child


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

        exponent = ((p & 0x7F800000) >> 23) - 127

        mantissa_bits = p & 0x7FFFFF
        mantissa = 1 + mantissa_bits / (1 << 23)

        return sign * mantissa * (2 ** exponent)

    def reverseBits(num) -> int:
        res = 0
        bitlen = len(bin(num)) - 2 #Update with pos of floating point
        for i in range(bitlen):
            a = (num >> i) & 1
            res |= a << (bitlen - 1 - i)
        return res

    def verify(self):
        return struct.unpack('f', struct.pack('I', self.pfloat))[0]
    
    def getSign(self, num: int | float):
        if num > 0:
            return num, 0
        return -1 * num, 1
    

class ChildNode:
    
    def __init__(self, value, distance):
        self.value = value
        self.distance = distance
        self.child = None