import random
import lib.util as util 
# import util as util 
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
    return a ** (p - 2) % p


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
