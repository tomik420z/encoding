def gf_multiply_modular(a, b, mod, n = 4):
    """
    INPUTS
    a - полином (множимое)
    b - полином (множитель)
    mod - неприводимый полином
    n - порядок неприводимого полинома
    OUTPUTS:
    product - результат перемножения двух полиномов a и b
    """
    # маска для наиболее значимого бита в слове
    msb = 2**(n - 1)
    # маска на все биты
    mask = 2**n - 1
    # r(x) = x^n mod m(x)
    r = mod ^ (2**n)
    product = 0 # результат умножения
    mm = 1
    for i in range(n):
        if b & mm > 0:
            # если у множителя текущий бит 1
            product ^= a
        # выполняем последовательное умножение на х
        if a & msb == 0:
            # если старший бит 0, то просто сдвигаем на 1 бит
            a <<= 1
        else:
            # если старший бит 1, то сдвиг на 1 бит
            a <<= 1
            # и сложение по модулю 2 с r(x)
            a ^= r
            # берем только n бит
            a &= mask
        # формируем маску для получения очередного бита в множителе
        mm += mm
    return product

def gf_divide(a, b):
    # деление полинома на полином
    # результат: частное, остаток (полиномы)
    dividend = a # делимое
    divisor = b # делитель
    a = 0
    # бит в делимом
    m = len(bin(dividend))-2
    # бит в делителе
    n = len(bin(divisor))-2
    s = divisor << m
    msb = 2 ** (m + n - 1)
    for i in range(m):
        dividend <<= 1
        if dividend & msb > 0:
            dividend ^= s
            dividend ^= 1
    maskq = 2**m - 1
    maskr = 2**n - 1
    r = (dividend >> m) & maskr
    q = dividend & maskq
    return q, r

def gf_inv(b, m, n):
    """Находит обратный элемент x в GF(2^4) по модулю m."""
    a1, a2, a3 = 1, 0, m
    b1, b2, b3 = 0, 1, b
    
    while b3 != 1:
        q, r = gf_divide(a3, b3)
        t1, t2, t3 = a1 + gf_multiply_modular(q, b1, m, n), a2 + gf_multiply_modular(q, b2, m, n), r
        a1, a2, a3 = b1, b2, b3
        b1, b2, b3 = t1, t2, t3
    return b2
    

def inverse_matrix_2x2(matrix):
    """Находит обратную матрицу размерности 2x2 в поле GF(2^4)."""
    a, b = matrix[0]
    c, d = matrix[1]
    
    # Находим детерминант
    det = gf_multiply_modular(a, d, 0b10011) ^ gf_multiply_modular(b, c, 0b10011)

    # Проверка на обратимость
    det_inv = gf_inv(det, 0b10011, 4)

    # Вычисление элементов обратной матрицы
    a_inv = gf_multiply_modular(
        d, det_inv, 0b10011
    )
    
    b_inv = gf_multiply_modular(
        gf_multiply_modular(b, det_inv, 0b10011) ^ (0b0), 1, 0b10011
    )
    
    c_inv = gf_multiply_modular(
        gf_multiply_modular(c, det_inv, 0b10011) ^ (0b0), 1, 0b10011
    )
    
    d_inv = gf_multiply_modular(
        a, det_inv, 0b10011
    )

    return [[a_inv, b_inv], [c_inv, d_inv]]

# n = 4
# a = 0b11
# m = 0b10011
# inv_a = gf_inv(a, m, n)
# print(format(inv_a))

# Пример использования
A = [[1, 4],   # 1 и 10
     [4, 1]]  # 11 и 12
A_inv = inverse_matrix_2x2(A)
print(A_inv)

# print("Обратная матрица:")
# for row in A_inv:
#     print([bin(elem) for elem in row])  # Печатаем в двоичном виде