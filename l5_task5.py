'''
Вариант 5
Дешифровать файл im39_sdes_c_cbc_all.bmp. Шифр SDES. 
Режим CBC. iv=132. Зашифровать, оставив первые 50 байт без изменений
'''

import lib.sdes as s
import lib.read_write_file as io 
from lib.local_path import SRC_ENCRYPTED_
from lib.local_path import SRC_DECRYPTED_
from lib.encryption_mode.cbc import decrypt_cbc
from lib.util import IsBmp

def find_keys(encrypted_data, iv):
    keys = []
    for key in range(1, 1000):
        sdes = s.SDes()
        sdes.key_schedule(key)

        def decrypt_sdec(ch): 
            return sdes.decrypt_block(ch, sdes.k1)
    
        decrypted_data = decrypt_cbc(encrypted_data, decrypt_sdec, iv)
        if IsBmp(decrypted_data):
            keys.append(key)

    return keys


def process_file(file_path, output_path, iv):
    
    data = io.read_data_1byte(file_path)
    keys = find_keys(data[:2], iv)
    if len(keys) == 0:
        print("Key not found")
        return
    
    # придётся перебирвать КАЖДЫЙ найденный ключ и смотреть на картинку в нашем примере 3 ключа (92, 921, 977) и правльный из них 921 
    for key in keys: 
        sdes = s.SDes()
        sdes.key_schedule(key)

        data = io.read_data_1byte(file_path)

        body = data
        
        def decrypt_sdec(ch): 
            return sdes.decrypt_block(ch, sdes.k1)
        
        decrypted_body = decrypt_cbc(body, decrypt_sdec, iv)
        
    
        print(decrypted_body[:3])
        io.write_data_1byte(output_path + str(key) + '.bmp', decrypted_body)
    


iv = 132

process_file(SRC_ENCRYPTED_('im39_sdes_c_cbc_all.bmp'), SRC_DECRYPTED_('im39_sdes_c_cbc_out'), iv)