from src.graph import KagomeGraph
from src.node import BondType, Spin

class Analysis:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def getSpinValue(spin:Spin) -> int:
        return 1 if spin == Spin.UP else -1
    
    @staticmethod
    def get_triangular_Energy(graph:KagomeGraph) -> float:
        triangular_energy: list[tuple[list[int], float]] = []
        
        for node in graph.nodes:
            if node is None:
                continue
            
            # triangle spin = node, right, bottomRight
            if node.rightType == BondType.Connected and node.bottomRightType == BondType.Connected:
                energy = 0.0
                
                tri_nodes = [node.clean_id, node.right.clean_id, node.bottomRight.clean_id]
                energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.right.spin) * node.JRight
                energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.bottomRight.spin) * node.JBottomRight
                energy += Analysis.getSpinValue(node.right.spin) * Analysis.getSpinValue(node.bottomRight.spin) * node.right.JBottom
                
                tri_spins = Analysis.getSpinValue(node.spin) 
                tri_spins += Analysis.getSpinValue(node.right.spin) 
                tri_spins += Analysis.getSpinValue(node.bottomRight.spin)
                
                triangular_energy.append((tri_nodes, energy, tri_spins))
            
            # triangle spin = node, bottom, bottomRight
            if node.bottomType == BondType.Connected and node.bottomRightType == BondType.Connected:
                energy = 0.0
                
                tri_nodes = [node.clean_id, node.bottom.clean_id, node.bottomRight.clean_id]
                energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.bottom.spin) * node.JBottom
                energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.bottomRight.spin) * node.JBottomRight
                energy += Analysis.getSpinValue(node.bottom.spin) * Analysis.getSpinValue(node.bottomRight.spin) * node.bottom.JRight
                
                triangular_energy.append((tri_nodes, energy, tri_spins))
                
        # print(triangular_energy)
        # for i, (tri_nodes, energy, tri_spins) in enumerate(triangular_energy):
        #     print(i, ")", tri_nodes, energy, tri_spins)
        
        print("Total Energy:", sum([energy for tri_nodes, energy, tri_spins in triangular_energy]))
        print("Total Spin:", sum([tri_spins for tri_nodes, energy, tri_spins in triangular_energy]))
        
        return triangular_energy