##Encrypt it, under the key "ICE", using repeating-key XOR.

string="Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key="ICE"

expected_result="0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

def hex_to_bytes(hex_str):
    return bytes.fromhex(hex_str)

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

string_byte=bytes(string,encoding='utf-8')
key_byte=bytes(key,encoding='utf-8')
xor=repeating_key_xor(string_byte,key_byte)
print(bytes(xor))
res_byte=hex_to_bytes(expected_result)
print(res_byte)
if xor==res_byte:
    print('giustooo')
if xor.hex()==expected_result:
    print('si u mest')
