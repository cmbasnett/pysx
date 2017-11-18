import lzs
import struct
import array


class Triangle(object):
    def __init__(self, buffer):
        (self.vertex1, self.vertex2, self.vertex3, self.walk, self.u1, self.v1, self.u2, self.v2,
         self.u3, self.v3, texture_and_location) = struct.unpack_from('10BH', buffer, 0)
        self.walk = (self.walk & 0x1f)
        self.texture = (texture_and_location & 0xff80) >> 7 # TODO: these are probably backwards
        self.location = (texture_and_location & 0x7f)


class Normal(object):
    def __init__(self, buffer):
        (self.x, self.y, self.z, self.w) = struct.unpack_from('3hH', buffer, 0)

    def __repr__(self):
        return str((self.x, self.y, self.z, self.w))


class Vertex(object):
    def __init__(self, buffer):
        (self.x, self.y, self.z, self.w) = struct.unpack_from('3hH', buffer, 0)

    def __repr__(self):
        return str((self.x, self.y, self.z, self.w))


class Mesh(object):
    def __init__(self, buffer):
        (triangle_count, vertex_count) = struct.unpack_from('2H', buffer)
        ofs = 4
        self.triangles = []
        self.vertices = []
        self.normals = []
        for i in range(triangle_count):
            self.triangles.append(Triangle(buffer[ofs:ofs + 12]))
            ofs += 12
        for i in range(vertex_count):
            self.vertices.append(Vertex(buffer[ofs:ofs + 8]))
            ofs += 8
        for i in range(vertex_count):
            self.normals.append(Normal(buffer[ofs:ofs + 8]))
            ofs += 8


class Block(object):
    def __init__(self, buffer, offset):
        mesh_offsets = [x for x in array.array('I', buffer[offset:offset + 64]).tolist()]
        self.meshes = []
        for mesh_offset in mesh_offsets:
            self.meshes.append(Mesh(lzs.inflate(buffer, offset + mesh_offset)))


class MAP(object):
    def __init__(self, buffer):
        block_size = 0xb800
        block_count = int(len(buffer) / block_size)
        self.blocks = [Block(buffer, i * block_size) for i in range(block_count)]