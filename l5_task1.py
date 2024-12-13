'''
Вариант 1
Расшифровать файл aa2_sdes_c_cbc_all.bmp – зашифрованное шифром S_DES
изображение в формате bmp. Режим шифрования CBC. Ключ равен 845. Вектор
инициализации равен 56. Зашифровать в режиме ECB и в режиме CBC, оставив
первые 50 байт без изменения. Сравнить полученные изображения.
'''
import lib.sdes as s
import lib.read_write_file as io 
from lib.local_path import SRC_ENCRYPTED_
from lib.local_path import SRC_DECRYPTED_
from lib.encryption_mode.cbc import decrypt_cbc
from lib.encryption_mode.cbc import encrypt_cbc

def process_file(file_path, output_path, key, iv):
    sdes = s.SDes()
    sdes.key_schedule(key)

    data = io.read_data_1byte(file_path)

    body = data
    
    def decrypt_sdec(ch): 
        return sdes.decrypt_block(ch, sdes.k1)
    
    decrypted_body = decrypt_cbc(body, decrypt_sdec, iv)
    
    io.write_data_1byte(output_path, decrypted_body)

    # зашифруем в режиме CBC
    def encrypt_sdec(ch):
        return sdes.encrypt_block(ch, sdes.k1)
    
    encrypted_body = encrypt_cbc(decrypted_body[50:], encrypt_sdec, iv)
    io.write_data_1byte(SRC_DECRYPTED_('aa2_sdes_c_cbc_encrypt_out.bmp'), decrypted_body[:50] + encrypted_body)

key = 845
iv = 56

process_file(SRC_ENCRYPTED_('aa2_sdes_c_cbc_all.bmp'), SRC_DECRYPTED_('aa2_sdes_c_cbc_out.bmp'), key, iv)