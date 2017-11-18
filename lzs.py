#!/usr/bin/env python3

import struct
import array
import argparse
import sys

def inflate(buffer, offset=0, length_min=3):
    (size,) = struct.unpack_from("I", buffer, offset)
    end = offset + size + 4
    offset += 4
    output = bytearray()
    cmd = 0
    bit = 0
    while offset <= end:
        if bit == 0:
            cmd = buffer[offset]
            bit = 8
            offset += 1
        if cmd & 1:
            output.append(buffer[offset])
            offset += 1
        else:
            a = buffer[offset]
            b = buffer[offset + 1]
            offset += 2
            o = a | ((b & 0xf0) << 4)
            l = (b & 0xf) + length_min
            raw_ofs = len(output) - ((len(output) - 18 - o) & 0xfff)
            for j in range(l):
                if raw_ofs < 0:
                    output.append(0)
                else:
                    # TODO: repeated run logic got lost?
                    output.append(output[raw_ofs])
                    raw_ofs += 1
        cmd >>= 1
        bit -= 1
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser('lzs')
    parser.add_argument('-o', '--output', action='store', dest='output')
    args = parser.parse_args()
    if args.output is None:
        sys.stdout.buffer.write(inflate(sys.stdin.buffer.read()))
    else:
        with open(args.output, 'wb') as f:
            f.write(inflate(sys.stdin.buffer.read()))