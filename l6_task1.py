'''
1. Расшифровать файл dd1_saes_c_all.bmp – зашифрованное шифром
S_AES изображение в формате bmp. Матрица для преобразования
MixColumns: [['1', '4'], ['4', '1']]. Неприводимый многочлен: x^4+x+1. Режим
шифрования ECB. Ключ равен 834. Зашифровать в режиме ECB, оставив
первые 50 байт без изменения
'''

from lib.saes import AES 
import lib.read_write_file as io 
from lib.local_path import SRC_ENCRYPTED_
from lib.local_path import SRC_DECRYPTED_
from lib.util import numeric_matrix_to_str_mx

key = 834
MATRIX_2x2 = [[0x1, 0x4],[0x4, 0x1]]
mod = 0b10011
n = 4
#-----------------------------------------------------------
aes = AES(key)
aes.column_Matrix = numeric_matrix_to_str_mx(MATRIX_2x2)
aes.column_InvMatrix = numeric_matrix_to_str_mx(AES.inverse_matrix_2x2(MATRIX_2x2, mod, n))


data = io.read_data_2byte(SRC_ENCRYPTED_('dd1_saes_c_all.bmp'))

decrypted_data = aes.decrypt_data(data)    
print(decrypted_data[:3])
io.write_data_2byte(SRC_DECRYPTED_('dd1_saes_c_out.bmp'), decrypted_data)

