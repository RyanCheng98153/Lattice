import argparse
from enum import Enum

class Model(Enum):
    Triangular = "triangular"
    MapleLeaf = "mapleleaf"
    Kagome = "kagome"
    
    def __str__(self):
        return self.value

class Kagome:
    def __init__(self,
                 ):
        pass

    def draw(self,
        _ids: list[int],
        _vars: list[list[int]]
    ):
        pass
    
def main(_model: Model):
    
    with open(args.filename, "r") as f:
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
    
    # i = int(input("Pick Result: "))
    i = 0
    
    if _model == Model.Kagome:
        print( results[i] )
        graph = Kagome(ids, results[qubos])
        
    
if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", 
                        "--model",
                        type=Model,
                        choices=list(Model),
                        required=True
                        )

    parser.add_argument("-f", 
                        "--filename",
                        type=str,
                        required=True
                        )

    args = parser.parse_args()
    
    main( _model=args.model )