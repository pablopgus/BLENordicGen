import xml.etree.ElementTree as ET

def getBLEMap():
    MXCL = ET.parse('Mixcell.xml').getroot()

    services = MXCL
    bleMap = []
    for s in services:
        s_ = service(s.attrib['name'], s.attrib['uuid'])
        for ch in s:
            ch_ = char(ch.attrib['name'], ch.attrib['uuid'], ch.attrib['type'], ch.attrib['initial'], ch.attrib['actions'])
            s_.addChar(ch_)
        bleMap.append(s_)
    return bleMap

class service():
    def __init__(self, name, uuid):
        self.name = name
        self.uuid = uuid
        self.charL = []

    def addChar(self, char):
        self.charL.append(char)

    # Represent the class object as its board
    def __repr__(self):
        res = " Service <"+self.name+"@"+self.uuid+">: ("
        for ch in self.charL:
            res += " "+str(ch) + ", "
        res += ") "
        return res

class char():
    def __init__(self, name, uuid, tp, dflt, act):
        self.name = name
        self.uuid = uuid
        self.type = tp
        self.default = dflt
        self.actions = act

    def __repr__(self):
        return "CHAR<"+self.name+"@"+self.uuid+">_"+self.actions