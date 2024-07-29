from enum import Enum

class Spin(Enum):
    UP = 1
    DOWN = 0

class Node:
    def __init__(self):
        spin: Spin = Spin.UP
        
        # vertices of current node
        v_self: Node = self
        # vertices that compose triangle 
        # B for Balance (middle, 90 degree), A for Asymmetric (right, 30 degree)
        v_triA: Node = None
        v_triB: Node = None 
        # vertices that compose hexagon
        # B for near bridge (left: -150 degree), A for near triA (right, -30 degree)
        v_hexA: Node = None
        v_hexB: Node = None 

def main():
    print("hello maple leaf !")

if __name__ = "__main__":
    main()
