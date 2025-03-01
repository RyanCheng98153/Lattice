import networkx as nx
from copy import deepcopy
import matplotlib.pyplot as plt
from src.graph import MLGraph
from src.node import BondType, Spin
from math import sqrt
from enum import Enum

class DisplayType(Enum):
    PLAIN = "plain"
    SPIN_FILE = "spinfile"
    ORDER_PARAMETERS = "orderP"
    
    def description(self):
        descriptions = {
            self.PLAIN: "Displaying theorical graph with no styling",
            self.SPIN_FILE: "Displaying spin of input file",
            self.ORDER_PARAMETERS: "Displaying order parameters",
        }
        return descriptions[self]
 
class Visualize:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def visualize(
        _graph: MLGraph, 
        labelHexagon = False, showStrength=False, save_fig=False, 
        display_type: DisplayType = DisplayType.PLAIN
    ):
        G: nx.Graph = nx.empty_graph( n=0 )
        
        def getPosition (_id):
            y, x = _id // _graph.W, _id % _graph.W
            y = _graph.L-1-y
            return (x, y)
        
        def getSpinColor(spin: Spin):
            if spin == Spin.UP:
                return "lightblue"
            if spin == Spin.DOWN:
                return "blue"
        
        def getOrderColor(id: int) -> str:
            i, j = _graph.helper.getCood(id)
            
            return {
                0: "red",
                1: "blue",
                2: "lightgreen"
            }.get(( i+j+1 ) % 3)
        
        # add Graphs nodes to networkx graph
        if labelHexagon:
            G.add_nodes_from(getPosition(id) for id in range(len(_graph.nodes)))
            nodes = _graph.nodes
        else:
            nodes = [node for node in _graph.nodes if labelHexagon or node is not None]
            G.add_nodes_from(getPosition(node.id) for node in nodes)
            
        if display_type == DisplayType.PLAIN:
            color_map = ["lightgray" if node is not None else "grey" for node in nodes]
        elif display_type == DisplayType.SPIN_FILE:
            color_map = [getSpinColor(node.spin) if node is not None else "grey" for node in nodes]
        elif display_type == DisplayType.ORDER_PARAMETERS:
            color_map = [getOrderColor(node.id) if node is not None else "grey" for node in nodes]
        else:
            raise ValueError("Invalid display type")
        
        nodelist = deepcopy(G.nodes()) # using deep copy not shallow copy because nx.network may return reference
        
        def getBondStyle(bondType: BondType, no_color = True) -> tuple[str, str]:
            if no_color:
                return "gray", "-"
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
                G.add_edge(getPosition(srcId), (_graph.W, -1), weight=bondStrength, bondColor=bondColor, bondStyle=bondStyle)
                continue
            # right periodic column
            if (srcId+1) % _graph.W == 0 and adjId % _graph.W == 0:
                adjX, adjY = getPosition(adjId)
                G.add_edge(getPosition(srcId), (_graph.W, adjY), weight=bondStrength, bondColor=bondColor, bondStyle=bondStyle)
                continue
            # bottom periodic row
            if srcId // _graph.W == _graph.L-1 and adjId // _graph.W == 0:
                adjX, adjY = getPosition(adjId)
                G.add_edge(getPosition(srcId), (adjX, -1), weight=bondStrength, bondColor=bondColor, bondStyle=bondStyle)
                continue
            G.add_edge(getPosition(srcId), getPosition(adjId), weight=bondStrength, bondColor=bondColor, bondStyle=bondStyle)
            
        sqrt3 = sqrt(3)
        pos = dict( ((i, j), (i+j/2, j*sqrt3)) for (i, j) in G.nodes() ) #Dictionary of all positions
        labels = dict( ((i, j), index) for index, (i, j) in enumerate(nodelist) ) #Add the labels to the nodes
        
        # draw
        bondColor = nx.get_edge_attributes(G, 'bondColor').values()
        bondStyle = nx.get_edge_attributes(G, 'bondStyle').values()
        weight_labels = nx.get_edge_attributes(G,'weight')
        
        node_width = 250 if _graph.L == 7 else 200
        edge_width = 3 if _graph.L == 7 else 2
        font_size = 10 if _graph.L == 7 else 8
        
        # small node with no font size
        node_width = 100
        show_labels = False
        
        # color of periodic nodes
        node_num = len(color_map)
        for i in range(G.nodes.__len__() - node_num):
            
            if DisplayType.SPIN_FILE:
                color_map.append("gray")
            elif DisplayType.ORDER_PARAMETERS:
                color_map.append("gray")
            elif DisplayType.PLAIN:
                color_map.append("orange")
        
        nx.draw(G, pos, labels=labels, with_labels=show_labels, 
                node_size=node_width, font_size=font_size, 
                node_color=color_map, edgecolors="black",
                edge_color=bondColor, width=edge_width, style=bondStyle)    
        # add label of bond edge strength
        if showStrength:
            nx.draw_networkx_edge_labels(G,pos,edge_labels=weight_labels)
        
        if save_fig:
            plt.savefig(f"./fig_mapleleaf_{_graph.L}_{_graph.L}.pdf", format='pdf', bbox_inches='tight')
        # else:
        #     plt.show()