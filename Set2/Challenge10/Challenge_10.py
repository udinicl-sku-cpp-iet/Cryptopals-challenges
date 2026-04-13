from Cryptodome.Cipher import AES
import base64


def base64_to_byte(encoded_str):
    return base64.b64decode(encoded_str)

def repeating_key_xor(byte_to_encode, key):
    return bytes(
        b ^ key[i % len(key)] for i, b in enumerate(byte_to_encode)
    )

def aes_ecb_encrypt(plaintext : bytes, key : bytes) -> bytes:
    cypher     = AES.new(key,AES.MODE_ECB)
    cyphertext = cypher.encrypt(plaintext)
    return cyphertext

def aes_ecb_decrypt(cyphertext : bytes, key : bytes) -> bytes:
    cypher    = AES.new(key,AES.MODE_ECB)
    plaintext = cypher.decrypt(cyphertext)
    return plaintext

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

if __name__ == "__main__":
    
    iv = bytes([0] * 16)
    key = b"YELLOW SUBMARINE"

    plaintext = b'TESTCBCMODE12345' * 2
    encrypted = aes_cbc_encrypt(plaintext, key, iv)
    decrypted = aes_cbc_decrypt(encrypted, key, iv)
    assert decrypted == plaintext, "Errore: decrypt(encrypt(x)) != x"
    
    with open("10.txt","r") as f:
        enc_bytes = base64_to_byte(f.read())
        f.close()
    assert len(enc_bytes) % 16 == 0
    
    print(aes_cbc_decrypt(enc_bytes, key, iv).decode('utf-8'))
