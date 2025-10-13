def hex_to_bytes(hex_str):    
    return bytes.fromhex(hex_str)

def is_ecb(cipher : bytes) -> bool:
    blocks = [cipher[i:i+16] for i in range(0,len(cipher),16)]
    for i in range(len(blocks)-1):
        for j in range(i+1,len(blocks)):
            if blocks[i] == blocks[j]:
                return True
    return False

if __name__ == "__main__":
    with open("8.txt","r") as f:
        cipher_file = f.readlines()
        f.close()
        
    for i in range(len(cipher_file)):
        cipher_file[i] = hex_to_bytes(cipher_file[i])
        if is_ecb(cipher_file[i]):
            print(i+1)
        
