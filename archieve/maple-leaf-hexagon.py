from enum import Enum
from typing import List
import random

class Spin(Enum):
    UP = 1
    DOWN = 0
    
class NodeType(Enum):
    v_SELF = 0
    
    v_BRIDGE = 1
    v_TriA = 2
    v_TriB = 3
    v_HexA = 4
    v_HexB = 5

class Node:
    def __init__( self, _id: int ):
        self.spin: Spin = Spin.UP
        
        # id of current node
        self.id: int = _id
        
        # vertex: bridge connects hexagons and triangles
        self.v_bridge: Node = None
        # vertices that compose triangle 
        # B for Balance (middle, 90 degree), A for Asymmetric (right, 30 degree)
        self.v_triA: Node = None
        self.v_triB: Node = None 
        # vertices that compose hexagon
        # B for near bridge (left: -150 degree), A for near triA (right, -30 degree)
        self.v_hexA: Node = None
        self.v_hexB: Node = None 
    
    def flip( self ):
        if self.spin == Spin.UP:
            self.spin = Spin.DOWN
        else:
            self.spin = Spin.UP
    
    def printNode( self ):
        output_str = f"[Node {self.id}]: {self.spin}"
        output_str += f", bridge: {None if self.v_bridge == None else f'{self.v_bridge.id} {self.v_bridge.spin}'} " + '\n'
        output_str += f"hexA: {None if self.v_hexA == None else f'{self.v_hexA.id} {self.v_hexA.spin}' }"
        output_str += f", hexB: {None if self.v_hexB == None else f'{self.v_hexB.id} {self.v_hexB.spin}'}" + '\n'
        output_str += f"triA: {None if self.v_triA == None else f'{self.v_triA.id} {self.v_triA.spin}'}"
        output_str += f", triB: {None if self.v_triB == None else f'{self.v_triB.id} {self.v_triB.spin}'}" + '\n'
        print(output_str)
        
        
class Hexagon:
    def __init__( self, _hexId ):
        self.hexId: int = _hexId
        self.nodes: List[Node] = [Node( self.hexId * 6 + nodeId ) for nodeId in range(0, 6)]
        self.connectHexagon()
        
    def prvNodeId( self, _id:int ):
        return (_id + 5) % 6
    
    def nxtNodeId( self, _id:int ):
        return (_id + 1 ) % 6
            
    def connectHexagon( self ):
        for i in range(0, 6):
            self.nodes[i].v_hexA = self.nodes[ self.nxtNodeId(i) ]
            self.nodes[i].v_hexB = self.nodes[ self.prvNodeId(i) ]
    
    def printHex ( self ):
        for node in self.nodes:
            node.printNode()
    
class MLGraph:
    def __init__(self, _W, _L):
        self.L = _L
        self.W = _W
        self.Hexagons: List[Hexagon] = [ Hexagon(id) for id in range(0, self.L * self.W) ]

    def getHexId( self, _i, _j ):
        return _i * self.W + _j
    
    def getNxtI( self, _i ):
        return (_i + 1) % self.L
    
    def getPrvI( self, _i ):
        return (_i + self.L - 1) % self.L
    
    def getNxtJ( self, _j ):
        return (_j + 1) % self.W
    
    def getPrvI( self, _j ):
        return (_j + self.W - 1) % self.W
    
    def connectGraph( self ):
        for i in range(0, self.L):
            for j in range(0, self.W):
                hex = self.Hexagons[ self.getHexId(i, j) ]
                
                for n in range( 0, len(hex.nodes) ):
                    hex.nodes[n]
    
    def printHexGraph( self ):
        print("print Hexagons")
        for i in reversed( range(0, self.L) ):
            output_str = ""
            for j in range(0, self.W): 
                output_str += f"{self.Hexagons[ self.getHexId(i, j) ].hexId } \t"
            print(output_str)
        print()
    
    def printNodeGraph( self ):
        print("print Nodes")
        for hex in self.Hexagons:
            hex.printHex()
        
def main():
    print("hello maple leaf !")
    # node: Node = Node(0)
    # node.printInfo()
    graph = MLGraph(9, 9)
    graph.printHexGraph()
    graph.printNodeGraph()

if __name__ == "__main__":
    main()
