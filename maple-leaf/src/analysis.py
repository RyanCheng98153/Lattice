from src.graph import MLGraph
from src.node import BondType, Spin

class Analysis:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def getSpinValue(spin:Spin) -> int:
        return 1 if spin == Spin.UP else -1
    
    @staticmethod
    def get_triangular_Energy(graph:MLGraph) -> float:
        triangular_energy: list[tuple[list[int], float]] = []
        
        for node in graph.nodes:
            if node is None:
                continue
            
            # triangle spin = node, right, bottomRight
            if node.rightType == BondType.Triangle and node.bottomRightType == BondType.Triangle:
                energy = 0.0
                
                tri_nodes = [node.clean_id, node.right.clean_id, node.bottomRight.clean_id]
                energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.right.spin) * node.JRight
                energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.bottomRight.spin) * node.JBottomRight
                energy += Analysis.getSpinValue(node.right.spin) * Analysis.getSpinValue(node.bottomRight.spin) * node.right.JBottom
                
                triangular_energy.append((tri_nodes, energy))
            
            # triangle spin = node, bottom, bottomRight
            if node.bottomType == BondType.Triangle and node.bottomRightType == BondType.Triangle:
                energy = 0.0
                
                tri_nodes = [node.clean_id, node.bottom.clean_id, node.bottomRight.clean_id]
                energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.bottom.spin) * node.JBottom
                energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.bottomRight.spin) * node.JBottomRight
                energy += Analysis.getSpinValue(node.bottom.spin) * Analysis.getSpinValue(node.bottomRight.spin) * node.bottom.JRight
                
                triangular_energy.append((tri_nodes, energy))
                
        # print(triangular_energy)
        for tri_nodes, energy in triangular_energy:
            print(tri_nodes, energy)
        
        print("Total Energy:", sum([energy for tri_nodes, energy in triangular_energy]))
        
        return triangular_energy