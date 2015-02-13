import struct

def isBox(content):
    return content.__class__.__name__ == 'Box'

class Box:
    def __init__(self, kind=None, content=None):
        self.kind    = kind    if kind    is not None else ''
        self.content = content if content is not None else []

    def serialize(self):
        serializedContent = ''
        for item in self.content:
            if isBox(item):
                serializedContent += item.serialize()
            else:
                # string
                serializedContent += item

        data = struct.pack('>I', 8 + len(serializedContent))
        data += '%-4s' % self.kind # pad to 4 bytes
        data += serializedContent

        return data

    def deserialize(self, data, pos=0):
        self.size = struct.unpack('>I', data[pos:pos+4])[0]
        pos +=4 
        self.kind = data[pos:pos+4]
        self.kind = str.rstrip(self.kind)
        pos +=4 

        # now read the content
        if self.kind not in ('cat', 'head'):
            self.content = [data[pos:pos+self.size-8]]
        else:
            size = self.size - 8
            while size > 0:
                boxSize = struct.unpack('>I', data[pos:pos+4])[0]
                size -= boxSize

                box = Box()
                box.deserialize(data, pos)
                pos += boxSize

                self.content.append(box)
    
    def __repr__(self):
        return self.fmt(0)

    def fmt(self, indent):
        serializedContent = ''
        serializedContentSize = 0

        leaf = False
        if len(self.content) == 1 and not isBox(self.content[0]):
            leaf = True

        if not leaf:
            serializedContent += '[\n'

        for item in self.content:
            if isBox(item):
                serializedContent += item.fmt(indent + 4)
                serializedContentSize += len(item.serialize())
            else:
                # string
                serializedContent += item
                serializedContentSize += len(item)

        if not leaf:
            serializedContent += 2* ' ' + ' ' * indent + ']'

        data = []
        data.append('{')
        data.append('  size = %d' % (8 + serializedContentSize))
        data.append('  type = %s' % self.kind) # pad to 4 bytes
        data.append('  content = %s' % serializedContent)
        data.append('}')

        out = ''
        for item in data:
            out += ' ' * indent + item + '\n'

        return out

if __name__ == '__main__':
    blackBox = Box(kind='body', content=['black'])
    noseBox  = Box(kind='nose', content=['red'])
    eyesBox  = Box(kind='eyes', content=['green'])

    headBox = Box(kind='head', content=[eyesBox, noseBox])
    catBox  = Box(kind='cat',  content=[headBox, blackBox])

    print catBox

    byteVec = catBox.serialize()
    catBox2 = Box()
    catBox2.deserialize(byteVec)

    print catBox2
