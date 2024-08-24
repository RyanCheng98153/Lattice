import sys
from src.graph import MLGraph
from src.helper import PrintHelper, NodeHelper
import networkx as nx
import matplotlib.pyplot as plt
import copy
    
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
    # visualize(graph)
    visualizeTriangular(graph)
    
def visualizeTriangular( _graph: MLGraph ):
    G = nx.empty_graph( n=0 )
    # exists nodes
    G.add_nodes_from((i, j) for i in range(_graph.W) for j in range(_graph.L))
    nodelist = copy.deepcopy(G.nodes())
    # right
    G.add_edges_from(((i, j), (i+1, j)) for i in range(_graph.W-1) for j in range(_graph.L))
    # button
    G.add_edges_from(((i, j), (i, j+1)) for i in range(_graph.W) for j in range(_graph.L-1))
    
    # button right
    G.add_edges_from(((i, j), (i+1, j-1)) for i in range(_graph.W) for j in range(_graph.L))
    
    pos = dict( (n, n) for n in G.nodes() ) #Dictionary of all positions
    labels = dict( ((i, j), i + (_graph.L-1-j) * _graph.W ) for i, j in nodelist )
    # print(labels)
    nx.draw_networkx(G, pos=pos, labels=labels,with_labels=True, node_size=10)
    # nx.draw_networkx(G) 
    plt.show() 
    
def visualize( _graph: MLGraph ):
    helper = NodeHelper(_graph.L, _graph.W)
    adjList = []
    
    for srcNode in _graph.nodes:
        if srcNode == None:
            continue
        for adjNode in [srcNode.right, srcNode.bottom, srcNode.bottomRight]:
            if adjNode == None:
                continue
            adjList.append([srcNode.id, adjNode.id])
    
    print(adjList)
    
    def get_id_pos (_id):
        y, x = _id // _graph.W, _id % _graph.W
        y = _graph.L-1-y
        return x, y
    
    G = nx.empty_graph( n=0 )
    # exists nodes
    G.add_nodes_from((i, j) for i in range(_graph.W) for j in range(_graph.L))
    nodelist = copy.deepcopy(G.nodes())
    
    pos = dict( (n, n) for n in G.nodes() ) #Dictionary of all positions
    labels = dict( ((i, j), i + (_graph.L-1-j) * _graph.W ) for i, j in nodelist )
    # print(labels)
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