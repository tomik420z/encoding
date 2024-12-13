
def decrypt_cbc(encrypted_data, fn_decrypt, iv):
    decrypted = []
    c_i = iv
    for byte in encrypted_data:
        decrypted.append(c_i ^ fn_decrypt(byte))
        c_i = byte
    return decrypted