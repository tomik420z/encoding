'''
2. Расшифровать файл im43_saes_c_all.bmp – зашифрованное шифром
S_AES изображение в формате bmp. Матрица для преобразования
MixColumns: [['b', '4'], ['e', 'd']]. Неприводимый многочлен: x^4+x+1. Режим
шифрования ECB. Ключ равен 2318. Зашифровать в режиме ECB, оставив
первые 50 байт без изменения.
'''

from lib.saes import AES 
import lib.read_write_file as io 
from lib.local_path import SRC_ENCRYPTED_
from lib.local_path import SRC_DECRYPTED_
from lib.util import numeric_matrix_to_str_mx

key = 2318
MATRIX_2x2 = [[0xB, 0x4],
              [0xE, 0xD]]
mod = 0b10011
n = 4
#-----------------------------------------------------------
data = io.read_data_2byte(SRC_ENCRYPTED_('im43_saes_c_all.bmp'))

# for mod in range(0, 100000):
#     aes = AES(key)
#     aes.column_Matrix = numeric_matrix_to_str_mx(MATRIX_2x2)
#     aes.column_InvMatrix = numeric_matrix_to_str_mx(AES.inverse_matrix_2x2(MATRIX_2x2, mod, n))
#     aes.modulus = mod
#     decrypted_data = aes.decrypt_data(data[:2])
#     if decrypted_data[0] == 19778:
#         print(mod) 
     
aes = AES(key)
aes.column_Matrix = MATRIX_2x2
aes.column_InvMatrix = AES.inverse_matrix_2x2(MATRIX_2x2, mod, n)
print(aes.column_InvMatrix)
decrypted_data = aes.decrypt_data(data[:3])
print(decrypted_data[:3])  
io.write_data_2byte(SRC_DECRYPTED_('im43_saes_c_out.bmp'), decrypted_data)


# for k1 in range(0, 16):
#     for k2 in range(0, 16):
#         for k3 in range(0, 16):
#             for k4 in range(0, 16):
#                 aes = AES(key)
#                 aes.column_Matrix = numeric_matrix_to_str_mx(MATRIX_2x2)
#                 aes.column_InvMatrix = numeric_matrix_to_str_mx([[k1, k2], [k3, k4]])
#                 decrypted_data = aes.decrypt_data(data[:2])
#                 if decrypted_data[0] == 19778:
#                     print(k1, k2, k3, k4)




