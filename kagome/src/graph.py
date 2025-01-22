from src.node import Node, NodeType, BondType
from src.helper import NodeHelper
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
                    self.nodes[srcId].NodeType = NodeType.Center
                    self.nodes[srcId] = None
                    continue
                self.nodes[srcId].right = self.nodes[self.helper.getRight(srcId)]
                self.nodes[srcId].bottom = self.nodes[self.helper.getBottom(srcId)]
                self.nodes[srcId].bottomRight = self.nodes[self.helper.getBottomRight(srcId)]
                
                # Red 
                if self.getIdentify(srcId) == 0:
                    self.nodes[srcId].NodeType = NodeType.Red
                    self.nodes[srcId].bottomRight = None
                    continue
                # Green
                if self.getIdentify(srcId) == 1:
                    self.nodes[srcId].NodeType = NodeType.Green
                    self.nodes[srcId].bottom = None
                    continue
                # Blue
                if self.getIdentify(srcId) == 2:
                    self.nodes[srcId].NodeType = NodeType.Blue
                    self.nodes[srcId].right = None
                    continue
        self.getAdjList(True)
                    
    def bondGraph(self, _JLayer: float):
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
                
                if srcNode.NodeType == NodeType.Red:
                    srcNode.JRight = _JLayer
                    srcNode.JBottom = _JLayer
                    srcNode.rightType = BondType.Connected
                    srcNode.bottomType = BondType.Connected
                    continue
                if srcNode.NodeType == NodeType.Green:
                    srcNode.JRight = _JLayer
                    srcNode.JBottomRight = _JLayer
                    srcNode.rightType = BondType.Connected
                    srcNode.bottomRightType = BondType.Connected
                    continue
                if srcNode.NodeType == NodeType.Blue:
                    srcNode.JBottom = _JLayer
                    srcNode.JBottomRight = _JLayer
                    srcNode.bottomType = BondType.Connected
                    srcNode.bottomRightType = BondType.Connected
                    continue
                
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