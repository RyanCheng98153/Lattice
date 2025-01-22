import sys
from src.graph import MLGraph
from src.visualize import Visualize
from src.node import Spin
import argparse
from src.analysis import Analysis

def getFileQubos(inputFile: str):
    with open(inputFile, "r") as f:
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
        
    return results

def main(arge: argparse.Namespace):
    L:int = 6
    W:int = 6
    
    # L:int = int(sys.argv[1])
    # W:int = int(sys.argv[2])
    L:int = args.L
    W:int = args.W
    
    hexInit:int = 0
    # if (len(sys.argv) > 3):
    #     hexInit = int(sys.argv[3])
    
    graph:MLGraph = MLGraph(L, W, hexInit)
    graph.makeGraph()
    # graph.bondGraph(3.0, 6.0, 2.0)
    graph.bondGraph(1.0, 1.0, 1.0)
    # graph.printGraphText()
    # graph.printGraphVisual()
    
    # if len(sys.argv) == 4:
    if args.inputFile is not None:
        # with open(sys.argv[3], "r") as f:
        results = getFileQubos(args.inputFile)
        
        qubos = results[0]["qubos"]
        
        for node in graph.nodes:
            if node is not None:
                spin = Spin.UP if qubos[node.clean_id] == 1 else Spin.DOWN
                node.spin = spin
            # print((node.clean_id, node.spin) if node is not None else None)

        Analysis.get_triangular_Energy(graph)

        Visualize.visualize(graph, labelHexagon=False, showStrength=False, fromfile=True, save_fig=args.saveFig)
        pass
    else:    
        Visualize.visualize(graph, labelHexagon=False, showStrength=False, save_fig=args.saveFig)
        pass
    
    if args.saveLattice:
        with open(file=f"./mapleleaf_L_{L}_{W}.txt", mode="w") as f:
            f.writelines(graph.getSpacefileText())
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Triangular Graph")
    parser.add_argument("-L", type=int, help="Lattice size")
    parser.add_argument("-W", type=int, help="Lattice size")
    parser.add_argument("--inputFile", required=False, type=str, help="file path")
    parser.add_argument("--saveFig", required=False, default=False , action="store_true", help="save figure")
    parser.add_argument("--saveLattice", required=False, default=False , action="store_true", help="save lattice file")
    args = parser.parse_args()
    main(args)