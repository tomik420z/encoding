import numpy as np
from BitVector import BitVector
from util import modular_to_bit_vector

class AES():
    S_Box = np.array([['9', '4', 'a', 'b'], ['d', '1', '8', '5'], ['6', '2', '0', '3'], ['c', 'e', 'f', '7']])
    S_InvBox = np.array([['a', '5', '9', 'b'], ['1', '7', '8', 'f'], ['6', '0', '2', '3'], ['c', '4', 'd', 'e']])
    RCON1 = int('10000000', 2)
    RCON2 = int('00110000', 2)
    modulus = BitVector(bitstring='10011')
    column_Matrix = list([[0x1, 0x4], [0x4, 0x1]])
    column_InvMatrix = list([[0x9, 0x2], [0x2, 0x9]])
    state_matrix = []
    

    def set_modulus(self, number):
        self.modulus = modular_to_bit_vector(number)

    @staticmethod
    def gf_divide(a, b):
        # деление полинома на полином
        # результат: частное, остаток (полиномы)
        dividend = a # делимое
        divisor = b # делитель
        a = 0
        # бит в делимом
        m = len(bin(dividend))-2
        # бит в делителе
        n = len(bin(divisor))-2
        s = divisor << m
        msb = 2 ** (m + n - 1)
        for i in range(m):
            dividend <<= 1
            if dividend & msb > 0:
                dividend ^= s
                dividend ^= 1
        maskq = 2**m - 1
        maskr = 2**n - 1
        r = (dividend >> m) & maskr
        q = dividend & maskq
        return q, r
    

    @staticmethod
    def gf_mi(b, m, n):
        b_vec = BitVector(intVal=int(b))
        try:
            result = b_vec.gf_MI(m, n)
            return int(result)
        except:
            raise "Exception"
        

    @staticmethod
    def inverse_matrix_2x2(matrix : list[list[int]], m : int, n : int):
        """Находит обратную матрицу размерности 2x2 в поле GF(2^4)."""
        a, b = matrix[0]
        c, d = matrix[1]
        mod = BitVector(intVal=m)     
        
        # Находим детерминант
        det = AES.gf_multiply_modular(a, d, mod, n) ^ AES.gf_multiply_modular(b, c, mod, n)

        # Проверка на обратимость
        det_inv = AES.gf_mi(det, mod, n)

        # Вычисление элементов обратной матрицы
        a_inv = AES.gf_multiply_modular(
            d, det_inv, mod, n
        )
        
        b_inv = AES.gf_multiply_modular(
            AES.gf_multiply_modular(b, det_inv, mod, n) ^ (0b0), 1, mod, n
        )
        
        c_inv = AES.gf_multiply_modular(
            AES.gf_multiply_modular(c, det_inv, mod, n) ^ (0b0), 1, mod, n
        )
        
        d_inv = AES.gf_multiply_modular(
            a, det_inv, mod, n
        )

        return [[a_inv, b_inv], [c_inv, d_inv]]


    @staticmethod
    def matrix_multiply(mat_a, mat_b, mod, n):
        rows_a = len(mat_a)
        cols_a = len(mat_a[0])
        rows_b = len(mat_b)
        cols_b = len(mat_b[0])

        # Проверка на совместимость матриц
        if cols_a != rows_b:
            raise ValueError("Матрицы не могут быть перемножены")

        # Результирующая матрица
        result = [[0] * cols_b for _ in range(rows_a)]

        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result[i][j] ^= AES.gf_multiply_modular(mat_a[i][k], mat_b[k][j], mod, n)

        return result


    @staticmethod
    def divide_into_two(key, size):
        """
        Делит ключ на две равные части.

        :param key: Входной ключ в виде числа.
        :param size: Размер каждой части.
        :return: Две части ключа.
        """
        size = size // 2
        # Преобразуем число в двоичную строку
        key_bin = bin(key)[2:]  # Убираем '0b' в начале
        key_bin = key_bin.zfill(size * 2)  # Дополняем до нужной длины

        # Разделяем на две части
        w0_bin = key_bin[:size]
        w1_bin = key_bin[size:size * 2]

        # Преобразуем обратно в десятичные числа
        w0 = int(w0_bin, 2)
        w1 = int(w1_bin, 2)

        return w0, w1
    
    @staticmethod
    def mux(l, r, n):
        """
        Объединяет два n-битовых числа l и r в одно 2n-битовое число.
        :param l: Старшая часть (n бит).
        :param r: Младшая часть (n бит).
        :param n: Количество бит в каждой части.
        :return: Объединенное число (2n бит).
        """
        return (l << n) | r


    @staticmethod
    def gf_multiply_modular(a, b, modular, n):
        """
        INPUTS
        a - полином (множимое)
        b - полином (множитель)
        mod - неприводимый полином
        n - порядок неприводимого полинома
        OUTPUTS:
        product - результат перемножения двух полиномов a и b
        """
        a_vec = BitVector(intVal=int(a))
        b_vec = BitVector(intVal=int(b))

        return a_vec.gf_multiply_modular(b_vec, modular, n).int_val()


    def __init__(self, key):
        """
        раундовые ключи. рассчитываются в функции key_schedule
        """
        self.k0, self.k1, self.k2 = self.key_expansion(key)
 
 
    def sbox(self, v):
        """
        Замена 4-битового значения по таблице S_Box
        """
        r, c = AES.divide_into_two(v, 4)
        rez = self.S_Box[r, c]
        return int(rez, 16)
    

    def g(self, w, i):
        """
        g функция в алгоритме расширения ключа
        """
        n00, n11 = AES.divide_into_two(w, 8)
        n0 = self.sbox(n00)
        n1 = self.sbox(n11)
        n1n0 = AES.mux(n1, n0, 4)
        if i == 1:
            rez = n1n0 ^ self.RCON1
        else:
            rez = n1n0 ^ self.RCON2
        return rez


    def key_expansion(self, key):
        """
        Алгоритм расширения ключа
        """

        w0, w1 = AES.divide_into_two(key, 16)
        w2 = w0 ^ self.g(w1, 1)

        w3 = w1 ^ w2
        w4 = w2 ^ self.g(w3, 2)
        w5 = w3 ^ w4
        return key, AES.mux(w2, w3, 8), AES.mux(w4, w5, 8)
    
    
    def to_state_matrix(self, block):
        """
        Формирование матрицы состояния из 16-ти битового числа
        """
        b1, b2 = AES.divide_into_two(block, 16)
        b11, b12 = AES.divide_into_two(b1, 8)
        b21, b22 = AES.divide_into_two(b2, 8)
        self.state_matrix = [[b11, b21], [b12, b22]]


    def add_round_key(self, k):
        """
        Сложение с раундовым ключом (Add round key)
        """
        k1, k2 = AES.divide_into_two(k, 16)
        k11, k12 = AES.divide_into_two(k1, 8)
        k21, k22 = AES.divide_into_two(k2, 8)
        self.state_matrix[0][0] ^= k11
        self.state_matrix[1][0] ^= k12
        self.state_matrix[0][1] ^= k21
        self.state_matrix[1][1] ^= k22
    

    def nibble_substitution(self):
        """
        Замена элементов матрицы состояния S (Nibble Substitution)
        """
        self.state_matrix[0][0] = self.sbox(self.state_matrix[0][0])
        self.state_matrix[0][1] = self.sbox(self.state_matrix[0][1])
        self.state_matrix[1][0] = self.sbox(self.state_matrix[1][0])
        self.state_matrix[1][1] = self.sbox(self.state_matrix[1][1])
 
 
    def shift_row(self):
        """
        Перестановка элементов в матрице состояния S (Shift Row)
        """
        a = self.state_matrix[1][0]
        self.state_matrix[1][0] = self.state_matrix[1][1]
        self.state_matrix[1][1] = a
 
 
    def mix_columns(self):
        """
        Перемешивание элементов в столбцах матрицы S (Mix Columns)
        """
        m00 = self.column_Matrix[0][0]
        m01 = self.column_Matrix[0][1]
        m10 = self.column_Matrix[1][0]
        m11 = self.column_Matrix[1][1]

        st00 = self.state_matrix[0][0]
        st10 = self.state_matrix[1][0]
        a = AES.gf_multiply_modular(m00, st00, self.modulus, 4)
        b = AES.gf_multiply_modular(m01, st10, self.modulus, 4)

        c = AES.gf_multiply_modular(m10, st00, self.modulus, 4)
        d = AES.gf_multiply_modular(m11, st10, self.modulus, 4)
        self.state_matrix[0][0] = a ^ b
        self.state_matrix[1][0] = c ^ d
        st00 = self.state_matrix[0][1]
        st10 = self.state_matrix[1][1]
        a = AES.gf_multiply_modular(m00, st00, self.modulus, 4)
        b = AES.gf_multiply_modular(m01, st10, self.modulus, 4)
        c = AES.gf_multiply_modular(m10, st00, self.modulus, 4)
        d = AES.gf_multiply_modular(m11, st10, self.modulus, 4)
        self.state_matrix[0][1] = a ^ b
        self.state_matrix[1][1] = c ^ d


    def from_state_matrix(self):
        """
        Формирование 16-ти битового числа из матрицы состояния
        """
        b1 = AES.mux(self.state_matrix[0][0], self.state_matrix[1][0], 4)
        b2 = AES.mux(self.state_matrix[0][1], self.state_matrix[1][1], 4)
        return AES.mux(b1, b2, 8)
 
 
    def encrypt(self, plaintext):
        """
        Алгоритм шифрования блока с заданными раундовыми ключами
        """
        self.to_state_matrix(plaintext)
        
        self.add_round_key(self.k0)

        self.nibble_substitution()
        self.shift_row()
        self.mix_columns()
        self.add_round_key(self.k1)
        
        self.nibble_substitution()
        self.shift_row()
        self.add_round_key(self.k2)

        return self.from_state_matrix()
    

    def decrypt_data(self, data):
        """
        Расшифрование 16-битовых чисел в data на ключе key
        """
        decrypted_data = []

        for block in data:
            decrypted_block = self.decrypt(block)
            # print(block)
            decrypted_data.append(decrypted_block)

        return decrypted_data
    
    def inverse_shift_row(self):
        """
        Обратная перестановка элементов в матрице состояния S
        """
        a = self.state_matrix[1][0]
        self.state_matrix[1][0] = self.state_matrix[1][1]
        self.state_matrix[1][1] = a

    def inverse_nibble_substitution(self):
        """
        Обратная замена элементов матрицы состояния S
        """
        self.state_matrix[0][0] = self.sbox_inv(self.state_matrix[0][0])
        self.state_matrix[0][1] = self.sbox_inv(self.state_matrix[0][1])
        self.state_matrix[1][0] = self.sbox_inv(self.state_matrix[1][0])
        self.state_matrix[1][1] = self.sbox_inv(self.state_matrix[1][1])


    def inverse_mix_columns(self):
        """
        Перемешивание элементов в столбцах матрицы S (Mix Columns)
        """
        m00 = self.column_InvMatrix[0][0]
        m01 = self.column_InvMatrix[0][1]
        m10 = self.column_InvMatrix[1][0]
        m11 = self.column_InvMatrix[1][1]
        s00 = self.state_matrix[0][0]
        s01 = self.state_matrix[0][1]
        s10 = self.state_matrix[1][0]
        s11 = self.state_matrix[1][1]
        mult = lambda lhs, rhs: AES.gf_multiply_modular(lhs,  rhs, self.modulus, 4) 

        self.state_matrix[0][0] = mult(m00, s00) ^ mult(m01, s10)
        self.state_matrix[0][1] = mult(m00, s01) ^ mult(m01, s11)
        self.state_matrix[1][0] = mult(m10, s00) ^ mult(m11, s10)
        self.state_matrix[1][1] = mult(m10, s01) ^ mult(m11, s11)
 

    def decrypt(self, ciphertext):
        """
        Алгоритм расшифрования блока с заданными раундовыми ключами
        """
        self.to_state_matrix(ciphertext)

        # Раунд 0: Add Round Key с k2
        self.add_round_key(self.k2)

        # Раунд 1
        self.inverse_shift_row()
        self.inverse_nibble_substitution()
        self.add_round_key(self.k1)
        self.inverse_mix_columns()

        # Раунд 2
        self.inverse_shift_row()
        self.inverse_nibble_substitution()
        self.add_round_key(self.k0)

        # Возвращаем расшифрованный блок
        return self.from_state_matrix()


    def encrypt_data(self, data):
        """
        шифрование 8-битовых чисел в data на ключе key
        """
        encrypted_data = []

        for block in data:
            encrypted_block = self.encrypt(block)
            encrypted_data.append(encrypted_block)

        return encrypted_data
    

    def sbox_inv(self, v):
        """
        Обратная замена 4-битового значения по таблице S_InvBox
        """
        r, c = self.divide_into_two(v, 4)
        rez = self.S_InvBox[r, c]
        return int(rez, 16)

        
# class AES():

#     S_Box = [
#         0b1110,
#         0b0100,
#         0b1101,
#         0b0001,
#         0b0010,
#         0b1111,
#         0b1011,
#         0b1000,
#         0b0011,
#         0b1010,
#         0b0110,
#         0b1100,
#         0b0101,
#         0b1001,
#         0b0000,
#         0b0111,
#     ]

#     S_InvBox = [
#         0b1110,
#         0b0011,
#         0b0100,
#         0b1000,
#         0b0001,
#         0b1100,
#         0b1010,
#         0b1111,
#         0b0111,
#         0b1101,
#         0b1001,
#         0b0110,
#         0b1011,
#         0b0010,
#         0b0000,
#         0b0101,
#     ]


#     # S_Box = np.array([['9', '4', 'a', 'b'], ['d', '1', '8', '5'], ['6', '2', '0', '3'], ['c', 'e', 'f', '7']])
#     # S_InvBox = np.array([['a', '5', '9', 'b'], ['1', '7', '8', 'f'], ['6', '0', '2', '3'], ['c', '4', 'd', 'e']])
#     RCON1 = int('10000000', 2)
#     RCON2 = int('00110000', 2)
#     modulus = int('10011', 2)
#     column_Matrix = list([[0x1, 0x4], [0x4, 0x1]])
#     column_InvMatrix = list([[0x9, 0x2], [0x2, 0x9]])
#     state_matrix = []


#     @staticmethod
#     def divide_into_two(key, size):
#         """
#         Делит ключ на две равные части.

#         :param key: Входной ключ в виде числа.
#         :param size: Размер каждой части.
#         :return: Две части ключа.
#         """
#         size = size // 2
#         # Преобразуем число в двоичную строку
#         key_bin = bin(key)[2:]  # Убираем '0b' в начале
#         key_bin = key_bin.zfill(size * 2)  # Дополняем до нужной длины

#         # Разделяем на две части
#         w0_bin = key_bin[:size]
#         w1_bin = key_bin[size:size * 2]

#         # Преобразуем обратно в десятичные числа
#         w0 = int(w0_bin, 2)
#         w1 = int(w1_bin, 2)

#         return w0, w1
    

#     @staticmethod
#     def mux(l, r, n):
#         """
#         Объединяет два n-битовых числа l и r в одно 2n-битовое число.
#         :param l: Старшая часть (n бит).
#         :param r: Младшая часть (n бит).
#         :param n: Количество бит в каждой части.
#         :return: Объединенное число (2n бит).
#         """
#         return (l << n) | r


#     def __init__(self, key):
#         """
#         раундовые ключи. рассчитываются в функции key_schedule
#         """
#         self.k0, self.k1, self.k2 = self.key_expansion(key)

    
#     # @staticmethod
#     # def gf_multiply_modular(a, b, mod, n):
#     #     """
#     #     INPUTS
#     #     a - полином (множимое)
#     #     b - полином (множитель)
#     #     mod - неприводимый полином
#     #     n - порядок неприводимого полинома
#     #     OUTPUTS:
#     #     product - результат перемножения двух полиномов a и b
#     #     """
#     #     product = 0  # Начальное значение произведения

#     #     # Пока b не равно нулю
#     #     while b > 0:
#     #         # Если младший бит b равен 1, добавляем a к продукту
#     #         if b & 1:
#     #             product ^= a  # XOR для сложения в GF(2)

#     #         # Сдвигаем b вправо на 1 (делим на 2)
#     #         b >>= 1

#     #         # Умножаем a на 2 (сдвигаем влево на 1)
#     #         a <<= 1

#     #         # Если a превышает степень n, то выполняем модульное деление
#     #         if a >= (1 << n):  # Проверяем, превышает ли a модульный полином
#     #             a ^= mod  # Выполняем XOR с модульным полином

#     #     return product


#     @staticmethod
#     def gf_multiply_modular(a, b, mod, n):
#         """
#         INPUTS
#         a - полином (множимое)
#         b - полином (множитель)
#         mod - неприводимый полином
#         n - порядок неприводимого полинома
#         OUTPUTS:
#         product - результат перемножения двух полиномов a и b
#         """
#         a_vec = BitVector(intVal=int(a))
#         b_vec = BitVector(intVal=int(b))

#         return a_vec.gf_multiply_modular(b_vec, BitVector(bitstring=format(mod, '04b')), n).int_val()
        
#         # # маска для наиболее значимого бита в слове
#         # msb = 2**(n - 1)
#         # # маска на все биты
#         # mask = 2**n - 1
#         # # r(x) = x^n mod m(x)
#         # r = mod ^ (2**n)
#         # product = 0 # результат умножения
#         # mm = 1
#         # for i in range(n):
#         #     if b & mm > 0:
#         #         # если у множителя текущий бит 1
#         #         product ^= a
#         #     # выполняем последовательное умножение на х
#         #     if a & msb == 0:
#         #         # если старший бит 0, то просто сдвигаем на 1 бит
#         #         a <<= 1
#         #     else:
#         #         # если старший бит 1, то сдвиг на 1 бит
#         #         a <<= 1
#         #         # и сложение по модулю 2 с r(x)
#         #         a ^= r
#         #         # берем только n бит
#         #         a &= mask
#         #     # формируем маску для получения очередного бита в множителе
#         #     mm += mm
#         # return product
    

#     @staticmethod
#     def matrix_multiply(mat_a, mat_b, mod, n):
#         rows_a = len(mat_a)
#         cols_a = len(mat_a[0])
#         rows_b = len(mat_b)
#         cols_b = len(mat_b[0])

#         # Проверка на совместимость матриц
#         if cols_a != rows_b:
#             raise ValueError("Матрицы не могут быть перемножены")

#         # Результирующая матрица
#         result = [[0] * cols_b for _ in range(rows_a)]

#         for i in range(rows_a):
#             for j in range(cols_b):
#                 for k in range(cols_a):
#                     result[i][j] ^= AES.gf_multiply_modular(mat_a[i][k], mat_b[k][j], mod, n)

#         return result


#     def sbox(self, v):
#         """
#         Замена 4-битового значения по таблице S_Box
#         """
#         # r, c = AES.divide_into_two(v, 4)
#         # rez = self.S_Box[r, c]
#         rez = self.S_Box[v]
#         return rez
    

#     def g(self, w, i):
#         """
#         g функция в алгоритме расширения ключа
#         """
#         n00, n11 = AES.divide_into_two(w, 8)
#         n0 = self.sbox(n00)
#         n1 = self.sbox(n11)
#         n1n0 = AES.mux(n1, n0, 4)
#         if i == 1:
#             rez = n1n0 ^ self.RCON1
#         else:
#             rez = n1n0 ^ self.RCON2
#         return rez
    
    
#     def glue(self, w0, w1, w2, w3):
#         return AES.mux(AES.mux(w0, w1, 4), AES.mux(w2, w3, 4), 8)

#     def key_expansion(self, key):
#         """
#         Алгоритм расширения ключа
#         """
#         W0, W1 = AES.divide_into_two(key, 16)
#         w0, w1 = AES.divide_into_two(W0, 8)
#         w2, w3 = AES.divide_into_two(W1, 8)

        
#         k0 = self.glue(w0, w1, w2, w3)
        
#         w4 = w0 ^ self.S_Box[w3] ^ 0b0001
#         w5 = w1 ^ w4
#         w6 = w2 ^ w5 
#         w7 = w3 ^ w6
#         k1 = self.glue(w4, w5, w6, w7)

#         w8 = w4 ^ self.S_Box[w7] ^ 0b0010
#         w9 = w5 ^ w8
#         w10 = w6 ^ w9
#         w11 = w7 ^ w10 
#         k2 = self.glue(w8, w9, w10, w11)

#         return k0, k1, k2
    
 
#     def to_state_matrix(self, block):
#         """
#         Формирование матрицы состояния из 16-ти битового числа
#         """
#         b1, b2 = AES.divide_into_two(block, 16)
#         b11, b12 = AES.divide_into_two(b1, 8)
#         b21, b22 = AES.divide_into_two(b2, 8)
#         self.state_matrix = [[b11, b21], 
#                              [b12, b22]
#                             ]
 
 
#     def add_round_key(self, k):
#         """
#         Сложение с раундовым ключом (Add round key)
#         """
#         k1, k2 = AES.divide_into_two(k, 16)
#         k11, k12 = AES.divide_into_two(k1, 8)
#         k21, k22 = AES.divide_into_two(k2, 8)
#         self.state_matrix[0][0] ^= k11
#         self.state_matrix[1][0] ^= k12
#         self.state_matrix[0][1] ^= k21
#         self.state_matrix[1][1] ^= k22


#     def nibble_substitution(self):
#         """
#         Замена элементов матрицы состояния S (Nibble Substitution)
#         """
#         self.state_matrix[0][0] = self.sbox(self.state_matrix[0][0])
#         self.state_matrix[0][1] = self.sbox(self.state_matrix[0][1])
#         self.state_matrix[1][0] = self.sbox(self.state_matrix[1][0])
#         self.state_matrix[1][1] = self.sbox(self.state_matrix[1][1])
 
 
#     def shift_row(self):
#         """
#         Перестановка элементов в матрице состояния S (Shift Row)
#         """
#         a = self.state_matrix[1][0]
#         self.state_matrix[1][0] = self.state_matrix[1][1]
#         self.state_matrix[1][1] = a

        
#     def mix_columns(self):
#         """
#         Перемешивание элементов в столбцах матрицы S (Mix Columns)
#         """
#         m00 = self.column_Matrix[0][0]
#         m01 = self.column_Matrix[0][1]
#         m10 = self.column_Matrix[1][0]
#         m11 = self.column_Matrix[1][1]
#         s00 = self.state_matrix[0][0]
#         s01 = self.state_matrix[0][1]
#         s10 = self.state_matrix[1][0]
#         s11 = self.state_matrix[1][1]
#         mult = lambda lhs, rhs: AES.gf_multiply_modular(lhs,  rhs, self.modulus, 4) 

#         self.state_matrix[0][0] = mult(m00, s00) ^ mult(m01, s10)
#         self.state_matrix[0][1] = mult(m00, s01) ^ mult(m01, s11)
#         self.state_matrix[1][0] = mult(m10, s00) ^ mult(m11, s10)
#         self.state_matrix[1][1] = mult(m10, s01) ^ mult(m11, s11)
        
    
#     def from_state_matrix(self):
#         """
#         Формирование 16-ти битового числа из матрицы состояния
#         """
#         b1 = AES.mux(self.state_matrix[0][0], self.state_matrix[1][0], 4)
#         b2 = AES.mux(self.state_matrix[0][1], self.state_matrix[1][1], 4)
#         return AES.mux(b1, b2, 8)
 

#     def encrypt(self, plaintext):
#         """
#         Алгоритм шифрования блока с заданными раундовыми ключами
#         """
#         self.to_state_matrix(plaintext)

#         # Раунд 0: Add Round Key с k0
#         self.add_round_key(self.k0)

#         # Раунд 1
#         self.nibble_substitution()
#         self.shift_row()
#         self.mix_columns()
#         self.add_round_key(self.k1)

#         # Раунд 2
#         self.nibble_substitution()
#         self.shift_row()
#         self.add_round_key(self.k2)

#         # Возвращаем зашифрованный блок
#         return self.from_state_matrix()


#     def decrypt(self, ciphertext):
#         # Преобразуем блок в матрицу состояния
#         self.to_state_matrix(ciphertext)

#         # Раунд 0: Add Round Key с k2
#         self.add_round_key(self.k2)

#         # Раунд 1
#         self.inverse_shift_row()
#         self.inverse_nibble_substitution()
#         self.add_round_key(self.k1)
#         self.inverse_mix_columns()

#         # Раунд 2
#         self.inverse_shift_row()
#         self.inverse_nibble_substitution()
#         self.add_round_key(self.k0)

#         # Возвращаем расшифрованный блок
#         return self.from_state_matrix()


#     def encrypt_data(self, data):
#         """
#         Шифрование 16-битовых чисел в data на ключе key
#         """
#         encrypted_data = []

#         for block in data:
#             encrypted_block = self.encrypt(block)
#             encrypted_data.append(encrypted_block)

#         return encrypted_data


#     def decrypt_data(self, data):
#         """
#         Расшифрование 16-битовых чисел в data на ключе key
#         """
#         decrypted_data = []

#         for block in data:
#             decrypted_block = self.decrypt(block)
#             # print(block)
#             decrypted_data.append(decrypted_block)

#         return decrypted_data


#     def inverse_nibble_substitution(self):
#         """
#         Обратная замена элементов матрицы состояния S
#         """
#         self.state_matrix[0][0] = self.sbox_inv(self.state_matrix[0][0])
#         self.state_matrix[0][1] = self.sbox_inv(self.state_matrix[0][1])
#         self.state_matrix[1][0] = self.sbox_inv(self.state_matrix[1][0])
#         self.state_matrix[1][1] = self.sbox_inv(self.state_matrix[1][1])


#     def sbox_inv(self, v):
#         """
#         Обратная замена 4-битового значения по таблице S_InvBox
#         """
#         # r, c = self.divide_into_two(v, 4)
#         rez = self.S_InvBox[v]
#         return int(rez)


#     def inverse_mix_columns(self):
#         """
#         Перемешивание элементов в столбцах матрицы S (Mix Columns)
#         """
#         m00 = self.column_InvMatrix[0][0]
#         m01 = self.column_InvMatrix[0][1]
#         m10 = self.column_InvMatrix[1][0]
#         m11 = self.column_InvMatrix[1][1]
#         s00 = self.state_matrix[0][0]
#         s01 = self.state_matrix[0][1]
#         s10 = self.state_matrix[1][0]
#         s11 = self.state_matrix[1][1]
#         mult = lambda lhs, rhs: AES.gf_multiply_modular(lhs,  rhs, self.modulus, 4) 

#         self.state_matrix[0][0] = mult(m00, s00) ^ mult(m01, s10)
#         self.state_matrix[0][1] = mult(m00, s01) ^ mult(m01, s11)
#         self.state_matrix[1][0] = mult(m10, s00) ^ mult(m11, s10)
#         self.state_matrix[1][1] = mult(m10, s01) ^ mult(m11, s11)


#     def inverse_shift_row(self):
#         """
#         Обратная перестановка элементов в матрице состояния S
#         """
#         a = self.state_matrix[1][0]
#         self.state_matrix[1][0] = self.state_matrix[1][1]
#         self.state_matrix[1][1] = a

#     @staticmethod
#     def gf_divide(a, b):
#         # деление полинома на полином
#         # результат: частное, остаток (полиномы)
#         dividend = a # делимое
#         divisor = b # делитель
#         a = 0
#         # бит в делимом
#         m = len(bin(dividend))-2
#         # бит в делителе
#         n = len(bin(divisor))-2
#         s = divisor << m
#         msb = 2 ** (m + n - 1)
#         for i in range(m):
#             dividend <<= 1
#             if dividend & msb > 0:
#                 dividend ^= s
#                 dividend ^= 1
#         maskq = 2**m - 1
#         maskr = 2**n - 1
#         r = (dividend >> m) & maskr
#         q = dividend & maskq
#         return q, r


#     @staticmethod
#     def gf_mi(b, m, n):
#         b_vec = BitVector(intVal=int(b))
#         return b_vec.gf_MI(BitVector(bitstring=format(m, '04b')), n)

#         # """Находит обратный элемент x в GF(2^4) по модулю m."""
#         # a1, a2, a3 = 1, 0, m
#         # b1, b2, b3 = 0, 1, b
        
#         # while b3 != 1:
#         #     q, r = AES.gf_divide(a3, b3)
#         #     t1, t2, t3 = a1 + AES.gf_multiply_modular(q, b1, m, n), a2 + AES.gf_multiply_modular(q, b2, m, n), r
#         #     a1, a2, a3 = b1, b2, b3
#         #     b1, b2, b3 = t1, t2, t3
#         # return b2
    

#     @staticmethod
#     def inverse_matrix_2x2(matrix, m, n):
        
#         # for k1 in range(16):
#         #     for k2 in range(16):
#         #         for k3 in range(16):
#         #             for k4 in range(16):
#         #                 inv_matrix = [
#         #                     [k1, k2],
#         #                     [k3, k4]
#         #                 ]
#         #                 if AES.matrix_multiply(matrix, inv_matrix, m, n) == [[1, 0],[0, 1]]:
#         #                     return inv_matrix
        
#         # return [[0, 0], [0, 0]]

#         """Находит обратную матрицу размерности 2x2 в поле GF(2^4)."""
#         a, b = matrix[0]
#         c, d = matrix[1]
        
#         # Находим детерминант
#         det = AES.gf_multiply_modular(a, d, m, n) ^ AES.gf_multiply_modular(b, c, m, n)

#         # Проверка на обратимость
#         det_inv = AES.gf_mi(det, m, n)

#         # Вычисление элементов обратной матрицы
#         a_inv = AES.gf_multiply_modular(
#             d, det_inv, m, n
#         )
        
#         b_inv = AES.gf_multiply_modular(
#             AES.gf_multiply_modular(b, det_inv, m, n) ^ (0b0), 1, m, n
#         )
        
#         c_inv = AES.gf_multiply_modular(
#             AES.gf_multiply_modular(c, det_inv, m, n) ^ (0b0), 1, m, n
#         )
        
#         d_inv = AES.gf_multiply_modular(
#             a, det_inv, m, n
#         )

#         return [[a_inv, b_inv], [c_inv, d_inv]]

