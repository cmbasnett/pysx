import struct
import png

TIM_TAG = 16
TIM_VERSION = 0

def chunks(l, n):
    '''Yield successive n-sized chunks from l.'''
    for i in range(0, len(l), n):
        yield l[i:i + n]

class TIM(object):

    class Palette(object):
        def __init__(self, f):
            format = 'IHHHH'
            (length, self.x, self.y, self.width, self.height) = struct.unpack_from(format, f.read(struct.calcsize(format)))
            self.data = list(map(lambda x: x[0], struct.iter_unpack('H', f.read(self.width * self.height * 2))))

        def __getitem__(self, item):
            # TODO: A special case is black pixels (RGB 0,0,0), which by default are treated as transparent by the PlayStation unless the STP bit is set.
            value = self.data[item]
            r = ((value & 0x001f) >> 0) * 8
            g = ((value & 0x03e0) >> 5) * 8
            b = ((value & 0x7c00) >> 10) * 8
            a = 0 if ((value & 0x8000) >> 15) else 255
            return (r, g, b, a)

    def __init__(self, path):
        f = open(path, mode='rb')
        # Header
        format = 'BBxxBxxx'
        (tag, version, flags) = struct.unpack_from(format, f.read(struct.calcsize(format)))
        if tag != TIM_TAG:
            raise Exception('Unhandled version (found: {}, expected {}'.format(tag, TIM_TAG))
        if version != TIM_VERSION:
            raise Exception('Unhandled version (found: {}, expected {}'.format(version, TIM_VERSION))
        self.bpp = [4, 8, 16, 24][flags & 0x3]
        has_palette = bool((flags & 0xC) >> 2)
        # Palette
        if has_palette:
            self.palette = TIM.Palette(f)
        # Image
        format = 'IHHHH'
        (length, x, y, self.width, self.height) = struct.unpack_from(format, f.read(struct.calcsize(format)))
        if self.bpp == 4:
            self.width *= 4
        elif self.bpp == 8:
            self.width *= 2
        elif self.bpp == 24:
            self.width /= 2
        length = (self.bpp * self.width * self.height) * 8
        self.data = f.read(length)

    def export(self, path):
        if self.palette is not None:
            indices = []
            if self.bpp == 4:
                indices = list(map(lambda x: x[0], struct.iter_unpack('B', self.data)))
                # TODO: need to split all the indices into 4-byte pairs
            elif self.bpp == 8:
                indices = list(map(lambda x: x[0], struct.iter_unpack('B', self.data)))
            pixels = list(map(lambda x: self.palette[x], indices))
            pixels = [i for sub in pixels for i in sub] # flatten everything out
            rows = list(chunks(pixels, 4 * self.width)) # separate into rows
            g = open(path, 'wb')
            writer = png.Writer(width=self.width, height=self.height, alpha=True)
            writer.write(g, rows)
        elif self.bpp == 16:
            pass
        elif self.bpp == 24:
            pass
