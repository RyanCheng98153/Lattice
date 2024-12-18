import networkx as nx
from copy import deepcopy
import matplotlib.pyplot as plt
from src.graph import TrianglularGraph
from src.node import BondType, NodeType, Spin
from math import sqrt
 
class Visualize:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def visualize( _graph: TrianglularGraph, showStrength=False, fromfile=False, save_fig=False ):
        G: nx.Graph = nx.empty_graph( n=0 )
        
        def getPosition (_id):
            y, x = _id // _graph.W, _id % _graph.W
            y = _graph.L-1-y
            return (x, y)
        
        def getLightColor (color):
            if color == "Red" or color == "red":
                return "pink"
            return "light" + color
        
        def getSpinColor(spin: Spin):
            if spin == Spin.UP:
                return "lightblue"
            if spin == Spin.DOWN:
                return "blue"
        
        # ignore the hexagon None ndoes
        G.add_nodes_from( getPosition(node.id) for node in _graph.nodes if node is not None )
        if fromfile:
            color_map = [getSpinColor(node.spin) for node in _graph.nodes if node is not None]
        else:
            color_map = ["lightgray" for node in _graph.nodes if node is not None]
            # print(len(color_map))
            # use spin color
            # color_map = [(node.NodeType.name) for node in _graph.nodes if node is not None]

        nodelist = deepcopy(G.nodes()) # using deep copy not shallow copy because nx.network may return reference
        
        def getBondStyle(bondType: BondType) -> tuple[str, str]:
            return "black", "-"
                    
        for srcId, adjId, bondStrength, bondType in _graph.getAdjList():
            if bondType == None:
                bondColor, bondStyle = "black", "-"
            else:
                bondColor, bondStyle = getBondStyle(bondType)
                
            srcX, srcY = getPosition(srcId)
            
            # right bottom periodic
            if srcId == len(_graph.nodes) -1 and adjId == 0:
                G.add_edge( (srcX, srcY) , (_graph.W, -1), weight=bondStrength, bondColor=bondColor, bondStyle=bondStyle)
                
                continue
            # right periodic column
            if (srcId+1) % _graph.W == 0 and adjId % _graph.W == 0:
                adjX, adjY = getPosition(adjId)
                G.add_edge( (srcX, srcY), (_graph.W, adjY), weight=bondStrength, bondColor=bondColor, bondStyle=bondStyle)
                
                continue
            # bottom periodic row
            if srcId // _graph.W == _graph.L-1 and adjId // _graph.W == 0:
                adjX, adjY = getPosition(adjId)
                G.add_edge( (srcX, srcY), (adjX, -1), weight=bondStrength, bondColor=bondColor, bondStyle=bondStyle)
                
                continue
            G.add_edge( (srcX, srcY), getPosition(adjId), weight=bondStrength, bondColor=bondColor, bondStyle=bondStyle)
        
        sqrt3 = sqrt(3)
        pos = dict( ((i, j), (i+j/2, j*sqrt3)) for (i, j) in G.nodes() ) #Dictionary of all positions
        labels = dict( ((i, j), index) for index, (i, j) in enumerate(nodelist) ) #Add the labels to the nodes
        
        # draw
        bondColor = nx.get_edge_attributes(G, 'bondColor').values()
        bondStyle = nx.get_edge_attributes(G, 'bondStyle').values()
        # nodeColor = nx.get_edge_attributes(G, "nodeColor").values()
        weight_labels = nx.get_edge_attributes(G,'weight')
        
        node_width = 250 if _graph.L == 7 else 200
        edge_width = 3 if _graph.L == 7 else 2
        font_size = 10 if _graph.L == 7 else 8
        
        color_map.extend(["gray" for _ in range(G.nodes.__len__() - len(color_map))])
        
        fontcolor = "black" if fromfile else "black"
        
        nx.draw(G, pos, labels=labels, with_labels=True, 
                node_size=node_width, font_size=font_size, font_color=fontcolor,
                node_color = color_map, edgecolors="black",
                edge_color=bondColor, width=edge_width, style=bondStyle)    
        # add label of bond edge strength
        if showStrength:
            nx.draw_networkx_edge_labels(G,pos,edge_labels=weight_labels)
        
        if save_fig:
            plt.savefig(f"./fig_triangular_{_graph.L}_{_graph.L}.png", format='png', bbox_inches='tight')
        else:
            plt.show()