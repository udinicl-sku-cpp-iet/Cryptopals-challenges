##Encrypt it, under the key "ICE", using repeating-key XOR.

string=\
"""\
Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal\
"""
key="ICE"

expected_result="""\
0b3637272a2b2e63622c2e69692a23693a2a3\
c6324202d623d63343c2a2622632427276527\
2a282b2f20430a652e2c652a3124333a653e2\
b2027630c692b20283165286326302e27282f\
"""

def hex_to_bytes(hex_str):
    return bytes.fromhex(hex_str)

def repeating_key_xor(byte_to_encode, key):
    return bytes(
        b ^ key[i % len(key)] for i, b in enumerate(byte_to_encode)
    )


string_byte = bytes(string,encoding='utf-8')
key_byte    = bytes(key,   encoding='utf-8')
xor         = repeating_key_xor(string_byte,key_byte)

if xor.hex() == expected_result:
    print('Well Done.')
