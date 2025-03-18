from src.graph import TrianglularGraph
from src.node import BondType, Spin
import math

class Analysis:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def getSpinValue(spin:Spin) -> int:
        return 1 if spin == Spin.UP else -1
    
    @staticmethod
    def get_triangular_Energy(graph:TrianglularGraph) -> float:
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
                
                tri_spins = [
                    Analysis.getSpinValue(node.spin), 
                    Analysis.getSpinValue(node.right.spin) ,
                    Analysis.getSpinValue(node.bottomRight.spin)
                ]
                
                triangular_energy.append((tri_nodes, tri_spins, energy))
            
            # triangle spin = node, bottom, bottomRight
            if node.bottomType == BondType.Triangle and node.bottomRightType == BondType.Triangle:
                energy = 0.0
                
                tri_nodes = [node.clean_id, node.bottom.clean_id, node.bottomRight.clean_id]
                energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.bottom.spin) * node.JBottom
                energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.bottomRight.spin) * node.JBottomRight
                energy += Analysis.getSpinValue(node.bottom.spin) * Analysis.getSpinValue(node.bottomRight.spin) * node.bottom.JRight
                
                tri_spins = [
                    Analysis.getSpinValue(node.spin) ,
                    Analysis.getSpinValue(node.bottom.spin) ,
                    Analysis.getSpinValue(node.bottomRight.spin)
                ]
                
                triangular_energy.append((tri_nodes, tri_spins, energy))
                
        # print(triangular_energy)
        for i, (tri_nodes, tri_spins, energy) in enumerate(triangular_energy):
            print(i, ")", tri_nodes, tri_spins, energy)
        
        print("Total Energy:", sum([energy for tri_nodes, tri_spins, energy in triangular_energy]))
        
        return triangular_energy
    
    @staticmethod
    def get_ordered_parameters(graph:TrianglularGraph) -> None:
        
        # for idx, node in enumerate(graph.nodes):
        #     if node is None:
        #         print(idx, None)
        #         continue
        #     print(idx, node.clean_id, node.spin, graph.helper.getCood(node.clean_id))
        
        # Blue, Black, Red declaration [pos_num, neg_num]
        color_parameter = {
            "red": [0, 0],
            "blue": [0, 0], 
            "black": [0, 0]
        }
        
        layer_energy = 0
        layer_count = 0
        
        for idx, node in enumerate(graph.nodes):
            i, j = graph.helper.getCood(idx)
            
            if node is None:
                continue
            
            # change color: red = 0, blue = 1, black = 2
            # color = ( 2*i+j ) % 3 => 0, 1, 2 => red, blue, black
            color = {
                0: "red",
                1: "blue",
                2: "black"
            }.get(( i+j+1 ) % 3)
            
            if node.spin == Spin.UP:
                color_parameter[color][0] += 1
            elif node.spin == Spin.DOWN:
                color_parameter[color][1] += 1
            else:
                raise Exception("Invalid Spin")
            
            # print(idx, node.clean_id, node.spin, graph.helper.getCood(node.clean_id), color)
            
            if node.right is not None:
                layer_energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.right.spin) * node.JRight
            layer_count += 1
            if node.bottom is not None:
                layer_energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.bottom.spin) * node.JBottom
            layer_count += 1
            if node.bottomRight is not None:
                layer_energy += Analysis.getSpinValue(node.spin) * Analysis.getSpinValue(node.bottomRight.spin) * node.JBottomRight
            layer_count += 1 
        
        print("Layer Energy:", layer_energy)
        # print("Layer Count:", layer_count)
        # print every color parameter in different lines
        print("Color Parameters:")
        for color, values in color_parameter.items():
            print(f"[{color.capitalize()}]:", "pos:", values[0], "neg:", values[1])
        
        # Order parameters
        m_red = (color_parameter["red"][0] - color_parameter["red"][1]) / (color_parameter["red"][0] + color_parameter["red"][1])
        m_blue = (color_parameter["blue"][0] - color_parameter["blue"][1]) / (color_parameter["blue"][0] + color_parameter["blue"][1])
        m_black = (color_parameter["black"][0] - color_parameter["black"][1]) / (color_parameter["black"][0] + color_parameter["black"][1])
        
        imagine_pi = complex(real=0, imag=4/3 * math.pi)
        
        order_parameter = (
            m_red * (math.e ** imagine_pi)
            + m_blue 
            + m_black * (math.e ** (imagine_pi * -1.0))
        ) / math.sqrt(3)
        
        NP_order_parameter = (
            m_red * (math.cos(math.pi * 4 / 3) + math.sin(math.pi * 4 / 3) * complex(real=0, imag=1))
            + m_blue 
            + m_black * (math.cos(math.pi * 4 / 3) - math.sin(math.pi * 4 / 3) * complex(real=0, imag=1))
        ) / math.sqrt(3)
        
        print("Ordered_parameter = ", "Real:", order_parameter.real, "Imag:", order_parameter.imag)
        print("Length of Order_P:", order_parameter.real ** 2 + order_parameter.imag ** 2)
        
        print("(NP) Ordered_parameter = ", "Real:", NP_order_parameter.real, "Imag:", NP_order_parameter.imag)
        print("(NP) Length of Order_P:", NP_order_parameter.real ** 2 + NP_order_parameter.imag ** 2)
        
        return