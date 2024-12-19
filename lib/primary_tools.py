import random
import lib.util as util 
import math


def euler_fun(n):
    result = 1  # 1 всегда взаимно просто с n
    for i in range(2, n):
        if gcd(i, n) == 1:
            result += 1
    return result


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def is_prime(p):
    if p < 2:
        return False
    for i in range(2, int(p ** 0.5) + 1):
        if p % i == 0:
            return False
    return True


def z_nz_group(n):
    group = []
    for x in range(1, n):
        if gcd(x, n) == 1:
            group.append(x)
    return group

def multiplicative_order(g, n):
    if gcd(g, n) != 1:
        return None
    order = 1
    result = g % n
    while result != 1:
        result = (result * g) % n
        order += 1
    return order


def primitive_roots(n):
    phi_n = euler_fun(n)
    roots = []
    for g in range(1, n):
        if gcd(g, n) == 1 and multiplicative_order(g, n) == phi_n:
            roots.append(g)
    return roots


def inv_number(a, p):
    return (a ** (p - 2)) % p


def find_p_2q_plus_1(bitfield_width):
    while True:
        q = random.randint(2 ** 5 - 1, 2 ** bitfield_width - 1)

        if q % 2 == 0:
            continue

        if is_prime(q):
            p = 2 * q + 1
            if is_prime(p):
                return p 
            

def find_first_g(p):
    '''
    находит первый первообразный корень 
    '''
    q = (p - 1) // 2
    for g in range(2, p):
        if (g ** q) % p != 1:
            return g
    
    return None


def find_p_g(bitfield_width):
    min_value, max_value = util.bound(bitfield_width)
    while True:
        q = random.randint(min_value, max_value)
        if q % 2 == 0:
            continue

        if is_prime(q):
            p = 2 * q + 1
            if is_prime(p):
                return p, find_first_g(p)
            

def power(a, x, p):
    t = math.floor(math.log2(x))
    s = a
    for i in range(t + 1):
        if util.check_bit(x, i):
            y *= s
            y %= p
        s = (s * s) % p

    return y 


def txt_2_int_nums(message, block_size):
     
    hash_sums = []
    i = 0
    p = len(message) // block_size 
    for j in range(p + 1):
        curr_sum = 0    
        for i in range(block_size):
            if j * block_size + i >= len(message):
                break
            curr_sum += ord(message[j * block_size + i]) * (256 ** i)
        if curr_sum > 0:
            hash_sums.append(curr_sum)
    
    return hash_sums


def int_nums_2_txt(bloks, block_size):
    message = ''
    for block in bloks:
        c = block
        for _ in range(block_size):
            message += chr(c % 256)
            c //= 256
    
    return message


def bytes_2_int_nums(data_in_bytes, block_size):

    hash_sums = []
    i = 0
    p = len(data_in_bytes) // block_size 
    for j in range(p + 1):
        curr_sum = 0    
        for i in range(block_size):
            if j * block_size + i >= len(data_in_bytes):
                break
            curr_sum += data_in_bytes[j * block_size + i] * (256 ** i)
        if curr_sum > 0:
            hash_sums.append(curr_sum)
    
    return hash_sums


def int_nums_2_bytes(bloks, block_size):
    data_in_bytes = []
    for block in bloks:
        c = block
        for _ in range(block_size):
            data_in_bytes.append(c % 256)
            c //= 256
    
    return data_in_bytes


def crt(a, m_list : list[int]):
    return [a % m for m in m_list]


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse does not exist")
    return x % m


def crt_inv(a_m: list[int], m_list: list[int]):
    total_product = 1
    for m in m_list:
        total_product *= m

    result = 0
    for a_i, m_i in zip(a_m, m_list):
        partial_product = total_product // m_i
        inverse = mod_inverse(partial_product, m_i)
        result += a_i * partial_product * inverse

    return result % total_product


def crt_inv_for_prime(a_m: list[int], m_list: list[int]):
    '''
    можно использовать, если все числа из m_list -- простые 
    оптимизированна для простых чисел crt_inv
    '''
    total_product = 1
    for m in m_list:
        total_product *= m

    result = 0
    for a_i, m_i in zip(a_m, m_list):
        partial_product = total_product // m_i
        inverse = inv_number(partial_product, m_i)
        result += a_i * partial_product * inverse

    return result % total_product


def dlog(g, pub_key, p):
    for x in range(p):
        if pub_key == (g ** x) % p:
            return x
    return None


def dlog_opt(g, pub_key, p):
    # Вычисляем m = ceil(sqrt(p))
    m = int(math.ceil(math.sqrt(p)))
    
    # Шаг младенца: вычисляем g^j mod p для j = 0, 1, ..., m-1
    baby_steps = {}
    for j in range(m):
        baby_steps[pow(g, j, p)] = j
    
    # Шаг великана: вычисляем g^{-m} mod p
    g_inv_m = pow(g, -m, p)  # Используем pow с отрицательным показателем для обратного
    if g_inv_m == 0:
        raise ValueError("g не имеет обратного по модулю p")
    
    # Шаг великана: вычисляем pub_key * (g^{-m})^i mod p для i = 0, 1, ..., m-1
    current = pub_key
    for i in range(m):
        # Проверяем, есть ли current в baby_steps
        if current in baby_steps:
            return i * m + baby_steps[current]
        # Обновляем current
        current = (current * g_inv_m) % p
    
    # Если решения нет
    return None

def elgamal_encrypt(pub_key, g, p, m):
    '''
    pub_key = public key
    g = primitive root
    p = prime
    message = number < p
    '''
    k = random.randint(1, p - 1)
    c_1 = pow(g, k, p) 
    c_2 = (m * pow(pub_key, k, p)) % p  
    return c_1, c_2


def elgamal_decrypt(pri_key, p, c1, c2):
    return (mod_inverse(c1 ** pri_key, p) * c2) % p 
    


# # Пример использования
# g = 3
# pub_key = 8
# p = 17
# priv_key = baby_step_giant_step(g, pub_key, p)
# print(f"Приватный ключ priv_key: {priv_key}")

# def modular_exponentiation(base, exp, mod):
#     """Возводит base в степень exp по модулю mod."""
#     result = 1
#     base = base % mod
#     while exp > 0:
#         if (exp % 2) == 1:  # Если exp нечетное
#             result = (result * base) % mod
#         exp = exp >> 1  # Делим exp на 2
#         base = (base * base) % mod
#     return result

# def dlog_opt(g, pub_key, p):
#     """Вычисляет дискретный логарифм pub_key = g^priv_key mod p."""
#     """RETURN priv_key"""

#     # Определяем m
#     m = int(math.ceil(math.sqrt(p - 1)))

#     # Шаг младенца
#     baby_steps = {}
#     for j in range(m):
#         value = modular_exponentiation(g, j, p)
#         baby_steps[value] = j

#     # Шаг великана
#     g_inv_m = modular_exponentiation(g, -m, p)  # g^(-m) mod p
#     current = pub_key

#     for i in range(m):
#         if current in baby_steps:
#             # Найдено совпадение
#             return i * m + baby_steps[current]
#         current = (current * g_inv_m) % p

#     return None  # Если логарифм не найден

    # M = 1
    # for m_curr in m_list:
    #     M *= m_curr 

    # inv_list = [inv_number(a, m_curr) for m_curr in m_list]
    # list_c = [curr_m * curr_inv for curr_m, curr_inv in zip(m_list, inv_list)]
    