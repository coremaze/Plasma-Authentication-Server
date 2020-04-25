PLASMA_CLIENT_KEY = [  4,  21, 132,  64,  32, 132, 243, 132,  17, 177,  43, 132, 101,  42,  44, 150]
PLASMA_SERVER_KEY = [ 37, 124,   3, 213, 190,  48, 142,  34,   7,  77, 143, 210, 201,  97,  86,  23]

def get_swap_index(index, buffer_size, key):
    return (key[index % len(key)] + index) % buffer_size

def decrypt(buffer, key):
    buffer = buffer[:]
    if type(buffer) == bytes:
        buffer = bytearray(buffer)
    elif type(buffer) != bytearray:
        raise ValueError('buffer must be bytes or bytearray')
    for i in range(len(buffer)-1, -1, -1):
        swap_index = get_swap_index(i, len(buffer), key)
        buffer[i] = (buffer[i] - i) & 0xFF
        buffer[i], buffer[swap_index] = buffer[swap_index], buffer[i]
    return buffer

def encrypt(buffer, key):
    buffer = buffer[:]
    if type(buffer) == bytes:
        buffer = bytearray(buffer)
    elif type(buffer) != bytearray:
        raise ValueError('buffer must be bytes or bytearray')
    for i in range(len(buffer)):
        swap_index = get_swap_index(i, len(buffer), key)
        buffer[i], buffer[swap_index] = buffer[swap_index], buffer[i]
        buffer[i] = (buffer[i] + i) & 0xFF
    return buffer

def hexdump(data):
    result = []
    for e in data:
        result.append(f'{e:02X}')
    return ''.join(result)

def unhexdump(data):
    result = []
    for i in range(0, len(data), 2):
        val = int(data[i:i+2], base=16)
        result.append(val)
    return bytes(result)
