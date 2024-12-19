import unittest
import random
from lib.local_path import SRC_DECRYPTED_
from lib.local_path import SRC_ENCRYPTED_
import lib.read_write_file as io
from lib.util import numeric_matrix_to_str_mx
from lib.util import modular_to_bit_vector
from lib.saes import AES

class TestAES(unittest.TestCase):


    '''
    Тест из статьи https://piazza.com/class_profile/get_resource/ixlc30gojpe5fs/iyv0273azwtz4
    '''
    # def test_state_mx(self):
    #     key = 0b1100001111110000
    #     block = 0b1001110001100011
    #     aes = AES(key)
        
    #     matrix2x2 = [
    #         [0b0011, 0b0010],
    #         [0b0010, 0b0011],
    #     ]   
    #     aes.column_Matrix = numeric_matrix_to_str_mx(matrix2x2)

    #     #step0
    #     aes.to_state_matrix(block)
    #     aes.add_round_key(aes.k0)
    #     self.assertEqual(aes.from_state_matrix(), 0b0101111110010011)
    #     #step1
    #     aes.nibble_substitution()
    #     self.assertEqual(aes.from_state_matrix(), 0b1111011110100001)        
    #     aes.shift_row()
    #     self.assertEqual(aes.from_state_matrix(), 0b1111000110100111)
    #     aes.mix_columns()
    #     self.assertEqual(aes.from_state_matrix(), 0b0000111000111110)
    #     aes.add_round_key(aes.k1)
    #     self.assertEqual(aes.from_state_matrix(), 0b0011111011000001)
    #     #step2
    #     aes.nibble_substitution()
    #     self.assertEqual(aes.from_state_matrix(), 0b0001000001010100)
    #     aes.shift_row()
    #     self.assertEqual(aes.from_state_matrix(), 0b0001010001010000)
    #     aes.add_round_key(aes.k2)
    #     self.assertEqual(aes.from_state_matrix(), 0b0111001011000110)

    #     self.assertEqual(aes.encrypt(0b1001110001100011), 0b0111001011000110)

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

        # Шифрование блока данных
        ciphertext = aes.encrypt(plaintext)
        
        self.assertEqual(ciphertext, 0b0000011100111000)

        # Проверка матрицы состояния
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
        inv_a = AES.gf_mi(a, modular_to_bit_vector(m), n)
        self.assertEqual(inv_a, 0b1110)
        product = AES.gf_multiply_modular(a, inv_a, modular_to_bit_vector(m), n)
        self.assertEqual(product, 1)

    def test_inverse_matrix(self):

        n = 4
        m = 0b10011
        list_matrix = [
            [[0xB, 0x4],[0xE, 0xD]],
            [[0x1, 0x4],[0x4, 0x1]],
            [[0xa, 0xc],[0x8, 0x6]],
            [[0x5, 0x3],[0x2, 0xc]],
            [[0x3, 0x8],[0x2, 0xb]],
        ]

        for mx in list_matrix:
            inv_mx = AES.inverse_matrix_2x2(mx, m, n)
            self.assertEqual(AES.matrix_multiply(mx, inv_mx, modular_to_bit_vector(m), n), [[1, 0],[0, 1]])
        

    def test_multiply_polynoms(self):
        n = 4
        m = 0b10011
        for i in range(1, 16):
            inv = AES.gf_mi(i, modular_to_bit_vector(m), n)
            self.assertEqual(AES.gf_multiply_modular(i, inv, modular_to_bit_vector(m), n), 1, f"default number = {i} inv number = {inv}")


    def test_encr_image(self):
        decrypted_data = io.read_data_2byte(SRC_DECRYPTED_('dd1_saes_c_out.bmp'))
        key = 834
        MATRIX_2x2 = [[0x1, 0x4],[0x4, 0x1]]
        mod = 0b10011
        n = 4
        
        aes = AES(key)
        aes.column_Matrix = MATRIX_2x2
        aes.column_InvMatrix = AES.inverse_matrix_2x2(MATRIX_2x2, mod, n)
        ed = aes.encrypt_data(decrypted_data[:3])
        self.assertEqual(ed[:3], [12850, 32719, 40703])


    def test_reciprocal(self):
        key = 2318
        MATRIX_2x2 = [
            [0xB, 0x4],
            [0xE, 0xD],
        ]
        mod = 0b10011
        n = 4
        aes = AES(key)
        aes.column_Matrix = numeric_matrix_to_str_mx(MATRIX_2x2)
        aes.column_InvMatrix = numeric_matrix_to_str_mx(AES.inverse_matrix_2x2(MATRIX_2x2, mod, n))
        print(aes.column_Matrix, aes.column_InvMatrix)
        plaintext = int('0110111101101011', 2)
        encrypted = aes.encrypt(plaintext)
        text = aes.decrypt(encrypted)
        self.assertEqual(plaintext, text, f"{format(plaintext, '016b')}, {format(text, '016b')}")

    
    def test_encryptional(self):
        key = 2318
        MATRIX_2x2 = [
            [0xB, 0x4],
            [0xE, 0xD],
        ]
        
        mod = 0b10011
        n = 4

        decrypted_data = io.read_data_2byte(SRC_DECRYPTED_('im43.bmp'))
        
        aes = AES(key)
        aes.column_Matrix = MATRIX_2x2
        aes.column_InvMatrix = AES.inverse_matrix_2x2(MATRIX_2x2, mod, n)
        ed = aes.encrypt_data(decrypted_data[:10])
         
        self.assertEqual(ed, [25945, 48673, 27761, 7282, 7282, 8780, 7282, 20778, 7282, 12469])


if __name__ == '__main__':
    unittest.main()