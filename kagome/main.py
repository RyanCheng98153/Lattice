import sys
from src.graph import KagomeGraph
from src.visualize import Visualize
from src.node import Spin
from src.node import Spin

def main():
    L:int = 6
    W:int = 6
    
    L:int = int(sys.argv[1])
    W:int = int(sys.argv[2])
    
    hexInit:int = 0
    # if (len(sys.argv) > 3):
    #     hexInit = int(sys.argv[3])
    
    graph = KagomeGraph(L, W, hexInit)
    graph.makeGraph()
    graph.bondGraph(1.0, 1.0, 1.0)
    # graph.printGraphText()
    # graph.printGraphVisual()
    
    if len(sys.argv) == 4:
        with open(sys.argv[3], "r") as f:
            datas = [line for line in f.readlines() if not line.startswith("#")]
        
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
        
        for node in graph.nodes:
            if node is not None:
                spin = Spin.UP if qubos[node.clean_id] == 1 else Spin.DOWN
                node.spin = spin
            # print((node.clean_id, node.spin) if node is not None else None)
        Visualize.visualize(graph, labelHexagon=False, showStrength=False, fromfile=True, save_fig=True)
    else:
        # with open(file=f"./kagome_L_{L}_{W}.txt", mode="w") as f:
        #     f.writelines(graph.getSpacefileText())
        Visualize.visualize(graph, labelHexagon=False, showStrength=False, save_fig=True)
    
if __name__ == "__main__":
    main()