def decrypt_cfb(encrypted_data, fn_encrypt, iv):
    decrypted = []
    c_i = iv

    for byte in encrypted_data:
        decrypted.append(fn_encrypt(c_i) ^ byte)
        c_i = byte 

    return decrypted