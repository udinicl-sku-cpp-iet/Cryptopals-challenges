import os
import random
from Cryptodome.Cipher import AES


def random_aes_key():
    return os.urandom(16)

def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    padding_len = block_size - (len(data) % block_size)
    padding = bytes([padding_len] * padding_len)
    return data + padding

def aes_ecb_encrypt(plaintext : bytes, key : bytes) -> bytes:
    cypher     = AES.new(key,AES.MODE_ECB)
    cyphertext = cypher.encrypt(plaintext)
    return cyphertext
def aes_ecb_decrypt(cyphertext : bytes, key : bytes) -> bytes:
    cypher    = AES.new(key,AES.MODE_ECB)
    plaintext = cypher.decrypt(cyphertext)
    return plaintext
def repeating_key_xor(byte_to_encode, key):
    return bytes(
        b ^ key[i % len(key)] for i, b in enumerate(byte_to_encode)
    )
def aes_cbc_encrypt(plaintext : bytes, key : bytes, iv : bytes) -> bytes:
    blocks = []
    cyphertext = b''
    for i in range(0, len(plaintext), 16):
        blocks.append(plaintext[i:i+16])
    for i, block in enumerate(blocks):
        if i == 0:
            xor = repeating_key_xor(block, iv)
        else:
            xor = repeating_key_xor(block, prev)
        prev = aes_ecb_encrypt(xor,key)
        cyphertext += prev
    return cyphertext

def aes_cbc_decrypt(cyphertext : bytes, key : bytes, iv : bytes) -> bytes:
    blocks = []
    plaintext = b''
    for i in range(0, len(cyphertext), 16):
        blocks.append(cyphertext[i:i+16])
    for i in range(len(blocks)):
        block = aes_ecb_decrypt(blocks[i],key)
        if i == 0:
            xor = repeating_key_xor(block, iv)
        else:
            xor = repeating_key_xor(block, blocks[i-1])
        plaintext += xor
    return plaintext

def encryption_oracle(user_input):
    key = random_aes_key()

    prefix = os.urandom(random.randint(5, 10))
    suffix = os.urandom(random.randint(5, 10))

    data = prefix + user_input + suffix
    data = pkcs7_pad(data,16)

    if random.randint(0, 1) == 0:
        ciphertext = aes_ecb_encrypt(data, key)
        mode = "ECB"
    else:
        iv = os.urandom(16)
        ciphertext = aes_cbc_encrypt(data, key, iv)
        mode = "CBC"
    return ciphertext, mode

def detect_mode(ciphertext, block_size=16):
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]

    if len(blocks) != len(set(blocks)):
        return "ECB"
    return "CBC"

def test_oracle():
    data = b"A" * 64  # input ripetitivo

    ciphertext, real_mode = encryption_oracle(data)
    detected_mode = detect_mode(ciphertext)


    print(f"Real: {real_mode}")
    print(f"Detected: {detected_mode}")

    if real_mode != detected_mode:
        print("sbagliato")

for _ in range(10):
    test_oracle()
