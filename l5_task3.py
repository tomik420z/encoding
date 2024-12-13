'''Вариант 3
Расшифровать файл aa4_sdes_c_cfb_all.bmp – зашифрованное шифром S_DES
изображение в формате bmp. Режим шифрования CFB. Ключ равен 455. Вектор
инициализации равен 162. Зашифровать в режиме ECB и в режиме CFB, оставив
первые 50 байт без изменения. Сравнить полученные изображения.
'''

import lib.sdes as s
import lib.read_write_file as io 
from lib.local_path import SRC_ENCRYPTED_
from lib.local_path import SRC_DECRYPTED_
from lib.encryption_mode.cfb import decrypt_cfb

def process_file(file_path, output_path, key, iv):
    sdes = s.SDes()
    sdes.key_schedule(key)

    data = io.read_data_1byte(file_path)

    body = data
    
    def encrypt_sdec(ch): 
        return sdes.encrypt_block(ch, sdes.k1)
    
    decrypted_body = decrypt_cfb(body, encrypt_sdec, iv)
    print(decrypted_body[:3])
    io.write_data_1byte(output_path, decrypted_body)


key = 455
iv = 162

process_file(SRC_ENCRYPTED_('aa4_sdes_c_cfb_all.bmp'), SRC_DECRYPTED_('aa4_sdes_c_cfb_out.bmp'), key, iv)