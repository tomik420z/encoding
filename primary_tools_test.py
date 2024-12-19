import unittest
import lib.primary_tools as pt
import lib.miller_rabin as mr

def display_test_name(test_func):
    """Декоратор для отображения имени теста перед его выполнением."""
    def wrapper(*args, **kwargs):
        print(f'Запуск теста: {test_func.__name__}')
        return test_func(*args, **kwargs)
    return wrapper

class TestPrimary(unittest.TestCase):
    @display_test_name
    def test_euler(self):
        self.assertEqual(pt.euler_fun(10), 4)
        self.assertEqual(pt.euler_fun(12), 4)
        self.assertEqual(pt.euler_fun(29), 28)
        self.assertEqual(pt.euler_fun(701), 700)
    
    @display_test_name
    def test_euler_mult(self):
        p = 17
        q = 113
        k = 3
        self.assertEqual(pt.euler_fun(p * q), (p - 1) * (q - 1))
        self.assertEqual(pt.euler_fun(p ** k), p ** k - p ** (k - 1))
        self.assertEqual(pt.euler_fun(q ** k), q ** k - q ** (k - 1))

    @display_test_name
    def test_z_group(self):
        self.assertEqual(pt.z_nz_group(9), [1,2,4,5,7,8])
        self.assertEqual(pt.z_nz_group(8), [1,3,5,7])
        self.assertEqual(pt.z_nz_group(7), [1,2,3,4,5,6])
        
    @display_test_name
    def test_multiplicative_order(self):
        self.assertEqual(pt.multiplicative_order(1, 17), 1)
        self.assertEqual(pt.multiplicative_order(2, 17), 8)
        self.assertEqual(pt.multiplicative_order(3, 17), 16)
        self.assertEqual(pt.multiplicative_order(4, 17), 4)
        self.assertEqual(pt.multiplicative_order(5, 17), 16)
        self.assertEqual(pt.multiplicative_order(6, 17), 16)
        self.assertEqual(pt.multiplicative_order(7, 17), 16)
        self.assertEqual(pt.multiplicative_order(8, 17), 8)
        self.assertEqual(pt.multiplicative_order(9, 17), 8)
        self.assertEqual(pt.multiplicative_order(10, 17), 16)
        self.assertEqual(pt.multiplicative_order(11, 17), 16)
        self.assertEqual(pt.multiplicative_order(12, 17), 16)
        self.assertEqual(pt.multiplicative_order(13, 17), 4)
        self.assertEqual(pt.multiplicative_order(14, 17), 16)
        self.assertEqual(pt.multiplicative_order(15, 17), 8)
        self.assertEqual(pt.multiplicative_order(16, 17), 2)

    @display_test_name
    def test_primitive_roots(self):
        self.assertEqual(pt.primitive_roots(4), [3])
        self.assertEqual(pt.primitive_roots(7), [3, 5])
        self.assertEqual(pt.primitive_roots(29), [2, 3, 8, 10, 11, 14, 15, 18, 19, 21, 26, 27])
        self.assertEqual(pt.primitive_roots(18), [5, 11])

    @display_test_name
    def test_pherma(self):
        p = 17449
        a = 7814
        a_inv = pt.inv_number(a, p)
        print(f'a = {a}, a_inv = {a_inv}')  
        self.assertEqual((a * a_inv) % p, 1)

    @display_test_name
    def test_th(self):
        a = 5
        b = 4
        p = 12
        phi_n = pt.euler_fun(b)
        print(f"phi({b}) = {phi_n}")
        result = pow(a, phi_n, p)
        print(f"{a}^{phi_n} mod {p} = {result}")


    @display_test_name
    def test_find_find_p_2q_plus_1(self):
        for i in range(100):
            p = pt.find_p_2q_plus_1(12)
            q = (p - 1) // 2
            self.assertEqual(pt.is_prime(q) == pt.is_prime(p) == True, True, f'p = {p}, q = {q}')


    @display_test_name
    def test_find_g(self):
        self.assertEqual(pt.find_first_g(5399), 7)


    @display_test_name
    def test_find_p_g(self):
        for i in range(100):
            p, g = pt.find_p_g(17)
            q = (p - 1) // 2
            self.assertNotEqual((g ** ((p - 1) / q)) % p, 1)


    @display_test_name
    def test_count_roots(self):
        cnt = 0
        for i in range(2, 100):
            if pt.is_prime(i):
                continue

            curr_roots = pt.primitive_roots(i)
            if 2 in curr_roots:
                cnt += 1

        print('cnt =', cnt)


    @display_test_name
    def test_generate_large_prime(self):
        number = mr.generate_large_prime(32)
        print('large num = ', bin(number)[2:])


    @display_test_name
    def test_check_sum(self):
        num = pt.txt_2_int_nums('Hello world!', block_size=12)
        self.assertEqual(num, [10334410032606748633331426632])
        num = pt.txt_2_int_nums('Hello world!', block_size=6)
        self.assertEqual(num, [35662932501832, 36715199885175])


    @display_test_name
    def test_int_nums_2_txt(self):
        msg = pt.int_nums_2_txt(bloks=[10334410032606748633331426632], block_size=12)
        self.assertEqual(msg, 'Hello world!')
        msg = pt.int_nums_2_txt([35662932501832, 36715199885175], block_size=6)
        self.assertEqual(msg, 'Hello world!')

    
    @display_test_name
    def test_bytes_2_int(self):
        data = [72, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100, 33]
        num = pt.bytes_2_int_nums(data, block_size=12)
        self.assertEqual(num, [10334410032606748633331426632])
        num = pt.bytes_2_int_nums(data, block_size=6)
        self.assertEqual(num, [35662932501832, 36715199885175])


    @display_test_name
    def test_ctr(self):
        self.assertEqual(pt.crt(2345, [89, 97]), [31, 17])
        self.assertEqual(pt.crt_inv([31, 17], [89, 97]), 2345)
        self.assertEqual(pt.crt_inv([1, 2, 3],[5, 8, 19]), 706)


    @display_test_name
    def test_dlog(self):
        self.assertEqual(pt.dlog(2, 1, 9), 0)
        self.assertEqual(pt.dlog(2, 2, 9), 1)
        self.assertEqual(pt.dlog(2, 4, 9), 2)
        self.assertEqual(pt.dlog(2, 8, 9), 3)
        self.assertEqual(pt.dlog(2, 7, 9), 4)
        self.assertEqual(pt.dlog(2, 5, 9), 5)   


    @display_test_name
    def test_dlog_opt(self):
        p = 901679
        g = 7
        pub_key = 386434
        priv_key = pt.dlog_opt(g, pub_key, p)
        print(f'priv_key = {priv_key}')
        self.assertEqual(pub_key, (g ** priv_key) % p)

        self.assertEqual(pt.dlog_opt(2, 1, 9), 0)
        self.assertEqual(pt.dlog_opt(2, 2, 9), 1)
        self.assertEqual(pt.dlog_opt(2, 4, 9), 2)
        self.assertEqual(pt.dlog_opt(2, 8, 9), 3)
        self.assertEqual(pt.dlog_opt(2, 7, 9), 4)
        self.assertEqual(pt.dlog_opt(2, 5, 9), 5)
        
    def test_elgamal(self):
        m = 331
        p = 467
        g = 2
        a = 153
        A = pow(g, a, p) 
        c1, c2 = pt.elgamal_encrypt(A, g, p, m)
        self.assertEqual(
            pt.elgamal_decrypt(a, p, c1, c2), m
        )
    
    


if __name__ == '__main__':
    unittest.main()