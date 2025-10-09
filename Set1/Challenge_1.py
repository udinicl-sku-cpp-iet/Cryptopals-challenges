#convert hex to base 64
import base64

hex_val = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
base64_val='SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

def hex_to_byte(hex):
#    print(type(hex))
    byte=bytes.fromhex(hex)
#    print(byte)
#    print(type(byte))
    return byte

def byte_to_base64(byte):
    base64_conv=base64.b64encode(byte)
#    print(type(base64_conv))
    return base64_conv

byte=hex_to_byte(hex_val)
#print(byte)
base64=byte_to_base64(byte)
#print(base64)

if base64==bytes(base64_val,'utf-8'):
    print('esattoooo')
