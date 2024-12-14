'''
3. Расшифровать файл dd5_saes_cbc_c_all.bmp – зашифрованное
шифром S_AES изображение в формате bmp. Матрица для преобразования
MixColumns: [['a', 'c'], ['8', '6']]. Неприводимый многочлен: x^4+x^3+1. 
Режим шифрования CBС. Ключ равен 1021. Вектор инициализации равен 456.
Зашифровать, оставив первые 50 байт без изменения. 
'''

from lib.saes import AES 
import lib.read_write_file as io 
from lib.local_path import SRC_ENCRYPTED_
from lib.local_path import SRC_DECRYPTED_
from lib.encryption_mode.cbc import decrypt_cbc
from lib.util import numeric_matrix_to_str_mx

key = 1021
vi = 456
MATRIX_2x2 = [[0xa, 0xc],[0x8, 0x6]]
mod = 0b11001
n = 4
#-----------------------------------------------------------
aes = AES(key)
aes.column_Matrix = numeric_matrix_to_str_mx(MATRIX_2x2)
aes.column_InvMatrix = numeric_matrix_to_str_mx(AES.inverse_matrix_2x2(MATRIX_2x2, mod, n))

data = io.read_data_2byte(SRC_ENCRYPTED_('dd5_saes_cbc_c_all.bmp'))

def decrypted_saes(block):
    return aes.decrypt(block)

decrypted_data = decrypt_cbc(data, decrypted_saes, vi)    
print(decrypted_data[:3])
io.write_data_2byte(SRC_DECRYPTED_('dd5_saes_cbc_c_out.bmp'), decrypted_data)
