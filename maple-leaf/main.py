import sys
from src.graph import MLGraph
from src.helper import Helper
    
def main():
    L = int(sys.argv[1])
    W = int(sys.argv[2])
    hexInit = int(sys.argv[3])
    
    graph = MLGraph(L, W, hexInit)
    graph.makeGraph()
    # graph.printGraphText()
    graph.printGraphVisual()
    # checkSingleNode(graph)
    
def checkSingleNode( _graph: MLGraph ):
    helper = Helper(_graph.L, _graph.W)
    n = 0
    while(n >= 0):
        try:
            n = int(input(f"node id you wanna check (0~{ _graph.L * _graph.W -1 }): "))
        except:
            print("invalid input, terminate")
            break
        if ( n >= ( _graph.L * _graph.W -1 ) ):
            print("invalid input")
            continue
        
        if _graph.nodes[n] != None:
            _graph.nodes[n].printNodeVisual(True)
        else:
            print( Helper.getPrettyId(None) + '   ' + Helper.getPrettyId(helper.getRight(n) ) )
            print( '     ' + '   ' + '     ' )
            print( Helper.getPrettyId(helper.getBottom(n)) + '   ' + Helper.getPrettyId(helper.getBottomRight(n) ) )
            
if __name__ == "__main__":
    main()