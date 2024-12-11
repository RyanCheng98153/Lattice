import sys
from src.graph import MLGraph
from src.test import Test
from src.visualize import Visualize
from src.node import Spin
from math import sqrt
from enum import Enum
from src.node import Spin
    
def main():
    L:int = int(sys.argv[1])
    W:int = int(sys.argv[2])
    
    hexInit:int = 0
    # if (len(sys.argv) > 3):
    #     hexInit = int(sys.argv[3])
    
    graph:MLGraph = MLGraph(L, W, hexInit)
    graph.makeGraph()
    # graph.bondGraph(3.0, 6.0, 2.0)
    graph.bondGraph(1.0, 1.0, 1.0)
    # graph.printGraphText()
    # graph.printGraphVisual()
    
    # with open(file=f"./mapleleaf_L_{L}_{W}.txt", mode="w") as f:
    #     f.writelines(graph.getSpacefileText())
    # Test.checkIsingleNode(graph)
    
    if len(sys.argv) == 4:
        with open(sys.argv[3], "r") as f:
            datas = f.readlines()
        
        ids = [int(id) for id in datas[0].split()[:-2]]
        
        results = []
        for data in datas[1:]:
            if data.startswith("['SPIN'"):
                break
            if not data[0].isdigit():
                continue
            
            items = data.split()
            qubos = [ -1 if var == "-1" else 1 for var in items[1:-2] ]
            energy = items[-2]
            
            if energy.startswith("-"):
                energy = -1 * float(energy[1:])
            else:
                energy = float(energy)
            
            results.append( { "qubos": qubos, "energy": energy })
        
        i = 0
        
        qubos = results[i]["qubos"]
        
        L:int = int(sqrt( len(qubos) ))
        W:int = L

        for node in graph.nodes:
            if node is not None:
                spin = Spin.UP if qubos[node.clean_id] == 1 else Spin.DOWN
                node.spin = spin
            # print((node.clean_id, node.spin) if node is not None else None)
            
        
    Visualize.visualize(graph, labelHexagon=False, showStrength=False)
    
if __name__ == "__main__":
    main()