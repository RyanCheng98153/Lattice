import sys
from src.graph import KagomeGraph
from src.test import Test
from src.visualize import Visualize
    
def main():
    L:int = 6
    W:int = 6
    
    L:int = int(sys.argv[1])
    W:int = int(sys.argv[2])
    
    hexInit:int = 0
    if (len(sys.argv) > 3):
        hexInit = int(sys.argv[3])
    
    graph = KagomeGraph(L, W, hexInit)
    graph.makeGraph()
    graph.bondGraph(1.0, 1.0, 1.0)
    # graph.printGraphText()
    # graph.printGraphVisual()
    
    # with open(file=f"./kagome_L_{L}_{W}.txt", mode="w") as f:
    #     f.writelines(graph.getSpacefileText())
    # Test.checkIsingleNode(graph)
    Visualize.visualize(graph, labelHexagon=True, showStrength=False)
    
if __name__ == "__main__":
    main()