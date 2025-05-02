import struct
import math

class PFloat:
    CHILD_NODE_SIZE = 8

    def __init__(self, num: int | float = 0):
        # Create 32-bit integer representation of given integer
        # Bits unable to be stored in the mantissa are stored in child nodes, forming a linked list of values with this object at the head
        self.child = None

        divisor_exponent = 0
        sign, num = 0 if num >= 0 else 1, abs(num)
        if isinstance(num, float):
            num, d = num.as_integer_ratio()
            divisor_exponent = d.bit_length() - 1  # power of 2

        msb = num.bit_length() - 1  # Subtract space of implicit leading 1
        exponent = msb + 127 - divisor_exponent
        dist_from_mpos = 23 - msb

        if dist_from_mpos >= 0:
            shifted = num << dist_from_mpos
            mantissa = shifted & 0x7FFFFF  # 11111111111111111111111; len 23
        else:  # msb is further than 23 bits
            dist_from_mpos = abs(dist_from_mpos)

            shifted = num >> dist_from_mpos
            mantissa = shifted & 0x7FFFFF
            nonMantissaBits = num ^ ((mantissa + (1 << 23)) << dist_from_mpos)

            shift = nonMantissaBits.bit_length() - self.CHILD_NODE_SIZE
            self.child = self.createChild(nonMantissaBits, shift)

        self.pfloat = (sign << 31) | exponent << 23 | mantissa
        self.exponent = exponent  # DEBUG

    def createChild(self, n, shift, distance=0):
        if not n:  # No more bits left
            return None

        numLeadingZeros = (shift + self.CHILD_NODE_SIZE) - n.bit_length()
        if numLeadingZeros:
            distance -= numLeadingZeros
            shift -= numLeadingZeros

        if shift < 0:  # last set of bits
            shift = 0
        val = n >> shift  # No need to bitmask since these are the highest set bits
        n ^= val << shift
        trailing_zeros = (val & -val).bit_length() - 1  # lsb
        val >>= trailing_zeros

        newChild = ChildNode(val, distance)
        newChild.child = self.createChild(
            n, shift - self.CHILD_NODE_SIZE, -trailing_zeros
        )
        return newChild

    def toInt(self) -> int:
        return int(self.toFloat())

    def toFloat(self) -> float:
        p = self.pfloat

        sign = -1 if p >> 31 else 1

        exponent = ((p & 0x7F800000) >> 23) - 127
        mantissa_bits = (1 << 23) | (p & 0x7FFFFF)
        nonMantissaBits = self.retrieveChildValues(exponent)
        mantissa = (mantissa_bits * (2 ** (exponent - 23))) + nonMantissaBits

        return sign * mantissa

    """ def toFloat(self) -> float:
        p = self.pfloat

        sign = -1 if p >> 31 else 1

        exponent = ((p & 0x7F800000) >> 23) - 127
        mantissa_bits = p & 0x7FFFFF
        nonMantissaBits = self.retrieveChildValues(exponent)
        mantissa = 1 + mantissa_bits / (1 << 23)
        
        intermed = mantissa * (2 ** exponent) + nonMantissaBits
        return sign * intermed """

    def retrieveChildValues(self, exponent) -> int:
        total = 0
        c = self.child
        exponent -= 23

        while c:
            val = c.value
            distance = c.distance
            exponent += distance - val.bit_length()
            total += val * (2**exponent)
            c = c.child
        return total

    def reverseBits(num) -> int:
        res = 0
        bitlen = len(bin(num)) - 2
        for i in range(bitlen):
            a = (num >> i) & 1
            res |= a << (bitlen - 1 - i)
        return res

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
        else:
            print("NO CHILD NODE")

    def verify(self):
        return struct.unpack("f", struct.pack("I", self.pfloat))[0]


class ChildNode:
    def __init__(self, value, distance):
        self.value = value
        self.distance = distance
        self.child = None
