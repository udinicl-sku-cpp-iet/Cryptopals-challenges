cypher_text="0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"


def hex_to_bytes(hex):
#    print(type(hex))
    byte=bytes.fromhex(hex)
#    print(byte)
#    print(type(byte))
    return byte

# def score_text2(text):
#     # Definisci la tua funzione di punteggio qui
#     # Ad esempio, puoi usare la frequenza delle lettere in inglese
#     # Questa è una funzione di esempio che assegna un punteggio basato sulla presenza di caratteri ASCII stampabili
#     return sum([1 if 32 <= c <= 126 else 0 for c in text])



cypher_bytes=hex_to_bytes(cypher_text)
print(len(cypher_bytes))
founded_keysize=found_keysize(cypher_bytes,num_block)#PER OGNI KEYSIZE CALCOLA LO SCORE HAMMING
print(founded_keysize)
print(cypher_bytes)
print('\n\n')
for i in range(3):
    keysize=founded_keysize[i][0]
    single_byte_encripted=single_byte_encrypted_group(cypher_bytes,keysize)
    key=[]
    for x in range(keysize):
        print(keysize)
        print(single_byte_encripted[x])
        group=bytes(single_byte_encripted[x])
        print(group)
        result=find_best_single_byte_xor(group,3)
        print(result)
        key.append(result[0][0])
    print(bytes(key))
    print("\n\n")







