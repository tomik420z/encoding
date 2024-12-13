class SDes:
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]
    LS1 = [2, 3, 4, 5, 1]
    LS2 = [3, 4, 5, 1, 2]
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
    EP = [4, 1, 2, 3, 2, 3, 4, 1]
    P4 = [2, 4, 3, 1]
    S0 = [[1, 0, 3, 2],
          [3, 2, 1, 0],
          [0, 2, 1, 3],
          [3, 1, 3, 2]]
    S1 = [[0, 1, 2, 3],
          [2, 0, 1, 3],
          [3, 0, 1, 0],
          [2, 1, 0, 3]]

    def init(self):
        self.k1 = 0  
        self.k2 = 0  

    @staticmethod
    def pbox(x, p, nx):        
        y = 0
        for i in reversed(range(len(p))):
            if x & (1 << (nx - p[i])):
                y |= (1 << (len(p) - 1 - i))
        return y

    def p10(self, x):
        return self.pbox(x, self.P10, 10)

    def p8(self, x):
        return self.pbox(x, self.P8, 10)

    def ls(self, x, p, n):        
        return self.pbox(x, p, n)

    def key_schedule(self, key):        
        permuted_key = self.p10(key)        
        left, right = permuted_key >> 5, permuted_key & 0b11111       
        left = self.ls(left, self.LS1, 5)
        right = self.ls(right, self.LS1, 5)        
        self.k1 = self.p8((left << 5) | right)        
        left = self.ls(left, self.LS2, 5)
        right = self.ls(right, self.LS2, 5)        
        self.k2 = self.p8((left << 5) | right)

    def sbox_lookup(self, sbox, row, col):
        return sbox[row][col]

    def fk(self, block, key):
        left, right = block >> 4, block & 0b1111        
        ep = self.pbox(right, self.EP, 4)        
        ep ^= key        
        left_ep, right_ep = ep >> 4, ep & 0b1111     
        row_s0 = ((left_ep & 0b1000) >> 2) | (left_ep & 0b0001)
        col_s0 = (left_ep & 0b0110) >> 1
        s0_out = self.sbox_lookup(self.S0, row_s0, col_s0)

        row_s1 = ((right_ep & 0b1000) >> 2) | (right_ep & 0b0001)
        col_s1 = (right_ep & 0b0110) >> 1
        s1_out = self.sbox_lookup(self.S1, row_s1, col_s1)        
        combined = (s0_out << 2) | s1_out
        p4 = self.pbox(combined, self.P4, 4)        
        left ^= p4
        return (left << 4) | right

    def encrypt_block(self, block, key):
        ip = self.pbox(block, self.IP, 8)
        fk1 = self.fk(ip, self.k1)
        swapped = ((fk1 & 0b1111) << 4) | (fk1 >> 4)
        fk2 = self.fk(swapped, self.k2)
        encrypted = self.pbox(fk2, self.IP_INV, 8)
        return encrypted

    def decrypt_block(self, block, key):
        ip = self.pbox(block, self.IP, 8)
        fk2 = self.fk(ip, self.k2)
        swapped = ((fk2 & 0b1111) << 4) | (fk2 >> 4)
        fk1 = self.fk(swapped, self.k1)
        decrypted = self.pbox(fk1, self.IP_INV, 8)
        return decrypted

    def cfb_encrypt(self, data, iv, key):
        encrypted = bytearray()
        feedback = iv

        for byte in data:
            encrypted_byte = self.encrypt_block(feedback, key) ^ byte
            encrypted.append(encrypted_byte)
            feedback = encrypted_byte  

        return encrypted

    def cfb_decrypt(self, data, iv, key):
        decrypted = bytearray()
        feedback = iv

        for byte in data:
            decrypted_byte = self.encrypt_block(feedback, key) ^ byte
            decrypted.append(decrypted_byte)
            feedback = byte  

        return decrypted



