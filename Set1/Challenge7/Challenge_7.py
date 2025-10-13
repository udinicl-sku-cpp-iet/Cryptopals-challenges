import base64
from Cryptodome.Cipher import AES

def base64_to_byte(encoded_str):
    return base64.b64decode(encoded_str)

key = b"YELLOW SUBMARINE"


if __name__ == "__main__":

    with open('7.txt','r') as f:
        file = f.read()
        f.close()

    cipher_bytes=base64_to_byte(file)
    cipher = AES.new(key,AES.MODE_ECB)
    plaintext = cipher.decrypt(cipher_bytes)
    print(plaintext.decode('utf-8'))
