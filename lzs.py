import struct
import array

def deflate(path, length_min=3):
    f = open(path, "rb")
    buffer = f.read()
    f.close()
    (size,) = struct.unpack_from("<I", buffer, 0)
    if size + 4 != len(buffer):
        raise Exception()
    input_buffer = array.array('B', buffer)
    output_buffer = array.array('B')
    input_offset = 4
    cmd = 0
    bit = 0
    while input_offset < len(input_buffer):
        if bit == 0:
            cmd = input_buffer[input_offset]
            bit = 8
            input_offset += 1
        if cmd & 1:
            output_buffer.append(input_buffer[input_offset])
            input_offset += 1
        else:
            a = input_buffer[input_offset]
            b = input_buffer[input_offset + 1]
            input_offset += 2
            o = a | ((b & 0xf0) << 4)
            l = (b & 0xf) + length_min
            rofs = len(output_buffer) - ((len(output_buffer) - 18 - o) & 0xfff)
            for j in range(l):
                if rofs < 0:
                    output_buffer.append(0)
                else:
                    output_buffer.append(output_buffer[rofs])
                rofs += 1
        cmd >>= 1
        bit -= 1
    return bytes(output_buffer)
