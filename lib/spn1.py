__author__ = 'рс'


from math import ceil
###############
# SPN1
###############

# Prints out its argument in binary
def binary(x, k):
    y = binary1(x)
    if len(y) < k:
        return "0"*(k-len(y))+y
    return y


def binary1(x):
    if x != 0:
        y = binary1(x >> 1) + str(x&1)
        if y == "":
            return "0"
        else:
            return y
    else:
        return ""


class SPN1():
# полная реализация: шифрование, расшифрование плюс режимы шифрования
    #p-box
    p = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    #S-box
    s = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]


    #construct inverse S-box
    s2 = []
    for i in range(len(s)):
        s2.append(0)
    for i in range(len(s)):
        s2[s[i]] = i


    def __init__(self, s, p):
        """
        раундовые ключи. рассчитываются в функции key_schedule
        """
        self.s = s
        self.p = p

        for i in range(len(self.s)):
            self.s2.append(0)
        for i in range(len(self.s)):
            self.s2[self.s[i]] = i


    # печатаем таблицу замен и таблицу перестановок
    def print_s_p(self):
        print('s={}'.format(self.s))
        print('p={}'.format(self.p))


    # s-box application (forward direction)
    def sbox(self, x):
        return self.s[x]


    #s-box application (backward direction)
    def asbox(self, x):
        return self.s2[x]


    #p-box application (forward direction)
    def pbox(self, x):
        #use longs
        y = 0
        for i in range(len(self.p)):
            if (x & (1 << i)) != 0:
                y ^= (1 << self.p[i])
        return y


    #p-box application (backward direction)
    def apbox(self, x):
        #use longs
        y = 0

        for i in range(len(self.p)):

            if (x & (1 << self.p[i])) != 0:
                y ^= (1 << i)
        
        return y


    #break into 6-bit chunks
    def demux(self, x):
        y = []
        for i in range(0, 4):
            y.append((x >> (i*4)) & 0xf)
        return y


    #convert back into 36-bit state
    def mux(self, x):
        y = 0
        for i in range(0, 4):
            y ^= (x[i] << (i*4))
        return y


    def round_keys(self, k):
        rk = []
        rk.append((k >> 16) & (2**16-1))
        rk.append((k >> 12) & (2**16-1))
        rk.append((k >> 8) & (2**16-1))
        rk.append((k >> 4) & (2**16-1))
        rk.append(k & (2**16-1))
        return rk


    # Key mixing
    def mix(self, p, k):
        v = p ^ k
        return v


    #round function
    def round(self, p, k):

        #XOR key
        u = self.mix(p, k)
        v = []
        # run through substitution layer
        for x in self.demux(u):
            v.append(self.sbox(x))
        w = self.pbox(self.mux(v))
        return w


    def last_round(self, p, k1, k2):
        #XOR key
        u = self.mix(p, k1)
        v = []
        # run through substitution layer
        for x in self.demux(u):
            v.append(self.sbox(x))
        #XOR key
        u = self.mix(self.mux(v), k2)
        return u


    #inverse round operation
    def inv_round(self, p, k):
        #XOR key
        u = self.mix(p, k)
        v = []
        # run through substitution layer
        for x in self.demux(u):
            v.append(self.asbox(x))
        # run through permutation layer
        w = self.apbox(self.mux(v))
        return w


    def inv_last_round(self, p, k1, k2):
        #XOR key
        u = self.mix(p, k1)
        v = []
        # run through substitution layer
        for x in self.demux(u):
            v.append(self.asbox(x))
        #XOR key
        u = self.mix(self.mux(v), k2)
        return u


    # Шифруем одно число
    def encrypt(self, p, rk, rounds):
        x = p
        for i in range(rounds-1):
            x = self.round(x, rk[i])
        x = self.last_round(x, rk[rounds-1], rk[rounds])
        return x


    # Шифруем массив чисел
    def encrypt_data(self, data, key, rounds):
        rk = self.round_keys(key)
        cypher_data = []
        for m in data:
            c = self.encrypt(m, rk, rounds)
            cypher_data.append(c)
        return cypher_data


    def round_keys_to_decrypt(self, k):
        rk = self.round_keys(k)
        n = len(rk)
        rkd = [rk[n-1]]
        for i in range(1, n-1):
            rkd.append(self.apbox(rk[n-1-i]))
        rkd.append(rk[0])
        return rkd


    def decrypt(self, x, key1, rounds):
        for i in range(rounds-1):
            # print('decrypt: round {}'.format(i+1))
            x = self.inv_round(x, key1[i])
        x = self.inv_last_round(x, key1[rounds-1], key1[rounds])
        return x


    # Расшифровываем массив чисел
    def decrypt_data(self, data, key, rounds):
        rk = self.round_keys_to_decrypt(key)
        cypher_data = []
        for m in data:
            c = self.decrypt(m, rk, rounds)
            cypher_data.append(c)
        return cypher_data
