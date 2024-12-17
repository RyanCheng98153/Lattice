from src.node import Node, NodeType
from src.helper import NodeHelper
from typing import List

class TrianglularGraph:
    def __init__(self, _L:int, _W:int):
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
                self.nodes[srcId].right = self.nodes[self.helper.getRight(srcId)]
                self.nodes[srcId].bottom = self.nodes[self.helper.getBottom(srcId)]
                self.nodes[srcId].bottomRight = self.nodes[self.helper.getBottomRight(srcId)]
                
        self.getAdjList(True)
                    
    def bondGraph(self, _JLayer:float):
        for i in range(0, self.L):
            for j in range(0, self.W):
                srcId = self.helper.getId(i, j)
                srcNode = self.nodes[srcId]
                
                srcNode.JRight = _JLayer
                srcNode.JBottom = _JLayer
                srcNode.JBottomRight = _JLayer
                
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