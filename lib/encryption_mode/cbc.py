
def decrypt_cbc(encrypted_data, fn_decrypt, iv):
    decrypted = []
    c_i = iv
    for byte in encrypted_data:
        decrypted.append(c_i ^ fn_decrypt(byte))
        c_i = byte
    return decrypted


def encrypt_cbc(plain_data, fn_encrypt, iv):
    encrypted = []
    c_i = iv
    
    for byte in plain_data:
        block_to_encrypt = c_i ^ byte
        encrypted_byte = fn_encrypt(block_to_encrypt)
        encrypted.append(encrypted_byte)
        c_i = encrypted_byte
    
    return encrypted
