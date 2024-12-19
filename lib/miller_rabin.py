import random
import lib.util as util

def rabin_miller(n):
    # Returns True if num is a prime number.
    q = n - 1
    k = 0
    while q % 2 == 0:
        # keep halving s until it is even (and use t
        # to count how many times we halve s)
        q = q // 2
        k += 1
    t = 5
    for trials in range(t):  # try to falsify num's primality 5 times
        a = random.randrange(2, n - 1)
        v = pow(a, q, n)
        if v != 1:  # this test does not apply if v is 1.
            i = 0
            while v != (n - 1):
                if i == k - 1:
                    return False, 0
                else:
                    i = i + 1
                    v = (v ** 2) % n
    probability_of_prime = 1 - 1.0/(4 ** t)
    return True, probability_of_prime


def is_prime(n):
    # Return True if n is a prime number. This function does a quicker
    # prime number check before calling rabin_miller().
    if n < 2:
        return False   # 0, 1, and negative numbers are not prime
    # About 1/3 of the time we can quickly determine if n is not prime
    # by dividing by the first few dozen prime numbers. This is quicker
    # than rabin_miller().
    low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    if n in low_primes:
        return True
    # See if any of the low prime numbers can divide n
    for prime in low_primes:
        if n % prime == 0:
            return False
    # If all else fails, call rabin_miller() to determine if n is a prime.
    return rabin_miller(n)


def generate_large_prime(bitfield_width):
    while True:
        min_val, max_val = util.bound(bitfield_width)
        candidate = random.randint(min_val, max_val)
        # print(candidate)
        #Гарантировать, что два старших бита выставлены в 1:
        candidate |= (1 << bitfield_width - 1)
        candidate |= (2 << bitfield_width - 3)
        if is_prime(candidate):
            return candidate
