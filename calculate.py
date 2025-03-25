from array import array
import struct

""" class TestMethods:
    def one():
        a = PFloat(7) """


class PFloat:

    def __init__(self, num: int = 0):
        # Create 32-bit integer representation of given integer
        num, sign = self.getSign(num)
        msb = num.bit_length() - 1
        exponent = msb + 127
        dist_from_mpos = 23 - msb
        shifted = num << dist_from_mpos if dist_from_mpos >= 0 else num >> (-1 * dist_from_mpos)
        mantissa = shifted & 0x7FFFFF # 11111111111111111111111; len 23
        #print("mantissa: " + bin(mantissa)[2:])
        self.pfloat = (sign << 31) | exponent << 23 | mantissa
        #print("float: " + bin(self.pfloat)[2:])

    def verify(self):
        float_value = struct.unpack('f', struct.pack('I', self.pfloat))[0]
        return int(float_value)
    
    def toInt(self):
        sign = self.pfloat & (1 << 31)
        mantissa = self.pfloat & 0x7FFFFF | 1 << 23
        exponent = (self.pfloat & 0x7F800000) >> 23
        if (23 - (exponent - 127) >= 0):
            original = mantissa >> 23 - (exponent - 127)
        else:
            original = mantissa << (exponent - 127) - 23
        #original = 1 << (corrected_mantissa.bit_length()) | corrected_mantissa
        #print(bin(original))
        #print(original)
        return original * (-1 if sign else 1)
    
    def getSign(self, num: int):
        if num > 0:
            return num, 0
        return -1 * num, 1

#t = 8388607 full 23 1s
# 170141163178059628080016879768632819712

def main():
    new = PFloat(1)
    print(new.toInt())

if __name__ == "__main__":
    main()