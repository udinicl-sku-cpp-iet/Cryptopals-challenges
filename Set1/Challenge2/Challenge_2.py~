#Write a function that takes two equal-length buffers and produces their XOR combination.
hex_val_1='1c0111001f010100061a024b53535009181c'
hex_val_2='686974207468652062756c6c277320657965'

result='746865206b696420646f6e277420706c6179'

def hex_to_byte(hex):
#    print(type(hex))
    byte=bytes.fromhex(hex)
#    print(byte)
#    print(type(byte))
    return byte

def fixed_xor(byte_1,byte_2):
    if len(byte_1)!=len(byte_2):
        print('le stringhe devono avere la stessa lunghezza')
    else:
        xor=bytearray(len(byte_1))
        for i in range(len(byte_1)):
            xor[i]=byte_1[i]^byte_2[i]
        return xor

byte_1=hex_to_byte(hex_val_1)
byte_2=hex_to_byte(hex_val_2)
print(fixed_xor(byte_1,byte_2))
if fixed_xor(byte_1,byte_2).hex()==result:
    print('giustoooo')

