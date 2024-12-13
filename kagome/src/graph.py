from src.node import Node, NodeType
from src.helper import PrintHelper, NodeHelper
from typing import List

class KagomeGraph:
    def __init__(self, _L:int, _W:int, _hexInit:int):
        self.L = _L
        self.W = _W
        self.nodes      :List[Node] = [Node(i) for i in range(0, _L*_W)]
        # self.hexInit    :int = _hexInit
        self.helper     :NodeHelper = NodeHelper(_L, _W)
    
    def getIdentify(self, _id):
        '''
        if identify of id is 0, identify as green node
        if identify of id is 1, identify as red node
        if identify of id is 2, identify as blue node
        if identify of id is 3, identify as hexagon center hole
        '''
        i, j = self.helper.getCood(_id)
        return 2 * (i%2) + (j%2)
    
    def makeGraph(self):
        for i in range(0, self.L):
            for j in range(0, self.W):
                srcId = self.helper.getId(i, j)
                # Hexagon center hole
                if self.getIdentify(srcId) == 3:
                    self.nodes[srcId] = None
                    continue
                self.nodes[srcId].right = self.nodes[self.helper.getRight(srcId)]
                self.nodes[srcId].bottom = self.nodes[self.helper.getBottom(srcId)]
                self.nodes[srcId].bottomRight = self.nodes[self.helper.getBottomRight(srcId)]
                
                # Green
                if self.getIdentify(srcId) == 0:
                    self.nodes[srcId].NodeType = NodeType.Green
                    self.nodes[srcId].bottomRight = None
                    continue
                # Red 
                if self.getIdentify(srcId) == 1:
                    self.nodes[srcId].NodeType = NodeType.Red
                    self.nodes[srcId].bottom = None
                    continue
                # Blue
                if self.getIdentify(srcId) == 2:
                    self.nodes[srcId].NodeType = NodeType.Blue
                    self.nodes[srcId].right = None
                    continue
        self.getAdjList(True)
                    
    def bondGraph(self, _JTriangle:float, _JHexagon: float, _JDimer: float):
        for i in range(0, self.L):
            for j in range(0, self.W):
                srcId = self.helper.getId(i, j)
                # is hexagon hole
                if self.nodes[srcId] == None:
                    # empty(None) Node don't have member variable of right, bottom, bottomRight
                    # so, find right, bottom, bottomRight from graph
                    continue
                    
                # is a regular node
                srcNode = self.nodes[srcId]
                
                if srcNode.NodeType == NodeType.Green:
                    srcNode.JRight = _JHexagon
                    srcNode.JBottom = _JHexagon
                    continue
                if srcNode.NodeType == NodeType.Red:
                    srcNode.JRight = _JHexagon
                    srcNode.JBottomRight = _JHexagon
                    continue
                if srcNode.NodeType == NodeType.Blue:
                    srcNode.JBottom = _JHexagon
                    srcNode.JBottomRight = _JHexagon
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
    
    def getAdjList(self, clean = False):
        adjList = []
        
        if clean:
            index = 0
            for srcNode in self.nodes:
                if srcNode != None:
                    srcNode.clean_id = index
                    index += 1
            
        for srcNode in self.nodes:
            if srcNode == None:
                continue
            for adjNode, bondStrength, bondType in [[srcNode.right, srcNode.JRight,srcNode.rightType], 
                                                [srcNode.bottom, srcNode.JBottom, srcNode.bottomType], 
                                                [srcNode.bottomRight, srcNode.JBottomRight, srcNode.bottomRightType]]:
                if adjNode == None:
                    continue
                
                if clean:
                    adjList.append([srcNode.clean_id, adjNode.clean_id, bondStrength, bondType])
                else:
                    adjList.append([srcNode.id, adjNode.id, bondStrength, bondType])
        
        return adjList
    
    def getSpacefileText(self):
        # spaceText = f"# Model: L {self.L} W {self.W} Kagome Graph" + "\n"
        spaceText = ""
        
        for srcId, adjId, strength, bondType in self.getAdjList(clean=True):
            spaceText += f"{srcId} {adjId} {strength}\n"
            
        return spaceText