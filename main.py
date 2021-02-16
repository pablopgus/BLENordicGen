from bleXML import *
from codeGen import *

BLEMap = getBLEMap()
CG = codeGen(BLEMap)
CG.run()