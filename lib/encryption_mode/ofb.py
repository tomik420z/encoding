def decrypt_ofb(encrypted_data, fn_encrypt, iv):
    decrypted = []    
    o_i = iv

    for byte in encrypted_data:
        o_i = fn_encrypt(o_i)
        decrypted.append(byte ^ o_i)

    return decrypted
    