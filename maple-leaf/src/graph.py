from src.node import Node
from src.helper import PrintHelper, NodeHelper
from typing import List

class MLGraph:
    def __init__(self, _L:int, _W:int, _hexInit:int):
        self.L = _L
        self.W = _W
        self.nodes      :List[Node] = [Node(i) for i in range(0, _L*_W)]
        self.hexInit    :int = _hexInit
        self.helper     :NodeHelper = NodeHelper(_L, _W)
    
    def getIdentify(self, _id):
        '''
        if identify of id is 0, there should be a hexagon hole at id 
        '''
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
                    
    def bondGraph(self, _JTriangle:float, _JHexagon: float, _JDimer: float):
        for i in range(0, self.L):
            for j in range(0, self.W):
                srcId = self.helper.getId(i, j)
                # is hexagon hole
                if self.nodes[srcId] == None:
                    # empty(None) Node don't have member variable of right, bottom, bottomRight
                    # so, find right, bottom, bottomRight from graph
                    right = self.helper.getRight(srcId)
                    bottom = self.helper.getBottom(srcId)
                    bottomRight = self.helper.getBottomRight(srcId)
                    # triangular lattice
                    self.nodes[right].JRight = _JTriangle
                    self.nodes[bottom].JBottom = _JTriangle
                    self.nodes[bottomRight].JBottomRight = _JTriangle
                    # hexagon lattice
                    self.nodes[right].JBottom = _JHexagon
                    self.nodes[bottom].JRight = _JHexagon
                    # dimer lattice
                    self.nodes[right].JBottomRight = _JDimer
                    self.nodes[bottomRight].JBottom = _JDimer
                    self.nodes[bottomRight].bottomRight.JRight = _JDimer
                    continue
                    
                # is a regular node
                rightNode = self.nodes[srcId].right
                bottomNode = self.nodes[srcId].bottom
                bottomRightNode = self.nodes[srcId].bottomRight
                
                # hexagon lattice
                if rightNode == None or bottomNode == None:
                    self.nodes[srcId].JBottomRight = _JHexagon
                if bottomRightNode == None:
                    self.nodes[srcId].JRight = _JHexagon
                    self.nodes[srcId].JBottom = _JHexagon
                    
                # triangular lattice
                if rightNode != None and rightNode.right == None:
                    self.nodes[srcId].JRight = _JTriangle
                    continue
                if bottomNode != None and bottomNode.bottom == None:
                    self.nodes[srcId].JBottom = _JTriangle
                    continue
                if bottomRightNode != None and bottomRightNode.bottomRight == None:
                    self.nodes[srcId].JBottomRight = _JTriangle
                    continue
                
                
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
                printStr1 += ( PrintHelper.getPrettyId(None) + '   '  )
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
    
    def getAdjList(self):
        adjList = []
        for srcNode in self.nodes:
            if srcNode == None:
                continue
            for adjNode, bondStrength in [[srcNode.right, srcNode.JRight], 
                                         [srcNode.bottom, srcNode.JBottom], 
                                         [srcNode.bottomRight, srcNode.JBottomRight]]:
                if adjNode == None:
                    continue
                adjList.append([srcNode.id, adjNode.id, bondStrength])
        
        return adjList