import os
import base64
import random
from Cryptodome.Cipher import AES

class InvalidPaddingException(Exception):
    pass

def random_aes_key():
    return os.urandom(16)

def strip_pkcs7_pad(data: bytes) -> bytes:
    padding_len = data[-1]
    if padding_len == 0 or padding_len > len(data):
        raise InvalidPaddingException("Padding non valido: lunghezza fuori range.")

    padding_bytes = data[-padding_len:]
    
    expected_padding = bytes([padding_len] * padding_len)
    
    if padding_bytes != expected_padding:
        raise InvalidPaddingException("Padding non valido: byte non corrispondenti.")
        
    return data[:-padding_len]

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

def first():
    strings = ["MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
               "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
               "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
               "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
               "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
               "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
               "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
               "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
               "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
               "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]
    stringa = base64.b64decode(random.choice(strings))
    return aes_cbc_encrypt(pkcs7_pad(stringa, 16), key, iv),iv

def second(cyphertext : bytes):
    try:
        strip_pkcs7_pad(aes_cbc_decrypt(cyphertext, key, iv))
    except InvalidPaddingException as e:
        return False
    return True



key = random_aes_key()
iv  = bytes([0] * 16)


cypher = first() [0]
testo_decifrato = b""

num_blocks = len(cypher) // 16

for block_idx in range(num_blocks):

    start = block_idx * 16
    end = start + 16
    block = cypher[start:end]
    
    if block_idx == 0:
        pred_block = iv
    else:
        pred_block = cypher[start - 16 : start]

    intermediate = bytearray(16)
    decrypted_block = bytearray(16)


    for padding_len in range(1, 17):

        byte_idx = 16 - padding_len 
        
        my_block = bytearray(16)
        
        for m in range(byte_idx + 1, 16):
            my_block[m] = intermediate[m] ^ padding_len
            
        for i in range(256):
            my_block[byte_idx] = i
            if second(my_block + block) == True:
                
                # --- GESTIONE DEI FALSI POSITIVI ---
                # Se stiamo cercando il padding \x01, potremmo essere stati sfortunati
                # e aver beccato un padding \x02\x02 naturale. Alteriamo il byte precedente
                # per distruggere l'eventuale \x02\x02 e vedere se regge come \x01.
                if padding_len == 1:
                    my_block[byte_idx - 1] ^= 1 
                    if second(my_block + block) == False:
                        continue # Era un falso positivo, continuiamo a cercare
                # -----------------------------------
                
                # JACKPOT! Calcoliamo l'intermediate
                intermediate_state = padding_len ^ i
                intermediate[byte_idx] = intermediate_state
                
                # Calcoliamo il VERO plaintext usando il vero blocco precedente
                decrypted_block[byte_idx] = intermediate_state ^ pred_block[byte_idx]
                break

    # Aggiungiamo il blocco decifrato al testo totale
    testo_decifrato += decrypted_block

print("\n--- TESTO DECIFRATO COMPLETAMENTE ---")
# Rimuoviamo il vero padding alla fine
print(strip_pkcs7_pad(testo_decifrato).decode())
