from lib.saes import AES 

key = int('1010011100111011', 2)
aes = AES(key)

# Блок данных P = 0110111101101011
plaintext = int('0110111101101011', 2)

print("Исходный блок данных (plaintext):", bin(plaintext))
print("Ключи расширения:")

print(f"k0: {bin(aes.k0)}")
print(f"k1: {bin(aes.k1)}")
print(f"k2: {bin(aes.k2)}")

# Шифрование блока данных
print("\nШифрование:")
ciphertext = aes.encrypt(plaintext)
print("Зашифрованный блок данных (ciphertext):", bin(ciphertext))

# Проверка матрицы состояния
aes.to_state_matrix(ciphertext)
print("Матрица состояния после шифрования:")
print(aes.state_matrix)