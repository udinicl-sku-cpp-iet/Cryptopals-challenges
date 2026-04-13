import os
import base64
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

def encryption_oracle(user_input):
    data = user_input + base64.b64decode(string)
    data = pkcs7_pad(data,16)
    return aes_ecb_encrypt(data, key)


def detect_mode(ciphertext, block_size=16):
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    if len(blocks) != len(set(blocks)):
        return "ECB"
    return "CBC"

def test_oracle():
    data = b"" 
    ciphertext = encryption_oracle(data)
    ciphertext_len = len(ciphertext)
    
    block_len = 0
    while block_len == 0:
        data = data + b"A"
        ciphertext = encryption_oracle(data)
        if len(ciphertext) > ciphertext_len:
            block_len = len(ciphertext) - ciphertext_len

    detected = b''
    while True:
        
        block_index = len(detected) // block_len
        start = block_index * block_len
        end = start + block_len
        
        data = (b"A" * ((block_len * (block_index+1)) - 1 - len(detected))) 
        lookup = {}
        for i in range(256):
            lookup[encryption_oracle(data + detected + bytes([i]))[start:end]] = bytes([i])
        
        target = encryption_oracle(data)[start:end]

        if target in lookup:
            detected += lookup[target]
        else:
            print(detected)
            break

key = random_aes_key()
string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
print(base64.b64decode(string))

for _ in range(1):
    test_oracle()
