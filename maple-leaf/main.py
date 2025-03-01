import argparse
from src.graph import MLGraph
from src.visualize import Visualize, DisplayType
from src.node import Spin
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
    
    L:int = args.L
    W:int = args.W
    
    graph:MLGraph = MLGraph(L, W, 0)
    graph.makeGraph()
    graph.bondGraph(1.0, 1.0, 1.0)
    
    if args.inputFile is not None:
        results = getFileQubos(args.inputFile)
        
        qubos = results[0]["qubos"]
        
        for node in graph.nodes:
            if node is not None:
                spin = Spin.UP if qubos[node.clean_id] == 1 else Spin.DOWN
                node.spin = spin
            # print((node.clean_id, node.spin) if node is not None else None)

        # Analysis.get_triangular_Energy(graph)
        Analysis.get_ordered_parameters(graph)

    # check if the args.display_type match DisplayType's value
    display_type = {
        "plain": DisplayType.PLAIN,
        "spinfile": DisplayType.SPIN_FILE,
        "orderP": DisplayType.ORDER_PARAMETERS
    }.get(args.displayType)
    
    Visualize.visualize(graph, labelHexagon=False, showStrength=False, save_fig=args.saveFig, display_type=display_type)
    
    if args.saveLattice:
        with open(file=f"./mapleleaf_L_{L}_{W}.txt", mode="w") as f:
            f.writelines(graph.getSpacefileText())
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MapleLeaf Graph")
    parser.add_argument("-L", type=int, help="Lattice size")
    parser.add_argument("-W", type=int, help="Lattice size")
    parser.add_argument("--inputFile", required=False, default=None, type=str, help="file path")
    parser.add_argument("--saveFig", required=False, default=False , action="store_true", help="save figure")
    parser.add_argument("--saveLattice", required=False, default=False , action="store_true", help="save lattice file")
    parser.add_argument("--displayType", required=False, default=None, type=str, help="display type (plain, spinfile, orderP)")
    args = parser.parse_args()
    
    if args.displayType is None:
        if args.inputFile is None:
            args.displayType = "plain"
        else:
            args.displayType = "spinfile"
        
    main(args)