import math
import sys
import random

class ECC:
    def __init__(self, a=10, p=997, g=(5, 1), private_key=15):
        self.a = a
        self.p = p
        self.g = g
        self.valid_points = self.__get_all_valid_points_generated(a, p, g)

        self.private_key = private_key
        self.public_key = self.__get_public_key_from_private_key(private_key=private_key, n=len(self.valid_points), g=g, a=a, p=p)

    def __convert_int_to_binary(self, a):
        return "{0:b}".format(a)

    def __modular_inverse(self, a, b):
        for i in range(b):
            if (a * i) % b == 1:
                return i
        return None

    ''' @:param point1
        point1: a tuple which indicates a point
        @:param a
        a: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
        @:param p
        p: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
    '''
    def __ecc_double(self, point, a, p):
        x1, y1 = point[0], point[1]
        slope = ((((3 * math.pow(x1, 2)) + a) % p) * (self.__modular_inverse((2 * y1), p))) % p
        x2 = (math.pow(slope, 2) - (2 * x1)) % p
        y2 = ((y1 + (slope * (x2 - x1))) * -1) % p
        return x2, y2

    ''' @:param point1
        point1: a tuple which indicates a point
        @:param point2
        point2: a tuple which indicates a point
        @:param p
        p: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
    '''
    def __ecc_add(self, point1, point2, p):
        x1, y1, x2, y2 = point1[0], point1[1], point2[0], point2[1]
        slope = (((y2 - y1) % p) * self.__modular_inverse((x2 - x1), p)) % p
        x3 = (math.pow(slope, 2) - x2 - x1) % p
        y3 = (((slope * (x1 - x3)) % p) - (y1 % p)) % p
        return x3, y3

    ''' @:param point
        point: a tuple which indicates a point
        @:param constant
        constant: an integer
        @:param a
        a: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
        @:param p
        p: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
    '''
    def __ecc_scalar_multiple(self, point, constant, a, p):
        constant_binary = self.__convert_int_to_binary(constant)
        doubling_result = point
        resulting_point = None
        if constant_binary[len(constant_binary) - 1] == "1":
            resulting_point = point
        for i in range(len(constant_binary) - 2, -1, -1):
            doubling_result = self.__ecc_double(point=doubling_result, a=a, p=p)
            if constant_binary[i] == "1":
                if resulting_point is None:
                    resulting_point = doubling_result
                else:
                    resulting_point = self.__ecc_add(point1=resulting_point, point2=doubling_result, p=p)
        return resulting_point

    ''' @:param original_point
        original_point: a tuple which indicates the point to be encrypted
        @:param public_key
        public_key: a tuple which indicates the public key
        @:param n
        n: an integer which indicates number of all valid points generated, including the generator point and the infinity
        @:param g
        g: a tuple which indicates the generator point
        @:param a
        a: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
        @:param p
        p: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
    '''
    def __ecc_elgamal_encrypt(self, original_point, public_key, n, g, a, p):
        r = random.randint(1, n - 1)
        c1 = self.__ecc_scalar_multiple(point=g, constant=r, a=a, p=p)
        c1 = int(c1[0]), int(c1[1])
        temp = self.__ecc_scalar_multiple(point=public_key, constant=r, a=a, p=p)
        c2 = self.__ecc_add(point1=temp, point2=original_point, p=p)
        c2 = int(c2[0]), int(c2[1])
        return c1, c2

    ''' @:param encrypted_point
        encrypted_point: a tuple which indicates point to be decrypted
        @:param private_key
        private_key: an integer which indicates the private key
        @:param a
        a: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
        @:param p
        p: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
    '''
    def __ecc_elgamal_decrypt(self, encrypted_point, private_key, a, p):
        c1, c2 = encrypted_point[0], encrypted_point[1]
        temp = self.__ecc_scalar_multiple(point=c1, constant=private_key, a=a, p=p)
        temp = temp[0], -temp[1]
        c3 = self.__ecc_add(point1=c2, point2=temp, p=p)
        c3 = int(c3[0]), int(c3[1])
        return c3

    ''' @:param a
        a: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
        @:param p
        p: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
        @:param g
        g: a tuple which indicates the generator point
    '''
    def __get_all_valid_points_generated(self, a, p, g):
        valid_points = [g]
        while True:
            last_point = valid_points[len(valid_points) - 1]
            try:
                if last_point == g:
                    next_point = self.__ecc_double(last_point, a, p)
                else:
                    next_point = self.__ecc_add(last_point, g, p)
                valid_points.append(next_point)
            except:
                valid_points.append((sys.maxsize, sys.maxsize))
                break
        return valid_points

    ''' @:param private_key
        private_key: an integer in range between [1, n - 1] inclusive
        @:param n
        n: an integer which indicates number of all valid points generated, including the generator point and the infinity
        @:param g
        g: a tuple which indicates the generator point
        @:param a
        a: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
        @:param p
        p: an integer which represent y^2 congruent to x^3 + ax + b (mod p)
    '''
    def __get_public_key_from_private_key(self, private_key, n, g, a, p):
        if 1 <= private_key <= n - 1:
            return self.__ecc_scalar_multiple(point=g, constant=private_key, a=a, p=p)
        raise Exception("Unable to generate public key")

    def encrypt(self, original_point):
        return self.__ecc_elgamal_encrypt(
            original_point=original_point,
            public_key=self.public_key,
            n=len(self.valid_points),
            g=self.g,
            a=self.a,
            p=self.p
        )

    def decrypt(self, encrypted_point):
        return self.__ecc_elgamal_decrypt(
            encrypted_point=encrypted_point,
            private_key=self.private_key,
            a=self.a,
            p=self.p
        )

if __name__ == "__main__":
    ecc = ECC()
    point_1 = (11,99)
    print(point_1)
    point_2 = ecc.encrypt(point_1)
    print(point_2)
    point_3 = ecc.decrypt(point_2)
    print(point_3)