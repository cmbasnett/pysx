import tim
import bcx
import txz
import map

tim.TIM(r'V:\MENU\PCLOUD.TIM').export('D:\pysx\export\.png')
#bcx.BCX('V:\FIELD\CLOUD.BCX')
#txz.TXZ(open(r'V:\WORLD\WM0.TXZ', 'rb').read())
map = map.MAP(open(r'V:\WORLD\WM3.MAP', 'rb').read())

# TODO: export *one* of the meshes in the blocks

with open('C:/Users/Colin/Desktop/WM3.obj', 'w') as f:
    vertex_count = 0
    for (i, block) in enumerate(map.blocks):
        block_x = (i % 9) * 32768
        block_z = (i // 9) * 32768
        f.write('o block{}\n'.format(i))
        for (j, mesh) in enumerate(block.meshes):
            x = block_x + ((j % 4) * 8192)
            z = block_z + ((j // 4) * 8192)
            for v in mesh.vertices:
                f.write('v {} {} {}\n'.format((v.x + x) / 8192, v.y / 8192, (v.z + z) / 8192))
            for t in mesh.triangles:
                f.write('f {} {} {}\n'.format(t.vertex1 + 1 + vertex_count, t.vertex2 + 1 + vertex_count, t.vertex3 + 1 + vertex_count))
            for n in mesh.normals:
                f.write('vn {} {} {}\n'.format(n.x, n.y, n.z))
            vertex_count += len(mesh.vertices)
