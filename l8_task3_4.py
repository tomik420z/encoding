'''
Задание 4
Создать текстовый файл. 
Записать в него свою ФИО (полностью). 
Извлечь содержимое файла в список data. 
Преобразовать этот список в массив целых чисел размерностью три байта (block_size=3). 
Выполнить обратное преобразование. 
Результат сохранить в новом файле. 
Два файла должны быть полностью идентичны.
'''
import lib.read_write_file as io
from lib.local_path import SRC_DECRYPTED_
from lib.local_path import SRC_ENCRYPTED_
import lib.primary_tools as pt
import lib.util as util

BLOCK_SIZE = 3

import os.path

FILE_DIR = os.getcwd()
print(FILE_DIR)
data = io.read_data_1byte(SRC_DECRYPTED_('my_name.txt'))
encrypted_data = pt.bytes_2_int_nums(data, BLOCK_SIZE)
decrypted_data = pt.int_nums_2_bytes(encrypted_data, block_size=BLOCK_SIZE)
print(util.ConvertToStr(decrypted_data))

