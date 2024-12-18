# 7. Расшифровать файл dd12_saes_ctr_c_all.bmp – зашифрованное
# шифром S_AES изображение в формате bmp. Матрица для преобразования
# MixColumns: [['7', '3'], ['2', 'e']]. Неприводимый многочлен: x^4+x+1. Режим
# шифрования CTR. Ключ равен 2645. Вектор инициализации равен 23184.
# Зашифровать, оставив первые 50 байт без изменения.

from lib.saes import AES 
import lib.read_write_file as io 
from lib.local_path import SRC_ENCRYPTED_
from lib.local_path import SRC_DECRYPTED_
from lib.encryption_mode.ctr import decrypt_ctr_2_bytes
from lib.util import numeric_matrix_to_str_mx

data = io.read_data_2byte(SRC_ENCRYPTED_('dd12_saes_ctr_c_all.bmp'))
vi = 23184
key = 2645
MATRIX_2x2 = [[0x7, 0x3],[0x2, 0xe]]
mod = 0b10011
n = 4

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


# #-----------------------------------------------------------
aes = AES(key)
aes.column_Matrix = MATRIX_2x2
aes.column_InvMatrix = AES.inverse_matrix_2x2(MATRIX_2x2, mod, n)
aes.set_modulus(mod)

def decrypted_saes(block):
    return aes.encrypt(block)

decrypted_data = decrypt_ctr_2_bytes(data, decrypted_saes, vi)    
print(decrypted_data[:3])
io.write_data_2byte(SRC_DECRYPTED_('dd12_saes_ctr_c_out.bmp'), decrypted_data)
