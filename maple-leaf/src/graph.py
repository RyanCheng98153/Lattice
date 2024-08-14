from src.node import Node
from src.helper import Helper
from typing import List

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