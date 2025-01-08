from enum import Enum

class Spin(Enum):
    UP = 1
    DOWN = 0

class NodeType(Enum):
    Green = 0
    Red = 1
    Blue = 2
    Center = 3

class BondType(Enum):
    Triangle = 0
    Hexagon = 1
    Dimer = 2
    
class Node:
    def __init__(self, _id:int):
        self.id         :int = _id
        self.clean_id   :int = _id
        self.spin:Spin = Spin.UP
        
        self.NodeType   :NodeType = None
        
        self.right      :Node = None
        self.bottom     :Node = None
        self.bottomRight:Node = None
        
        self.JRight      :float = 1.0
        self.JBottom     :float = 1.0
        self.JBottomRight:float = 1.0
        
        self.rightType         :BondType = None
        self.bottomType        :BondType = None
        self.bottomRightType   :BondType = None
        
    def __repr__(self):
        return f"[Node {self.id}]: {self.spin}"
    
    def set_spin(self, spin:Spin):
        self.spin = spin