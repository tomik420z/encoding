import unittest
from saes import AES

class TestAES(unittest.TestCase):
    
    def test_matrix(self):
        key = 0b1010011100111011
        aes = AES(key)

        self.assertEqual(aes.k0, 0b1010011100111011)
        self.assertEqual(aes.k1, 0b0001110000100111)
        self.assertEqual(aes.k2, 0b0111011001010001)

        aes.to_state_matrix(0b0110111101101011)
        self.assertEqual(aes.state_matrix, [[0x6, 0x6], [0xf, 0xb]])
        
        aes.add_round_key(key)
        self.assertEqual(aes.state_matrix, [[0xc, 0x5], [0x8, 0x0]])

        aes.nibble_substitution()
        self.assertEqual(aes.state_matrix, [[0xc, 0x1], [0x6, 0x9]])

        aes.shift_row()
        self.assertEqual(aes.state_matrix,[[0xc,0x1],[0x9, 0x6]])

        aes.mix_columns()
        self.assertEqual(aes.state_matrix, [[0xe,0xa],[0xc, 0x2]])
        

    def test_encrypt(self):
        key = int('1010011100111011', 2)
        aes = AES(key)

        # Блок данных P = 0110111101101011
        plaintext = int('0110111101101011', 2)

        print("Исходный блок данных (plaintext):", bin(plaintext))
        print("Ключи расширения:")

        print(f"k0: {format(aes.k0, '016b')}")
        print(f"k1: {format(aes.k1, '016b')}")
        print(f"k2: {format(aes.k2, '016b')}")

        # Шифрование блока данных
        print("\nШифрование:")
        ciphertext = aes.encrypt(plaintext)
        
        self.assertEqual(ciphertext, 0b0000011100111000)

        print("Зашифрованный блок данных (ciphertext):", format(ciphertext, '016b'))

        # Проверка матрицы состояния
        aes.to_state_matrix(ciphertext)
        self.assertEqual(aes.state_matrix, [[0x0, 0x3],[0x7, 0x8]])


    def test_decrypt(self):
        key = int('1010011100111011', 2)
        aes = AES(key)

        # Блок данных P = 0110111101101011
        plaintext = int('0110111101101011', 2)
        ciphertext = aes.encrypt(plaintext)
        
        self.assertEqual(ciphertext, 0b0000011100111000)
        # Проверка матрицы состояния
        aes.to_state_matrix(ciphertext)
        self.assertEqual(aes.state_matrix, [[0x0, 0x3],[0x7, 0x8]])
        self.assertEqual(aes.decrypt(ciphertext), plaintext)


    def test_multiply_polynom(self):
        n = 4
        a = 0b11
        m = 0b10011
        inv_a = AES.gf_mi(a, m, n)
        self.assertEqual(inv_a, 0b1110)
        product = AES.gf_multiply_modular(a, inv_a, m, n)
        self.assertEqual(product, 1)

    def test_inverse_matrix(self):
        n = 4
        mx = [
            [1, 4], 
            [4, 1],
        ]
        m = 0b10011
        inv_mx = AES.inverse_matrix_2x2(mx, m, n)
        self.assertEqual(inv_mx, [[9, 2],[2, 9]])




if __name__ == '__main__':
    unittest.main()