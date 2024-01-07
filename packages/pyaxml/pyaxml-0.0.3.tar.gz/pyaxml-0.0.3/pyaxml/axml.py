from .proto import axml_pb2
from struct import pack, unpack
from androguard.core.resources import public
import re
import ctypes

AXML_HEADER_SIZE=8
AXML_STRING_POOL_HEADER_SIZE=28



class AXMLHeader:

    def __init__(self, type = 0, size = 0, proto=None):
        if proto is None:
            self.proto = axml_pb2.AXMLHeader()
            self.proto.type = type
            self.proto.size = size
            self.proto.header_size = AXML_HEADER_SIZE
        else:
            self.proto = proto
        

    def pack(self):
        return pack("<HHL", self.proto.type, self.proto.header_size, self.proto.size)
    

class AXMLHeader_XML(AXMLHeader):

    def __init__(self, size=0, proto=None):
        if proto is None:
            super().__init__(axml_pb2.RES_XML_TYPE, size)
        else:
            self.proto = proto


class AXMLHeader_STRING_POOL:

    def __init__(self, sb=None, size=0, proto=None):
        if proto:
            self.proto = proto
    
    def compute(self):
        pass

    def pack(self):
        return AXMLHeader(proto=self.proto.hnd).pack() + pack("<LLLLL", self.proto.len_stringblocks, self.proto.len_styleblocks,
                                                                        self.proto.flag, self.proto.stringoffset, self.proto.styleoffset)


##############################################################################
#
#                              STRINGBLOCKS
#
##############################################################################


class StringBlock:

    def __init__(self, data="", size=0, utf8=False, proto=None):
        if proto:
            self.proto = proto
            self.utf8= utf8
        else:
            self.proto = axml_pb2.StringBlock()
            self.proto.data = data
            self.proto.size = size
            self.utf8= utf8
    
    def compute(self):
        self.proto.size = len(self.proto.data)
    
    def pack(self):
        if self.utf8:
            return pack('<BB', self.proto.size, self.proto.size) + self.proto.data.encode('utf-8')[2:] + b'\x00'
        else:
            return pack("<H", self.proto.size) + self.proto.data.encode('utf-16')[2:] + b'\x00\x00'

class StringBlocks:
 
    def __init__(self, proto = None):
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.StringBlocks()
    
    def compute(self):
    
        idx = 0
        for s in self.proto.stringblocks:
            self.proto.stringoffsets.append(idx)
            idx += len(StringBlock(proto=s, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG).pack())

        self.proto.hnd.stringoffset = AXML_STRING_POOL_HEADER_SIZE + \
            len(b"".join(pack('<I', x) for x in self.proto.stringoffsets)) + \
            len(b"".join(pack('<I', x) for x in self.proto.styleoffsets))
        
        self.proto.hnd.styleoffset = 0

        self.proto.hnd.hnd.CopyFrom(AXMLHeader(axml_pb2.RES_STRING_POOL_TYPE, len(self.pack())).proto)
        self.proto.hnd.hnd.header_size = AXML_STRING_POOL_HEADER_SIZE
        self.proto.hnd.len_stringblocks = len(self.proto.stringoffsets)
        self.proto.hnd.len_styleblocks = len(self.proto.styleoffsets)

    def pack(self):
        sb_offsets = b"".join(pack('<I', x) for x in self.proto.stringoffsets)
        st_offsets = b"".join(pack('<I', x) for x in self.proto.styleoffsets)
        sb = self.align(b"".join(StringBlock(proto=elt, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG).pack() for elt in self.proto.stringblocks))
        st = b"" # TODO
        return AXMLHeader_STRING_POOL(proto=self.proto.hnd).pack() + sb_offsets + st_offsets + sb + st
    
    def align(self, buf):
        return buf + b"\x00" * (4 - (len(buf) % 4))

    def get(self, name):
        try:
            index = self.index(name)
        except ValueError:
            index = len(self.proto.stringblocks)
            tmp = StringBlock(data=name, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG)
            tmp.compute()
            self.proto.stringblocks.append(tmp.proto)
        return index
    
    def index(self, name):
        for i in range(0, len(self.proto.stringblocks)):
            if self.proto.stringblocks[i].data == name:
                return i
        raise ValueError

##############################################################################
#
#                              RESOURCEMAP
#
##############################################################################

class ResourceMap:


    def __init__(self, res=[], proto=None):
        if proto is None:
            self.proto = axml_pb2.ResourceMap()
            self.proto.res.extend(res)
            self.proto.header.CopyFrom(AXMLHeader(axml_pb2.RES_XML_RESOURCE_MAP_TYPE, 8).proto)
            self.proto.header.size = AXML_HEADER_SIZE + 4 * len(res)
        else:
            self.proto = proto
    
    def pack(self):
        return AXMLHeader(proto=self.proto.header).pack() + b"".join(pack("<L", x) for x in self.proto.res)

##############################################################################
#
#                              XML ELEMENTS
#
##############################################################################

class AXMLHeader_RES_XML(AXMLHeader):
    def __init__(self, type=0, size=0, proto=None):
        if proto is None:
            super().__init__(type, size + 8, proto)
            self.proto.header_size = 16
        else:
            self.proto = proto 

class AXMLHeader_START_ELEMENT(AXMLHeader_RES_XML):

    def __init__(self, size):
        super().__init__(axml_pb2.RES_XML_START_ELEMENT_TYPE, size)

class AXMLHeader_END_ELEMENT(AXMLHeader_RES_XML):

    def __init__(self, size):
        super().__init__(axml_pb2.RES_XML_END_ELEMENT_TYPE, size)

class AXMLHeader_START_NAMESPACE(AXMLHeader_RES_XML):

    def __init__(self, size):
        super().__init__(axml_pb2.RES_XML_START_NAMESPACE_TYPE, size)

class AXMLHeader_END_NAMESPACE(AXMLHeader_RES_XML):

    def __init__(self, size):
        super().__init__(axml_pb2.RES_XML_END_NAMESPACE_TYPE, size)

class Classical_RES_XML:

    def __init__(self, lineNumber=0, Comment=0xffffffff, proto=None):
        if proto is None:
            self.proto.generic.lineNumber = lineNumber
            self.proto.generic.Comment = Comment
        else:
            self.proto.generic.CopyFrom(proto)

    @property
    def content(self):
        return pack('<LL', self.proto.generic.lineNumber, self.proto.generic.Comment)
    
    def compute(self):
        pass

    def pack(self):
        return self.content

class RES_XML_START_ELEMENT(Classical_RES_XML):

    def __init__(self, namespaceURI=0xffffffff, name=0xffffffff, attributes=[],
            styleAttribute=-1, classAttribute=-1, lineNumber=0, Comment=0xffffffff,
            proto : axml_pb2.ResXMLStartElement = None):
        if proto is None:
            self.proto = axml_pb2.ResXMLStartElement()
            super().__init__(lineNumber, Comment)
            self.proto.namespaceURI = namespaceURI
            self.proto.name = name
            self.proto.attributes.extend(attributes)
            self.proto.styleAttribute = styleAttribute
            self.proto.classAttribute = classAttribute
        else:
            self.proto = proto
            super().__init__(proto=proto.generic)
            

    def compute(self):
        self.proto.len_attributes = len(self.proto.attributes)
        super().compute()

    @property
    def content(self):
        return super().content + pack('<LLLLhh',
                self.proto.namespaceURI,
                self.proto.name,
                0x140014, # potential attribute value
                self.proto.len_attributes,
                self.proto.styleAttribute,
                self.proto.classAttribute) + \
                        b"".join(Attribute(proto=a).pack() for a in self.proto.attributes)

class RES_XML_END_ELEMENT(Classical_RES_XML):

    def __init__(self, namespaceURI=0xffffffff, name=0xffffffff,
                 lineNumber=0, Comment=0xffffffff,
                 proto : axml_pb2.ResXMLEndElement = None):
        if proto is None:
            self.proto = axml_pb2.ResXMLEndElement()
            super().__init__(lineNumber, Comment)
            self.proto.namespaceURI = namespaceURI
            self.proto.name = name
        else:
            self.proto = proto
            super().__init__(proto=proto.generic)
            


    @property
    def content(self):
        return super().content + pack('<LL',
                self.proto.namespaceURI,
                self.proto.name)

class RES_XML_START_NAMESPACE(Classical_RES_XML):

    def __init__(self, prefix=0xffffffff, uri=0xffffffff,
                lineNumber=0, Comment=0xffffffff,
                proto : axml_pb2.ResXMLStartNamespace = None):
        if proto is None:
            self.proto = axml_pb2.ResXMLStartNamespace()
            super().__init__(lineNumber, Comment)
            self.proto.prefix = prefix
            self.proto.uri = uri
        else:
            self.proto = proto
            super().__init__(proto=proto.generic)
            

    @property
    def content(self):
        return super().content + pack('<LL',
                self.proto.prefix,
                self.proto.uri)

class RES_XML_END_NAMESPACE(Classical_RES_XML):

    def __init__(self, prefix=0xffffffff, uri=0xffffffff,
                 lineNumber=0, Comment=0xffffffff,
                 proto : axml_pb2.ResXMLEndNamespace = None):
        if proto is None:
            self.proto = axml_pb2.ResXMLEndNamespace()
            super().__init__(lineNumber, Comment)
            self.proto.prefix = prefix
            self.proto.uri = uri
        else:
            self.proto = proto
            super().__init__(proto=proto.generic)
            

    @property
    def content(self):
        return super().content + pack('<LL',
                self.proto.prefix,
                self.proto.uri)
    

class Attribute:

    def __init__(self, namespaceURI=0xffffffff, name=0xffffffff, value=0xffffffff, type=0xffffffff, data=0xffffffff, proto=None):
        if proto is None:
            self.proto = axml_pb2.Attribute()
            self.proto.namespaceURI = namespaceURI
            self.proto.name = name
            self.proto.value = value
            self.proto.type = type
            self.proto.data = data
        else:
            self.proto = proto

    def pack(self):
        return pack('<LLLLL', self.proto.namespaceURI, self.proto.name, self.proto.value,
                self.proto.type, self.proto.data)



class RessourceXML:

    def __init__(self, proto=None) -> None:
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.RessourceXML()
    
    def pack(self):
        buf = b""
        for elt in self.proto.elts:
            header = AXMLHeader(proto=elt.header).pack()
            if elt.HasField('start_elt'):
                buf += header + RES_XML_START_ELEMENT(proto=elt.start_elt).pack()
            elif elt.HasField('end_elt'):
                buf += header + RES_XML_END_ELEMENT(proto=elt.end_elt).pack()
            elif elt.HasField('start_ns'):
                buf += header + RES_XML_START_NAMESPACE(proto=elt.start_ns).pack()
            elif elt.HasField('end_ns'):
                buf += header + RES_XML_END_NAMESPACE(proto=elt.end_ns).pack()
        return buf


##############################################################################
#
#                              AXML OBJECT
#
##############################################################################


class AXML:

    def __init__(self, proto=None):
        if proto:
            self.proto = proto
            self.stringblocks = StringBlocks(proto=self.proto.stringblocks)
        else:
            self.proto = axml_pb2.AXML()
            self.stringblocks = StringBlocks()
    
    @property
    def get_proto(self):
        self.proto.stringblocks = self.stringblocks.proto
        return self.proto

    ###########################################
    #                                         #
    #           ENOCDE from XML               #
    #                                         #
    ###########################################
    
    def from_xml(self, root):
        self.add_all_attrib(root)
        self.start_namespace("http://schemas.android.com/apk/res/android", "android")
        self.from_xml_etree(root)
        self.end_namespace("http://schemas.android.com/apk/res/android", "android")
        self.compute()
   
    
    def from_xml_etree(self, root):
        self.start(root.tag, root.attrib)
        for e in root:
            self.from_xml_etree(e)
        self.end(root.tag)

    
    def add_xml_elt(self, res_xml, header_xml):
        res_xml.compute()

        header = header_xml(len(res_xml.content))

        elt = axml_pb2.XMLElement()
        elt.header.CopyFrom(header.proto)
        if type(res_xml.proto) is axml_pb2.ResXMLStartElement:
            elt.start_elt.CopyFrom(res_xml.proto)
        elif type(res_xml.proto) is axml_pb2.ResXMLStartNamespace:
            elt.start_ns.CopyFrom(res_xml.proto)
        elif type(res_xml.proto) is axml_pb2.ResXMLEndNamespace:
            elt.end_ns.CopyFrom(res_xml.proto)
        elif type(res_xml.proto) is axml_pb2.ResXMLEndElement:
            elt.end_elt.CopyFrom(res_xml.proto)
        self.proto.resourcexml.elts.append(elt)

    def start(self, root, attrib):
        index = self.stringblocks.get(root)
        i_namespace = self.stringblocks.get("android")
        attributes = []

        dic_attrib = attrib.items()
        for k, v in dic_attrib:
            tmp = k.split('{')
            if len(tmp) > 1:
                tmp = tmp[1].split('}')
                name = self.stringblocks.get(tmp[1])
                namespace = self.stringblocks.get(tmp[0])
            else:
                namespace = 0xffffffff
                name = self.stringblocks.get(k)

            if v == "true":
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x12000000, 1).proto)
            elif v == "false":
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x12000000, 0).proto)
            elif re.search("^@android:[0-9a-fA-F]+$", v):
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x1000000, int(v[-8:], 16)).proto)
            elif re.search("^@[0-9a-fA-F]+$", v):
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x1000000, int(v[1:], 16)).proto)
            elif re.search("^0x[0-9a-fA-F]+$", v):
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x11000000, int(v[2:], 16)).proto)
            else:
                if self.stringblocks.proto.stringblocks[name].data == "versionName":
                    value = self.stringblocks.get(v)
                    attributes.append(Attribute(namespace, name, value, 0x3000008, value).proto)
                elif self.stringblocks.proto.stringblocks[name].data == "compileSdkVersionCodename":
                    value = self.stringblocks.get(v)
                    attributes.append(Attribute(namespace, name, value, 0x3000008, value).proto)
                else:
                    try:
                        value = ctypes.c_uint32(int(v)).value
                        attributes.append(Attribute(namespace, name, 0xffffffff, 0x10000008, value).proto)
                    except ValueError:
                        try:
                            value = unpack('>L', pack('!f', float(v)))[0]
                            attributes.append(Attribute(namespace, name, 0xffffffff, 0x04000008, value).proto)
                        except ValueError:
                            value = self.stringblocks.get(v)
                            attributes.append(Attribute(namespace, name, value, 0x3000008, value).proto)


        content = RES_XML_START_ELEMENT(0xffffffff, index, attributes)
        self.add_xml_elt(content, AXMLHeader_START_ELEMENT)


    def start_namespace(self, prefix, uri):
        index = self.stringblocks.get(prefix)
        i_namespace = self.stringblocks.get(uri)


        content = RES_XML_START_NAMESPACE(i_namespace, index)
        self.add_xml_elt(content, AXMLHeader_START_NAMESPACE)

    def end_namespace(self, prefix, uri):
        index = self.stringblocks.get(prefix)
        i_namespace = self.stringblocks.get(uri)


        content = RES_XML_END_NAMESPACE(i_namespace, index)
        self.add_xml_elt(content, AXMLHeader_END_NAMESPACE)

    def end(self, attrib):
        index = self.stringblocks.index(attrib)
        i_namespace = self.stringblocks.index("android")

        content = RES_XML_END_ELEMENT(0xffffffff, index)
        self.add_xml_elt(content, AXMLHeader_END_ELEMENT)

    def add_all_attrib(self, root):
        res = []
        namespace = "{http://schemas.android.com/apk/res/android}"
        queue = [root]
        while len(queue) > 0:
            r = queue.pop()
            for child in r:
                queue.append(child)
            for k in r.attrib.keys():
                if k.startswith(namespace):
                    name = k[len(namespace):]
                    if name in public.SYSTEM_RESOURCES['attributes']['forward']:
                        val = public.SYSTEM_RESOURCES['attributes']['forward'][name]
                        if not val in res:
                            self.stringblocks.get(name)
                            res.append(val)
        self.proto.resourcemap.CopyFrom(ResourceMap(res=res).proto)

    ###########################################
    #                                         #
    #           ENOCDE from XML               #
    #                                         #
    ###########################################
    
    def compute(self):
        self.stringblocks.compute()
        self.proto.header_xml.CopyFrom(AXMLHeader_XML(len(self.pack())).proto)

    def pack(self):
        self.proto.stringblocks.CopyFrom(self.stringblocks.proto)
        sb_pack = self.stringblocks.pack()
        res = ResourceMap(proto=self.proto.resourcemap).pack()
        resxml = RessourceXML(proto=self.proto.resourcexml).pack()
        header_xml = AXMLHeader_XML(proto=self.proto.header_xml).pack()
        return header_xml + sb_pack + res + resxml

