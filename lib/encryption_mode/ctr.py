def decrypt_ctr(encrypted_data, fn_encrypt, iv):
    decrypted = []
    c_i = iv
    
    for byte in encrypted_data:
        decrypted.append(byte ^ fn_encrypt(c_i))
        c_i = (c_i + 1) % 256 

    return decrypted


def decrypt_ctr_2_bytes(encrypted_data, fn_encrypt, iv):
    decrypted = []
    c_i = iv
    
    for byte in encrypted_data:
        decrypted.append(byte ^ fn_encrypt(c_i))
        c_i = (c_i + 1) % (2 ** 16) 

    return decrypted