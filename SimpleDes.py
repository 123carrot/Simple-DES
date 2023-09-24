import numpy as np
import time


# 初始置换盒
def initial_permutation(arr):
    arr = np.array(arr)
    a = np.array([3, 0, 2, 4, 6, 1, 7, 5])
    reordered_arr = np.zeros_like(arr)
    reordered_arr[a] = arr
    return reordered_arr


# 最终置换盒
def final_permutation(arr):
    arr = np.array(arr)
    a = np.array([1, 5, 2, 0, 3, 7, 4, 6])
    reordered_arr = np.zeros_like(arr)
    reordered_arr[a] = arr
    return reordered_arr


# 密钥置换P10
def key_permutation(arr):
    arr = np.array(arr)
    a = np.array([6, 2, 0, 4, 1, 9, 3, 8, 7, 5])
    reordered_arr = np.zeros_like(arr)
    reordered_arr[a] = arr
    return reordered_arr


# 压缩置换盒p8
def compression_permutation_box(input_array):
    input_array = np.array(input_array)
    input_array = input_array[2:]
    pbox = np.array([1, 3, 5, 0, 2, 4, 7, 6])
    reordered_arr = np.zeros_like(input_array)
    reordered_arr[pbox] = input_array
    return reordered_arr


# 扩展盒epbox
def expansion_permutation_box(input_array):
    input_array = np.array(input_array)
    input_array = np.concatenate([input_array.copy(), input_array.copy()])
    a = np.array([1, 2, 3, 0, 7, 4, 5, 6])
    reordered_arr = np.zeros_like(input_array)

    reordered_arr[a] = input_array
    return reordered_arr


# 轮函数替换Sbox1
def sub_box1(in4):
    in4 = np.array(in4)
    x = in4[[0, 3]]
    y = in4[[1, 2]]
    dic = {
        (0, 0): 0,
        (0, 1): 1,
        (1, 0): 2,
        (1, 1): 3
    }
    mapped_x = dic[tuple(x)]
    mapped_y = dic[tuple(y)]

    sbox1 = [[np.array([0, 1]), np.array([0, 0]), np.array([1, 1]), np.array([1, 0])],
             [np.array([1, 1]), np.array([1, 0]), np.array([0, 1]), np.array([0, 0])],
             [np.array([0, 0]), np.array([1, 0]), np.array([0, 1]), np.array([1, 1])],
             [np.array([1, 1]), np.array([0, 1]), np.array([0, 0]), np.array([1, 0])]]

    return sbox1[mapped_x][mapped_y]


# 轮函数替换Sbox2
def sub_box2(in4):
    in4 = np.array(in4)
    x = in4[[0, 3]]
    y = in4[[1, 2]]
    dic = {
        (0, 0): 0,
        (0, 1): 1,
        (1, 0): 2,
        (1, 1): 3
    }
    mapped_x = dic[tuple(x)]
    mapped_y = dic[tuple(y)]
    sbox2 = [[np.array([0, 0]), np.array([0, 1]), np.array([1, 0]), np.array([1, 1])],
             [np.array([1, 0]), np.array([1, 1]), np.array([0, 1]), np.array([0, 0])],
             [np.array([1, 1]), np.array([0, 0]), np.array([0, 1]), np.array([1, 0])],
             [np.array([1, 0]), np.array([0, 1]), np.array([0, 0]), np.array([1, 1])]]

    return sbox2[mapped_x][mapped_y]


# 替换函数sbox
def sub(arr):
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    result1 = sub_box1(left)
    result2 = sub_box2(right)
    output = np.concatenate([result1, result2])
    return output


# spbox
def spbox(arr):
    a = np.array([3, 0, 2, 1])
    reordered_arr = np.zeros_like(arr)
    reordered_arr[a] = arr
    return reordered_arr


# 分割
def split(arr):
    middle = len(arr) // 2
    left = arr[:middle]
    right = arr[middle:]
    return left, right


# 循环左移
def left_shift(arr):
    arr = np.roll(arr, -1)
    return arr


# 密钥生成算法 (未测试）
def generate_key(arr):
    arr = key_permutation(np.array(arr))
    # 生成密钥1
    left, right = split(arr)
    left = left_shift(left)
    right = left_shift(right)
    middle1 = np.concatenate((left, right))

    k1 = compression_permutation_box(middle1)
    # 生成密钥2
    left = left_shift(left)
    right = left_shift(right)
    middle2 = np.concatenate((left, right))
    k2 = compression_permutation_box(middle2)
    return k1, k2


# F函数
def f_function(input_arr, k):
    input_arr = expansion_permutation_box(input_arr)
    arr = np.bitwise_xor(input_arr, k)
    arr = sub(arr)
    arr = spbox(arr)
    return arr


# 加密算法
def encode(key, content):
    content = initial_permutation(content)
    left, right = split(content)
    k1, k2 = generate_key(key)
    temp1 = f_function(right, k1)
    right2 = np.bitwise_xor(temp1, left)
    left2 = right
    temp2 = f_function(right2, k2)
    left3 = np.bitwise_xor(left2, temp2)
    arr = np.concatenate([left3, right2])
    return final_permutation(arr)


# 解密
def decode(key, content):
    content = initial_permutation(content)
    left, right = split(content)
    k1, k2 = generate_key(key)
    temp1 = f_function(right, k2)
    right2 = np.bitwise_xor(temp1, left)
    left2 = right
    temp2 = f_function(right2, k1)
    left3 = np.bitwise_xor(left2, temp2)
    return final_permutation(np.concatenate([left3, right2]))


# 字符串转为二进制数组
def string_change(string):
    if not isinstance(string, bytes):  # 检查 string 是否是 bytes 对象
        string = string.encode('ISO-8859-1')
    arr = np.array([format(c, '08b') for c in string]).tolist()
    arr = [np.array(list(c)) for c in arr]
    arr = [c.astype(int) for c in arr]
    return arr


# 二进制数组加密为字符串
def encode_str(key, string):
    arr = string_change(string)
    # print (arr)
    en_arr = [encode(key, c) for c in arr]
    # print(en_arr)
    en_arr = [c.astype(str) for c in en_arr]
    # print(en_arr)
    en_arr = [''.join(c.tolist()) for c in en_arr]
    en_arr = [int(c, 2) for c in en_arr]
    obj_string = bytes(en_arr)
    # obj_string = str(obj_string)
    return obj_string.decode('ISO-8859-1')


#
def decode_str(key, string):
    arr = string_change(string)
    de_arr = [decode(key, c) for c in arr]
    # print(de_arr)
    de_arr = [c.astype(str) for c in de_arr]
    # print(de_arr)
    de_arr = [''.join(c.tolist()) for c in de_arr]
    de_arr = [int(c, 2) for c in de_arr]
    obj_string = bytes(de_arr)
    # print(type(obj_string.decode('ISO-8859-1')))
    return obj_string.decode('ISO-8859-1')


# 文件加密
def txt_encode(filename, key):
    with open(filename, "r", encoding="ISO-8859-1") as f:
        content = f.read()
        content = encode_str(key, content)
    with open("output1.txt", "wb") as f:  # 注意这里是 "wb"
        f.write(content)


# 文件解密
def txt_decode(filename, key):
    with open(filename, "rb") as f:  # 注意这里是 "rb"
        content = f.read()
        content = decode_str(key, content)
    with open("output_decoded.txt", "w", encoding="ISO-8859-1") as f:
        f.write(content)


# 暴力破解
def brute_force_sdes(ciphertext, plaintext):
    possible_keys = []
    # Try all possible 10-bit keys
    for key in range(1024):  # 2^10 = 1024 possible keys
        binary_key = np.array([int(b) for b in format(key, '010b')])  # Convert to 10-bit binary array
        encrypted_text = encode(binary_key, plaintext)
        if np.array_equal(encrypted_text, ciphertext):
            possible_keys.append(binary_key)
    return possible_keys


from concurrent.futures import ProcessPoolExecutor
import json
from itertools import product

# 尝试找出所有的密钥碰撞
key_collisions = {}
# Initialize a list to store the collided keys for each plaintext-ciphertext pair
collided_keys = {}


# Define a function to handle each plaintext-ciphertext pair
def handle_pair_multiprocess(plaintext, ciphertext):
    local_key_collisions = {}
    local_collided_keys = {}

    plaintext_bin = np.array([int(b) for b in format(plaintext, '08b')])
    ciphertext_bin = np.array([int(b) for b in format(ciphertext, '08b')])

    # Loop over all possible 10-bit keys
    for key in range(1024):
        binary_key = np.array([int(b) for b in format(key, '010b')])

        encrypted_text = encode(binary_key, plaintext_bin)
        if np.array_equal(encrypted_text, ciphertext_bin):
            key_int = int("".join(map(str, binary_key)), 2)
            local_key_collisions[key_int] = local_key_collisions.get(key_int, 0) + 1

            pair_str = f"{plaintext:08b}-{ciphertext:08b}"
            if pair_str not in local_collided_keys:
                local_collided_keys[pair_str] = []
            local_collided_keys[pair_str].append(key_int)

    return local_key_collisions, local_collided_keys


def brute_force_all_collisions_multiprocess():
    global key_collisions, collided_keys
    key_collisions = {}
    collided_keys = {}

    with ProcessPoolExecutor(max_workers=4) as executor:
        pairs = list(product(range(256), repeat=2))
        futures = [executor.submit(handle_pair_multiprocess, *pair) for pair in pairs]

        for future in futures:
            local_key_collisions, local_collided_keys = future.result()

            # Aggregate the results in the main process
            for key, count in local_key_collisions.items():
                key_collisions[key] = key_collisions.get(key, 0) + count
            for pair, keys in local_collided_keys.items():
                collided_keys[pair] = collided_keys.get(pair, []) + keys


# 将结果写入文件
def write_results_to_file(file_path, collided_keys):
    # Convert the collided_keys dictionary keys to strings as JSON keys need to be strings
    str_collided_keys = {str(k): v for k, v in collided_keys.items()}

    results = {
        'collided_keys': str_collided_keys
    }

    with open(file_path, 'w') as file:
        json.dump(results, file, indent=4)


def corrected_main():
    brute_force_all_collisions_multiprocess()
    write_results_to_file("collisions.json", collided_keys)

# # Protect the execution of multiprocessing code with if __name__ == '__main__': block
# if __name__ == '__main__':
#     corrected_main()
