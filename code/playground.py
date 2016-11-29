import time
from enum import Enum

BLOCK_TYPE = {
    0 : "STREAMINFO",
    1 : "PADDING",
    2 : "APPLICATION",
    3 : "SEEKTABLE",
    4 : "VORBIS_COMMENT",
    5 : "CUESHEET",
    6 : "PICTURE",
}

def bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break

def intToByte(b):
    return "{0:08b}".format(b)

def byteToASCII(b):
    n = int('0b' + b, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        if self.name:
            print('[%s]' % self.name),
        print('Elapsed: %s' % (time.time() - self.tstart))

def getFlacHeader(data):
    s = ""
    for i in range(4):
        s += byteToASCII(data[i])
    return s

def getMetaBlockHeader(data, cursor):
    metaBlockHeader = ''
    return (data[cursor][0] == '1', BLOCK_TYPE[int('0b' + data[cursor][1:8], 2)], int('0b' + data[cursor + 1] + data[cursor + 2] + data[cursor + 1]))


def main():
    with Timer("Reading Flac File"):
        filename = "01 - The Post War Dream.flac"
        data = []
        for b in bytes_from_file(filename):
            data.append(intToByte(b))
    print(getFlacHeader(data))
    print(getMetaBlockHeader(data, 1))


if __name__ == '__main__':
    main()
