import base64

def score_text(text):
    frequency = {
        'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835,
        'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610, 'h': 0.0492888,
        'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490,
        'm': 0.0202124, 'n': 0.0564513, 'o': 0.0596302, 'p': 0.0137645,
        'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357,
        'u': 0.0225134, 'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692,
        'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
    }
    return sum([frequency.get(chr(byte), 0) for byte in text.lower()])

def hamming_distance(bytes_1,bytes_2):
    assert len(bytes_1) == len(bytes_2)
    hamming_distance=0
    for b1,b2 in zip(bytes_1,bytes_2):
        for i in range(8):
            hamming_distance+=(b1>>i)&0x1^(b2>>i)&0x1
    return hamming_distance

def hex_to_bytes(hex_str):    
    return bytes.fromhex(hex_str)
def base64_to_byte(encoded_str):
    return base64.b64decode(encoded_str)



def found_keysize(cipher_bytes : bytes ,max_block : int = 40, max_keysize : int = 1200):#num_block=n_blocchi di calcolo hamming
    result = {}
    for keysize in range(2,max_keysize):
        num_block = len(cipher_bytes) // keysize
        if num_block > max_block : num_block = max_block
        if num_block % 2 != 0    : num_block -= 1
        if num_block < 2         : continue
        blocks = [cipher_bytes[i * keysize:(i + 1) * keysize] for i in range(num_block)]
        distances = []
        for i in range(0,num_block-1):
            dist = hamming_distance(blocks[i],blocks[i+1])
            distances.append(dist / keysize)
        average_distance = sum(distances) / len(distances)
        result[keysize]  = average_distance
    return sorted(result.items(),key=lambda item: item[1])

def choose_keysize(candidates: list, n: int) -> int:
    print(f"\nMigliori {n} keysizes trovati:")
    for i, (keysize, score) in enumerate(candidates[:n], 1):
        print(f"[{i}] Keysize: {keysize}, Score: {score:.4f}")

    while True:
        try:
            scelta = int(input(f"Scegli un'opzione (1-{n}): "))
            if 1 <= scelta <= n:
                return candidates[scelta - 1][0]
            else:
                print(f"Inserisci un numero tra 1 e {n}.")
        except ValueError:
            print("Input non valido. Inserisci un numero intero.")

def repeating_key_xor(byte_to_encode, key):
    return bytes(
        b ^ key[i % len(key)] for i, b in enumerate(byte_to_encode)
    )


def found_best_key(keysize : int, ciphertext : bytes):
    key = bytearray(keysize)
    for i in range(keysize):
        best_score = 0
        best_byte = 0

        block = ciphertext[i::keysize][:((len(ciphertext)//keysize))]  # prendi tutti i byte cifrati dalla i-esima posizione della chiave

        for x in range(256):
            decoded = repeating_key_xor(block, [x])  # funzione che xor-a ogni byte con x
            score = score_text(decoded)
            if score > best_score:
                best_score = score
                best_byte = x

        key[i] = best_byte

    return bytes(key)
    



if __name__ == "__main__":
    assert hamming_distance(b"this is a test" ,b"wokka wokka!!!")==37

    with open('6.txt','r') as f:
        file = f.read()
        f.close()

    cipher_bytes=base64_to_byte(file)
    founded_keysize = found_keysize(cipher_bytes, max_block = 100, max_keysize = 150)
    key             = found_best_key(choose_keysize(founded_keysize, 10), cipher_bytes)
    print(key)
    print(repeating_key_xor(cipher_bytes,key).decode('utf-8'))
