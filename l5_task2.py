'''
Вариант 2
Расшифровать файл aa3_sdes_c_ofb_all.bmp – зашифрованное шифром S_DES
изображение в формате bmp. Режим шифрования OFB. Ключ равен 932. Вектор
инициализации равен 234. Зашифровать в режиме ECB и в режиме OFB, оставив
первые 50 байт без изменения. Сравнить полученные изображения.
'''

import lib.sdes as s
import lib.read_write_file as io 
from lib.local_path import SRC_ENCRYPTED_
from lib.local_path import SRC_DECRYPTED_
from lib.encryption_mode.ofb import decrypt_ofb

def process_file(file_path, output_path, key, iv):
    sdes = s.SDes()
    sdes.key_schedule(key)

    data = io.read_data_1byte(file_path)

    body = data
    
    def encrypt_sdec(ch): 
        return sdes.encrypt_block(ch, sdes.k1)
    
    decrypted_body = decrypt_ofb(body, encrypt_sdec, iv)
    print(decrypted_body[:3])
    io.write_data_1byte(output_path, decrypted_body)


key = 932
iv = 234

process_file(SRC_ENCRYPTED_('aa3_sdes_c_ofb_all.bmp'), SRC_DECRYPTED_('aa3_sdes_c_ofb_out.bmp'), key, iv)