import os
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

def parse_cookie(cookie : str) -> dict:
    profile = {}
    for s in cookie.split("&"):
        key,value = s.split("=")
        profile[key] = value
    return profile

def profile_for(mail : str) -> str:
    global uid
    uid = uid + 1
    return "email=" + mail.replace("&","").replace("=","") + f"&uid={uid}&role=user"

uid = 10
key = random_aes_key()

    

## 1. Get a block that decrypts to "admin" + PKCS7 padding
# We want: [6 bytes: "email="][10 bytes: padding][16 bytes: "admin" + padding]
# "admin" is 5 bytes. 16 - 5 = 11. Padding byte is \x0b (11).
pad_len = 16 - len("admin")
admin_payload = "A" * 10 + "admin" + chr(pad_len) * pad_len
cipher_1 = aes_ecb_encrypt(pkcs7_pad(profile_for(admin_payload).encode(),16), key)

# The 'admin' block is the second block (indices 16 to 32)
admin_block = cipher_1[16:32]


## 2. Get a ciphertext that ends exactly at "role="
# Target structure: "email=AAA@bb.com&uid=10&role="
# Length: 6 + email_len + 8 (for &uid=10&) + 5 (for role=) = 19 + email_len
# To make 19 + email_len = 32 (two full blocks), email_len must be 13.
email_prefix = "marco@udi.com" # 13 chars
cipher_2 = aes_ecb_encrypt(pkcs7_pad(profile_for(email_prefix).encode(),16), key)

# cipher_2 currently ends with a block for "user" + padding.
# We cut that off and paste our admin_block.
# Block 0: email=marco@udi.
# Block 1: com&uid=10&role=
# Block 2: user + padding (Discard this)
pasted_cipher = cipher_2[0:32] + admin_block



decrypted_bytes = aes_ecb_decrypt(pasted_cipher, key)

padding_len = decrypted_bytes[-1]
final_plain = decrypted_bytes[:-padding_len].decode()

print(f"Malicious Query String: {final_plain}")
print("Final Profile Object:")
print(parse_cookie(final_plain))

