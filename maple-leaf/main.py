import sys
from src.graph import MLGraph
from src.test import Test
from src.visualize import Visualize
    
def main():
    L:int = int(sys.argv[1])
    W:int = int(sys.argv[2])
    
    hexInit:int = 0
    if (len(sys.argv) > 3):
        hexInit = int(sys.argv[3])
    
    graph = MLGraph(L, W, hexInit)
    graph.makeGraph()
    graph.bondGraph(3.0, 6.0, 2.0)
    # graph.printGraphText()
    # graph.printGraphVisual()
    
    # Test.checkIsingleNode(graph)
    Visualize.visualize(graph, labelHexagon=True, showStrength=False)
    
if __name__ == "__main__":
    main()