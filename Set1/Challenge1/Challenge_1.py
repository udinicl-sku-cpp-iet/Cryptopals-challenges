#convert hex to base 64
import base64

hex_val = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
base64_val='SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

def hex_to_byte(hex):
    return bytes.fromhex(hex)

def byte_to_base64(byte):
    return base64.b64encode(byte)

byte=hex_to_byte(hex_val)
base64=byte_to_base64(byte)


if base64==bytes(base64_val,'utf-8'):
    print('Well done.')
