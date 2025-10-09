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
    hamming_distance=0
    if len(bytes_1)!=len(bytes_2):
        print("Le stringhe devono avere la stessa lunghezza")
    else:
        for b1,b2 in zip(bytes_1,bytes_2):
           for i in range(8):
               hamming_distance+=(b1>>i)&0x1^(b2>>i)&0x1
        return hamming_distance
def hex_to_bytes(hex_str):
    return bytes.fromhex(hex_str)
def single_byte_xor(byte_data, key):
    return bytes([b ^ key for b in byte_data])
def find_best_single_byte_xor(byte_data,n):#ritorna le prime 3 n migliori chiavi
    result=[]
    for key in range(256):
        decoded = single_byte_xor(byte_data, key)
        score = score_text(decoded)      
        result.append((key,score))
    result.sort(key=lambda x: x[1],reverse=True)
    return result[:n]
def CreateBytesList(size, bytes_array,num_blocks):
    blocks = []
    required_length = size * num_blocks
    if len(bytes_array) < required_length:
        print("ERRORE FUNZIONE CREATE_BYTE_LIST\n\n\n")
        exit()  
    for i in range(0, required_length+1, size):
        block = bytes_array[i:i + size]
        blocks.append(block)
        num_blocks=num_blocks-1
        if(num_blocks==0):
            break
    return blocks
def found_keysize(cypher_bytes,num_block):#num_block=n_blocchi di calcolo hamming
    if num_block%2 != 0:
        print("ERRORE FUNZIONE FOUND_KEYSIZE\n\n\n")
        exit()
    result=dict()
    for keysize in range(2,40):
        hamm_distance=0
        blocks=CreateBytesList(keysize,cypher_bytes,num_block)
        for i in range(0,num_block-1,2):
            hamm_distance+=hamming_distance(blocks[i],blocks[i+1])
        hamm_distance=hamm_distance/keysize
        result[keysize]=hamm_distance
    return sorted(result.items(),key=lambda item: item[1])
def single_byte_encrypted_group(cypher_bytes,keysize):
    number_of_blocks_max=int(len(cypher_bytes)/keysize)
    blocks=CreateBytesList(keysize,cypher_bytes,number_of_blocks_max)        
    final_byte=[]
    for j in range(keysize):
        group_of_byte=[]
        for x in range(number_of_blocks_max):
            group_of_byte.append(blocks[x][j])
        final_byte.append(group_of_byte)
    return final_byte
def repeating_key_xor(byte_to_encode,key):
    i=0
    j=0
    xor=bytearray(len(byte_to_encode))
    for b in byte_to_encode:
        xor[j]=b^key[i]
        j=j+1
        i=i+1
        if i>=len(key):
            i=i%len(key)
    return xor





with open('canzone_encripted.txt','r') as f:
    file = f.read()
    f.close()

cypher_bytes=hex_to_bytes(file)
print(len(cypher_bytes))



num_block=28#dev'essere pari,vedi found_keysize
print(len(cypher_bytes))
founded_keysize=found_keysize(cypher_bytes,num_block)#PER OGNI KEYSIZE CALCOLA LO SCORE HAMMING
print(founded_keysize)
#print(cypher_bytes)
print('\n\n')
for i in range(3):
    keysize=founded_keysize[i][0]
    single_byte_encripted=single_byte_encrypted_group(cypher_bytes,keysize)
    key=[]
    for x in range(keysize):
        #print(keysize)
        #print(single_byte_encripted[x])
        group=bytes(single_byte_encripted[x])
        # print(group)
        result=find_best_single_byte_xor(group,3)
        # print(result)
        key.append(result[0][0])
    if keysize == 38:
        print(repeating_key_xor(cypher_bytes,bytes(key)).decode('utf-8'))
        print(bytes(key).decode('utf-8'))
    

