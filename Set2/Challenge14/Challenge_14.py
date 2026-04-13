import os
import base64
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

def encryption_oracle(user_input):
    data = random_prefix + user_input + base64.b64decode(string)
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

    test_payload = b"A" * (block_len * 2)
    final_pad_len = 0
    found = False
    for pad_len in range(block_len):
        cipher = encryption_oracle(b"B" * pad_len + test_payload)
        for i in range(0, len(cipher) - block_len, block_len):
            if cipher[i : i + block_len] == cipher[i + block_len : i + 2 * block_len]:
                start_block = i//16
                final_pad_len = pad_len
                found = True
                break
        if found:
            break
    print(f"Blocco di partenza: {start_block}")
    print(f"Padding necessario: {final_pad_len}")
    print(f"Lunghezza reale del prefisso: {len(random_prefix)}")
    detected = b''
    while True:
        
        block_index = (len(detected) // block_len)
        start = block_index * block_len
        end = start + block_len
        
        data = (b"A" * ((block_len * (block_index+1)) - 1 - len(detected)))  
        lookup = {}
        for i in range(256):
            lookup[encryption_oracle((b'B' * final_pad_len)+ data + detected + bytes([i]))[(start_block * block_len) + start:(start_block * block_len) + end]] = bytes([i])
        
        target = encryption_oracle((b'B' * final_pad_len) + data)[(start_block * block_len) + start : (start_block * block_len) + end ]

        if target in lookup:
            detected += lookup[target]
        else:
            print(detected)
            break

key = random_aes_key()
random_prefix = os.urandom(random.randint(1, 40))
string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
print(base64.b64decode(string))

for _ in range(1):
    test_oracle()
