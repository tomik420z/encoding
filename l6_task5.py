'''
5. Дешифровать файл t20_saes_ofb_c_all.txt. Шифр SAES. Режим OFB.
Известны младшие биты ключа: 011110110, вектор инициализации 3523
Матрица для преобразования MixColumns: [['3', '8'], ['2', 'b']]. Неприводимый
многочлен: x^4+x+1.
'''
import itertools
from lib.saes import AES 
import lib.read_write_file as io 
from lib.local_path import SRC_ENCRYPTED_
from lib.local_path import SRC_DECRYPTED_
from lib.encryption_mode.ofb import decrypt_ofb
from lib.detectEnglish import isEnglish
from lib.util import convert_2b_to_str
known_bits = '011110110'
iv = 3523
MATRIX_2x2 = [[0x3, 0x8],[0x2, 0xb]]
mod = 0b10011
n = 4

# Перебор всех 16-битных ключей
data = io.read_data_2byte(SRC_ENCRYPTED_('t20_saes_ofb_c_all.txt'))

inv_matrix = AES.inverse_matrix_2x2(MATRIX_2x2, mod, n)

i = 0
for bits in itertools.product('01', repeat=7):
    candidate_key = ''.join(bits) + known_bits  # Формируем полный ключ
    
    candidate_key_int = int(candidate_key, 2)  # Преобразуем в целое число

    aes = AES(candidate_key_int)
    aes.column_Matrix = MATRIX_2x2
    aes.column_InvMatrix = inv_matrix
    aes.set_modulus(mod)
    decrypted_data = decrypt_ofb(data[:10], lambda block : aes.decrypt(block), iv)

    str_sequence = convert_2b_to_str(decrypted_data)
    print(f'key = {candidate_key}', str_sequence)
    