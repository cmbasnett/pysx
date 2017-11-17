#!/usr/bin/env python3

import struct
import array
import argparse
import sys

def inflate(buffer, length_min=3):
    (size,) = struct.unpack_from("<I", buffer, 0)
    if size + 4 != len(buffer):
        raise Exception('size ({}) exceeds length of buffer ({})'.format(size, len(buffer)))
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
    return bytearray(output_buffer)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('lzs')
    parser.add_argument('-o', '--output', action='store', dest='output')
    args = parser.parse_args()
    if args.output is None:
        sys.stdout.buffer.write(inflate(sys.stdin.buffer.read()))
    else:
        with open(args.output, 'wb') as f:
            f.write(inflate(sys.stdin.buffer.read()))