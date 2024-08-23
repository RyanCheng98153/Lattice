import sys
from src.graph import MLGraph
from src.helper import PrintHelper, NodeHelper
import networkx as nx
import matplotlib.pyplot as plt
    
def main():
    L:int = int(sys.argv[1])
    W:int = int(sys.argv[2])
    
    hexInit:int = 0
    if (len(sys.argv) > 3):
        hexInit = int(sys.argv[3])
    
    graph = MLGraph(L, W, hexInit)
    graph.makeGraph()
    # graph.printGraphText()
    # graph.printGraphVisual()
    # checkIsingleNode(graph)
    visualize(graph)
    
def visualize( _graph: MLGraph ):
    adjList = []
    
    for srcNode in _graph.nodes:
        if srcNode == None:
            continue
        for adjNode in [srcNode.right, srcNode.bottom, srcNode.bottomRight]:
            if adjNode == None:
                continue
            adjList.append([srcNode.id, adjNode.id])

    # G = nx.DiGraph()
    # G.add_edges_from(adjList)
    # G = nx.grid_2d_graph(_graph.L, _graph.W)
    # pos = dict( (n, n) for n in G.nodes() ) #Dictionary of all positions
    # labels = dict( ((i, j), i + (_graph.L-1-j) * _graph.W ) for i, j in G.nodes() )
    # nx.draw_networkx(G, pos=pos, labels=labels,with_labels=False, node_size=10)
    N=7
    G=nx.grid_2d_graph(N,N)
    pos = dict( (n, n) for n in G.nodes() ) #Dictionary of all positions
    labels = dict( ((i, j), i + (N-1-j) * N ) for i, j in G.nodes() )
    print(f"G: {G}")
    print(f"pos: {pos}")
    print(f"labels: {labels}")
    nx.draw_networkx(G, pos=pos, labels=labels,with_labels=True, node_size=10)
    
    
    # nx.draw_networkx(G) 
    plt.show() 
    # print(adjList)
    return adjList

def checkIsingleNode( _graph: MLGraph ):
    helper = NodeHelper(_graph.L, _graph.W)
    n = 0
    while(n >= 0):
        try:
            id = int(input(f"node id you wanna check (0~{ _graph.L * _graph.W -1 }): "))
        except:
            print("invalid input, terminate")
            break
        if ( id >= ( _graph.L * _graph.W -1 ) ):
            print("invalid input")
            continue
        
        if _graph.nodes[id] != None:
            _graph.nodes[id].printNodeVisual(True)
        else:
            print( PrintHelper.getPrettyId(None) + '   ' + PrintHelper.getPrettyId(helper.getRight(id) ) )
            print( '     ' + '   ' + '     ' )
            print( PrintHelper.getPrettyId(helper.getBottom(id)) + '   ' + PrintHelper.getPrettyId(helper.getBottomRight(id) ) )
            
if __name__ == "__main__":
    main()