import base64
from Crypto.Cipher import AES

def base64_to_byte(encoded_str):
    return base64.b64decode(encoded_str)

def aes_ecb_encrypt(plaintext : bytes, key : bytes) -> bytes:
    cypher = AES.new(key,AES.MODE_ECB)
    cyphertext = cypher.encrypt(plaintext)
    return cyphertext

def aes_ecb_decrypt(cyphertext : bytes, key : bytes) -> bytes:
    cypher = AES.new(key,AES.MODE_ECB)
    plaintext = cypher.decrypt(cyphertext)
    return plaintext

key = b"YELLOW SUBMARINE"


if __name__ == "__main__":

    with open('7.txt','r') as f:
        file = f.read()
        f.close()

    cypher_bytes=base64_to_byte(file)
    plaintext = aes_ecb_decrypt(cypher_bytes, key)
    print(plaintext.decode('utf-8'))
    assert aes_ecb_encrypt(plaintext, key) == cypher_bytes
