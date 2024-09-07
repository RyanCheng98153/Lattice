import networkx as nx
from copy import deepcopy
import matplotlib.pyplot as plt
from src.graph import MLGraph
from src.node import BondType
from math import sqrt
 
class Visualize:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def visualizeTriangular( _graph: MLGraph ):
        G:nx.Graph = nx.empty_graph( n=0 )
        # exists nodes
        G.add_nodes_from((i, j) for i in range(_graph.W) for j in range(_graph.L))
        nodelist = deepcopy(G.nodes())
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
    
    @staticmethod
    def visualize( _graph: MLGraph, labelHexagon = False, showStrength=False ):
        G: nx.Graph = nx.empty_graph( n=0 )
        
        def getPosition (_id):
            y, x = _id // _graph.W, _id % _graph.W
            y = _graph.L-1-y
            return (x, y)
        
        # add MLGraphs nodes to networkx graph
        if labelHexagon:
            G.add_nodes_from( getPosition( id ) for id in range(len(_graph.nodes)) )
        else:
            # ignore the hexagon None ndoes
            G.add_nodes_from( getPosition(node.id) for node in _graph.nodes if node is not None )
        
        nodelist = deepcopy(G.nodes()) # using deep copy not shallow copy because nx.network may return reference
        
        # get edgeList from adjList
        # edgesList = []
        
        def getBondStyle(bondType: BondType) -> tuple[str, str]:
            if bondType == BondType.Hexagon:
                return "blue", "-"
            if bondType == BondType.Triangle:
                # return "orange", ":"
                return "orange", "--"
            if bondType == BondType.Dimer:
                return "red", "-"
        
        for srcId, adjId, bondStrength, bondType in _graph.getAdjList():
            if bondType == None:
                bondColor, bondStyle = "black", "-"
            else:
                bondColor, bondStyle = getBondStyle(bondType)
            
            # right button periodic
            if srcId == len(_graph.nodes) -1 and adjId == 0:
                # edgesList.append((getPosition(srcId), (_graph.W, -1), bondStrength))
                G.add_edge(getPosition(srcId), (_graph.W, -1), weight=bondStrength, color=bondColor, style=bondStyle)
                continue
            # right periodic column
            if (srcId+1) % _graph.W == 0 and adjId % _graph.W == 0:
                adjX, adjY = getPosition(adjId)
                # edgesList.append((getPosition(srcId), (_graph.W, adjY), bondStrength ))
                G.add_edge(getPosition(srcId), (_graph.W, adjY), weight=bondStrength, color=bondColor, style=bondStyle)
                continue
            # bottom periodic row
            if srcId // _graph.W == _graph.L-1 and adjId // _graph.W == 0:
                adjX, adjY = getPosition(adjId)
                # edgesList.append((getPosition(srcId), (adjX, -1), bondStrength ))
                G.add_edge(getPosition(srcId), (adjX, -1), weight=bondStrength, color=bondColor, style=bondStyle)
                continue
            # edgesList.append((getPosition(srcId), getPosition(adjId), bondStrength ))
            # color = bondColor(bondType)
            G.add_edge(getPosition(srcId), getPosition(adjId), weight=bondStrength, color=bondColor, style=bondStyle)
            
        # print(edgesList)
        # add the edges to the graph
        # G.add_weighted_edges_from( edgesList )
        
        sqrt3 = sqrt(3)
        pos = dict( ((i, j), (i+j/2, j*sqrt3)) for (i, j) in G.nodes() ) #Dictionary of all positions
        labels = dict( ((i, j), index) for index, (i, j) in enumerate(nodelist) ) #Add the labels to the nodes
        
        # draw
        bondColor = nx.get_edge_attributes(G, 'color').values()
        bondStyle = nx.get_edge_attributes(G, 'style').values()
        weight_labels = nx.get_edge_attributes(G,'weight')
        
        node_width = 250 if _graph.L == 7 else 200
        edge_width = 3 if _graph.L == 7 else 2
        font_size = 10 if _graph.L == 7 else 8
        
        nx.draw(G, pos, labels=labels, with_labels=True, 
                node_size=node_width, font_size=font_size, 
                node_color = "orange", edgecolors="black",
                edge_color=bondColor, width=edge_width, style=bondStyle)    
        # add label of bond edge strength
        if showStrength:
            nx.draw_networkx_edge_labels(G,pos,edge_labels=weight_labels)
        
        plt.show()
