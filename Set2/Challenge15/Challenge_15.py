class InvalidPaddingException(Exception):
    pass

def strip_pkcs7_padding(data: bytes) -> bytes:
    padding_len = data[-1]
    if padding_len == 0 or padding_len > len(data):
        raise InvalidPaddingException("Padding non valido: lunghezza fuori range.")

    padding_bytes = data[-padding_len:]
    
    expected_padding = bytes([padding_len] * padding_len)
    
    if padding_bytes != expected_padding:
        raise InvalidPaddingException("Padding non valido: byte non corrispondenti.")
        
    return data[:-padding_len]

try:
    print(strip_pkcs7_padding(b"ICE ICE BABY\x04\x04\x04\x04"))
except InvalidPaddingException as e:
    print(e)

try:
    print(strip_pkcs7_padding(b"ICE ICE BABY\x05\x05\x05\x05"))
except InvalidPaddingException as e:
    print(e)

try:
    print(strip_pkcs7_padding(b"ICE ICE BABY\x01\x02\x03\x04"))
except InvalidPaddingException as e:
    print(e)
