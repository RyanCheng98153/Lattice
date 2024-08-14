from enum import Enum
from typing import List
import sys

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

class Helper:
    def __init__(self, _L:int, _W:int):
        self.L:int = _L
        self.W:int = _W
    
    def getCood(self, _id):
        return _id // self.W, _id % self.W
    
    def getId(self, _i, _j):
        return _i * self.W + _j
    
    def getRight(self, _id):
        i, j = self.getCood(_id)
        return self.getId( i, (j+1) % self.W ) 
    
    def getBottom(self, _id):
        i, j = self.getCood(_id)
        return self.getId( (i+1) % self.L, j )
    
    def getBottomRight(self, _id):
        i, j = self.getCood(_id)
        return self.getId( (i+1) % self.L, (j+1) % self.W )
    
    @staticmethod
    def getPrettyId( _id ):
        if _id == None:
            return "[   ]"
        elif _id < 10:
            return "[ " + str(_id) + " ]"
        elif _id < 100:
            return "[ " + str(_id) + "]"
        elif _id < 1000:
            return "["  + str(_id) + "]"
        else:
            return "[INF]"
    

class MLGraph:
    def __init__(self, _L:int, _W:int, _hexInit:int):
        self.L = _L
        self.W = _W
        self.nodes      :List[Node] = [Node(i) for i in range(0, _L*_W)]
        self.hexInit    :int = _hexInit
        self.helper     :Helper = Helper(_L, _W)
    
    def getIdentify(self, _id):
        i, j = self.helper.getCood(_id)
        return ( j - 3*i - self.hexInit) % 7    
    
    def makeGraph(self):
        for i in range(0, self.L):
            for j in range(0, self.W):
                srcId = self.helper.getId(i, j)
                if self.getIdentify(srcId) == 0 :
                    self.nodes[srcId] = None
                    continue
                self.nodes[srcId].right = self.nodes[self.helper.getRight(srcId)]
                self.nodes[srcId].bottom = self.nodes[self.helper.getBottom(srcId)]
                self.nodes[srcId].bottomRight = self.nodes[self.helper.getBottomRight(srcId)]
                
                if self.getIdentify(srcId) == 6:
                    self.nodes[srcId].right = None
                if self.getIdentify(srcId) == 3:
                    self.nodes[srcId].bottom = None
                if self.getIdentify(srcId) == 2:
                    self.nodes[srcId].bottomRight = None
                
    def printGraphText(self):
        for i, node in enumerate(self.nodes):
            if node == None:
                print( f"[Node {i}]: spin: {None}\n" )
                continue
            node.printNodeText()
            
    def printGraphVisual(self):
        printStr1 = ''
        printStr2 = ''
        for index, node in enumerate(self.nodes):
            if node == None:
                printStr1 += ( Helper.getPrettyId(None) + '   '  )
                printStr2 += ( '     ' + '   '  )
            else:
                tmp1, tmp2 = node.printNodeVisual(False)
                printStr1 += tmp1
                printStr2 += tmp2
                
            if index % self.W == self.W-1:
                print(printStr1)
                print(printStr2)
                printStr1 = ''
                printStr2 = ''

    
def main():
    L = int(sys.argv[1])
    W = int(sys.argv[2])
    hexInit = int(sys.argv[3])
    
    graph = MLGraph(L, W, hexInit)
    graph.makeGraph()
    # graph.printGraphText()
    graph.printGraphVisual()
    # checkSingleNode(graph)
    
def checkSingleNode( _graph: MLGraph ):
    helper = Helper(_graph.L, _graph.W)
    n = 0
    while(n >= 0):
        try:
            n = int(input(f"node id you wanna check (0~{ _graph.L * _graph.W -1 }): "))
        except:
            print("invalid input, terminate")
            break
        if ( n >= ( _graph.L * _graph.W -1 ) ):
            print("invalid input")
            continue
        
        if _graph.nodes[n] != None:
            _graph.nodes[n].printNodeVisual(True)
        else:
            print( Helper.getPrettyId(None) + '   ' + Helper.getPrettyId(helper.getRight(n) ) )
            print( '     ' + '   ' + '     ' )
            print( Helper.getPrettyId(helper.getBottom(n)) + '   ' + Helper.getPrettyId(helper.getBottomRight(n) ) )
            
if __name__ == "__main__":
    main()