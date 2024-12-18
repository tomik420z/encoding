from BitVector import BitVector

def ConvertToStr(bytesData):
    return ''.join([chr(s) for s in bytesData])


def divide_two_byte_number(block):
    '''
    конвертирует 2-ух байтовое число в два однобайтовых 
    '''
    return (block >> 8) & 0xFF, block & 0xFF
    

def modular_to_bit_vector(m : int):
    return BitVector(intVal = m, size = 5)


def convert_2b_to_str(bytes_data):
    one_bytes_data = []

    for block in bytes_data:
        b1, b2 = divide_two_byte_number(block)
        one_bytes_data.append(b1)
        one_bytes_data.append(b2)

    return ConvertToStr(one_bytes_data)

def IsPng(data):
    keySequence = [137, 80]
    return keySequence == data[:2]


def IsBmp(data):
    if len(data) < 2:
        return False
    keySequence = [66, 77]
    return keySequence == data[:2]


def numeric_matrix_to_str_mx(mx):
    ans = []
    for line in mx:
        ans.append([str(el) for el in line])
    return ans