'''
Вариант 15
Расшифровать файл im37_sdes_c_cfb_all.bmp. Шифр SDES. Режим CFB. Key =
862, iv= 221. Зашифровать, оставив первые 50 байт без изменения.
'''

import lib.sdes as s
import lib.read_write_file as io 
from lib.local_path import SRC_ENCRYPTED_
from lib.local_path import SRC_DECRYPTED_

def process_file(file_path, output_path, key, iv):
    sdes = s.SDes()
    sdes.key_schedule(key)

    data = io.read_data_1byte(file_path)

    body = data
    decrypted_body = sdes.cfb_decrypt(body, iv, sdes.k1)
    
    io.write_data_1byte(output_path, decrypted_body)


key = 0b1101011110  
iv = 0b11011101   

process_file(SRC_ENCRYPTED_('im37_sdes_c_cfb_all.bmp'), SRC_DECRYPTED_('im37_sdes_c_cfb_output.bmp'), key, iv)