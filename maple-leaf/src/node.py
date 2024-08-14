from enum import Enum
from src.helper import Helper

class Spin(Enum):
    UP = 1
    DOWN = 0

class Node:
    def __init__(self, _id:int):
        self.id:int = _id
        self.spin:Spin = Spin.UP
        
        self.right      :Node = None
        self.bottom     :Node = None
        self.bottomRight:Node = None
        
        self.left       :Node = None

    def printNodeText( self ):
        print( f"[Node {self.id}]: {self.spin}" )
        output_str = f"right: {None if self.right == None else f'{self.right.id} {self.right.spin}'}"
        output_str += f", bottom: {None if self.bottom == None else f'{self.bottom.id} {self.bottom.spin}'}"
        output_str += f", bottomRight: {None if self.bottomRight == None else f'{self.bottomRight.id} {self.bottomRight.spin}'} \n"
        print(output_str)
        
    def printNodeVisual( self, printMode=False ):
        ''' example
        [slf] - [rig]
          |   \      
        [btm] - [ br]
        '''
        
        str1 = Helper.getPrettyId(self.id)
        str2 = ''
        str3 = ''
        # self and right node
        if self.right != None:
            str1 += ' - ' 
            if printMode: str1 += Helper.getPrettyId(self.right.id)
        else:
            str1 += '   ' 
            if printMode: str1 += Helper.getPrettyId(None)
        # bottom node
        if self.bottom != None:
            str2 += '  |  '
            if printMode: str3 += Helper.getPrettyId(self.bottom.id)
        else:
            str2 += '     '
            if printMode: str3 += Helper.getPrettyId(None)
        # bottomRight node
        if self.bottomRight != None:
            str2 += ' \ ' 
            if printMode: str2 += '     '
            if printMode: str3 += '   ' + Helper.getPrettyId(self.bottomRight.id)
        else:
            str2 += '   ' 
            if printMode: str2 += '     '
            if printMode: str3 += '   ' + Helper.getPrettyId(None)
        # decide whether to print or not
        if printMode:
            print(str1)
            print(str2)
            print(str3)
        return [str1, str2]